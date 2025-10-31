"""
Google Drive API service
"""
from typing import Optional, Dict, Any
from io import BytesIO
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
from core.exceptions import DriveAPIError, FolderCreationError, FileUploadError
from config.settings import settings
from config.logging_config import get_logger
from utils.retry import retry_on_api_error

logger = get_logger(__name__)

SCOPES = ['https://www.googleapis.com/auth/drive']


class DriveService:
    """Google Drive API wrapper"""

    def __init__(self):
        """Initialize Drive service"""
        try:
            credentials = service_account.Credentials.from_service_account_info(
                settings.google_credentials,
                scopes=SCOPES
            )
            self.service = build('drive', 'v3', credentials=credentials)
            logger.info("Drive service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Drive service: {e}")
            raise DriveAPIError(f"Drive service initialization failed: {e}")

    @retry_on_api_error(max_attempts=3)
    def create_folder(
        self,
        folder_name: str,
        parent_folder_id: Optional[str] = None
    ) -> str:
        """
        Create a folder in Google Drive

        Args:
            folder_name: Folder name
            parent_folder_id: Parent folder ID (None for root)

        Returns:
            Folder ID

        Raises:
            FolderCreationError: If folder creation fails
        """
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }

            if parent_folder_id:
                file_metadata['parents'] = [parent_folder_id]

            folder = self.service.files().create(
                body=file_metadata,
                fields='id, name, webViewLink'
            ).execute()

            folder_id = folder.get('id')
            logger.info(f"Folder created: {folder_name} (ID: {folder_id})")
            return folder_id

        except Exception as e:
            logger.error(f"Folder creation failed: {folder_name}, error: {e}")
            raise FolderCreationError(f"Failed to create folder {folder_name}: {e}")

    @retry_on_api_error(max_attempts=3)
    def find_folder(
        self,
        folder_name: str,
        parent_folder_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Find folder by name

        Args:
            folder_name: Folder name
            parent_folder_id: Parent folder ID

        Returns:
            Folder ID if found, None otherwise
        """
        try:
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            if parent_folder_id:
                query += f" and '{parent_folder_id}' in parents"

            response = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)',
                pageSize=1
            ).execute()

            files = response.get('files', [])
            if files:
                return files[0]['id']
            return None

        except Exception as e:
            logger.warning(f"Folder search failed: {folder_name}, error: {e}")
            return None

    def ensure_folder_path(
        self,
        folder_path: str,
        root_folder_id: Optional[str] = None
    ) -> str:
        """
        Ensure folder path exists, creating folders as needed

        Args:
            folder_path: Folder path (e.g., "01_KR_TO_3PL/TA717001250829/BL")
            root_folder_id: Root folder ID

        Returns:
            Final folder ID
        """
        parts = folder_path.strip('/').split('/')
        current_parent_id = root_folder_id or settings.google_drive_root_folder_id

        for part in parts:
            # Try to find existing folder
            folder_id = self.find_folder(part, current_parent_id)

            if not folder_id:
                # Create folder if it doesn't exist
                folder_id = self.create_folder(part, current_parent_id)

            current_parent_id = folder_id

        logger.info(f"Folder path ensured: {folder_path} (ID: {current_parent_id})")
        return current_parent_id

    @retry_on_api_error(max_attempts=3)
    def upload_file(
        self,
        file_content: bytes,
        file_name: str,
        folder_id: str,
        mime_type: str = 'application/pdf'
    ) -> Dict[str, Any]:
        """
        Upload file to Google Drive

        Args:
            file_content: File content (bytes)
            file_name: File name
            folder_id: Destination folder ID
            mime_type: MIME type

        Returns:
            Dict with file_id and drive_url

        Raises:
            FileUploadError: If upload fails
        """
        try:
            file_metadata = {
                'name': file_name,
                'parents': [folder_id]
            }

            media = MediaIoBaseUpload(
                BytesIO(file_content),
                mimetype=mime_type,
                resumable=True
            )

            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()

            file_id = file.get('id')
            drive_url = file.get('webViewLink')

            logger.info(f"File uploaded: {file_name} (ID: {file_id})")

            return {
                'file_id': file_id,
                'drive_url': drive_url
            }

        except Exception as e:
            logger.error(f"File upload failed: {file_name}, error: {e}")
            raise FileUploadError(f"Failed to upload file {file_name}: {e}")

    @retry_on_api_error(max_attempts=3)
    def delete_file(self, file_id: str) -> None:
        """Delete file from Drive"""
        try:
            self.service.files().delete(fileId=file_id).execute()
            logger.info(f"File deleted: {file_id}")
        except Exception as e:
            logger.error(f"File deletion failed: {file_id}, error: {e}")
            raise DriveAPIError(f"Failed to delete file {file_id}: {e}")
