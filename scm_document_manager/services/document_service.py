"""
Document service orchestration
"""
from datetime import datetime
from typing import Optional
from core.models import DocumentMetadata, UploadResult
from core.enums import UploadStatus
from core.exceptions import ValidationError
from config.settings import settings
from config.logging_config import get_logger
from utils.folder_utils import determine_shipment_category, build_folder_path, build_file_name
from .drive_service import DriveService
from .sheets_service import SheetsService

logger = get_logger(__name__)


class DocumentService:
    """Document upload orchestration service"""

    def __init__(
        self,
        drive_service: Optional[DriveService] = None,
        sheets_service: Optional[SheetsService] = None
    ):
        """Initialize document service"""
        self.drive = drive_service or DriveService()
        self.sheets = sheets_service or SheetsService()

    def upload_document(
        self,
        file_content: bytes,
        file_name: str,
        shipment_id: str,
        doc_type: str,
        doc_type_abbr: str,
        uploader: Optional[str] = None,
        origin: Optional[str] = None,
        destination: Optional[str] = None,
        carrier_name: Optional[str] = None,
        carrier_mode: Optional[str] = None
    ) -> UploadResult:
        """
        Upload document with full orchestration

        Args:
            file_content: File content (bytes)
            file_name: Original file name
            shipment_id: Invoice number
            doc_type: Document type
            doc_type_abbr: Document type abbreviation
            uploader: Uploader name
            origin: 출발창고
            destination: 도착창고
            carrier_name: 운송사
            carrier_mode: 운송 모드

        Returns:
            UploadResult
        """
        try:
            # Validate file size
            file_size_bytes = len(file_content)
            if file_size_bytes > settings.max_file_size_bytes:
                raise ValidationError(
                    f"File size ({file_size_bytes / 1024 / 1024:.2f}MB) exceeds limit "
                    f"({settings.max_file_size_mb}MB)"
                )

            # Use default uploader if not provided
            uploader = uploader or settings.default_uploader

            # Determine shipment category and folder path
            category = determine_shipment_category(
                origin=origin or "",
                destination=destination or "",
                doc_type=doc_type
            )

            folder_path = build_folder_path(category, shipment_id, doc_type)

            logger.info(f"Uploading to folder path: {folder_path}")

            # Ensure folder exists
            folder_id = self.drive.ensure_folder_path(folder_path)

            # Build standardized file name
            upload_date = datetime.now().strftime("%Y%m%d")
            std_file_name = build_file_name(upload_date, doc_type_abbr, file_name)

            # Determine MIME type
            mime_type = self._get_mime_type(file_name)

            # Upload file
            upload_result = self.drive.upload_file(
                file_content=file_content,
                file_name=std_file_name,
                folder_id=folder_id,
                mime_type=mime_type
            )

            # Create metadata
            metadata = DocumentMetadata(
                shipment_id=shipment_id,
                doc_type=doc_type,
                file_name=std_file_name,
                drive_file_id=upload_result['file_id'],
                drive_url=upload_result['drive_url'],
                drive_folder_id=folder_id,
                uploader=uploader,
                file_size_bytes=file_size_bytes,
                status=UploadStatus.UPLOADED,
                carrier_name=carrier_name,
                carrier_mode=carrier_mode,
                origin=origin,
                destination=destination
            )

            # Log to Dashboard sheet
            self.sheets.append_upload_log(metadata)

            logger.info(f"Document uploaded successfully: {shipment_id}/{doc_type}")

            return UploadResult(
                success=True,
                message=f"File uploaded successfully: {std_file_name}",
                metadata=metadata
            )

        except Exception as e:
            logger.error(f"Document upload failed: {e}")
            return UploadResult(
                success=False,
                message="Upload failed",
                error=str(e)
            )

    def _get_mime_type(self, file_name: str) -> str:
        """Determine MIME type from file extension"""
        ext = file_name.lower().split('.')[-1]

        mime_types = {
            'pdf': 'application/pdf',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'xls': 'application/vnd.ms-excel',
            'csv': 'text/csv',
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg'
        }

        return mime_types.get(ext, 'application/octet-stream')
