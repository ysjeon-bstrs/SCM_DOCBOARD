"""
Google Sheets API service
"""
from typing import List, Dict, Optional, Any
import gspread
from google.oauth2 import service_account
from core.exceptions import SheetsAPIError
from core.models import ShipmentInfo, DocumentMetadata
from config.settings import settings
from config.logging_config import get_logger
from utils.retry import retry_on_api_error

logger = get_logger(__name__)

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


class SheetsService:
    """Google Sheets API wrapper"""

    def __init__(self):
        """Initialize Sheets service"""
        try:
            credentials = service_account.Credentials.from_service_account_info(
                settings.google_credentials,
                scopes=SCOPES
            )
            self.client = gspread.authorize(credentials)
            logger.info("Sheets service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Sheets service: {e}")
            raise SheetsAPIError(f"Sheets service initialization failed: {e}")

    @retry_on_api_error(max_attempts=3)
    def search_shipments(self, search_term: str) -> List[ShipmentInfo]:
        """
        Search shipments in SCM 통합 시트

        Args:
            search_term: Search term (invoice number or partial match)

        Returns:
            List of matching ShipmentInfo
        """
        try:
            sheet = self.client.open_by_key(settings.invoice_sheet_id)
            worksheet = sheet.worksheet(settings.invoice_sheet_name)

            # Get all records
            records = worksheet.get_all_records()

            # Filter by search term
            search_lower = search_term.lower()
            matches = []

            for record in records:
                invoice_no = str(record.get('인보이스 번호', '')).lower()
                ticket_name = str(record.get('티켓명', '')).lower()

                if search_lower in invoice_no or search_lower in ticket_name:
                    try:
                        shipment = ShipmentInfo(
                            invoice_no=record.get('인보이스 번호', ''),
                            ticket_name=record.get('티켓명'),
                            carrier_name=record.get('carrier_name', ''),
                            carrier_mode=record.get('carrier_mode', ''),
                            origin=record.get('출발창고', ''),
                            destination=record.get('도착창고', ''),
                            onboard_date=str(record.get('onboard_date', '')),
                            bl_no=record.get('bl_no'),
                            status=record.get('status')
                        )
                        matches.append(shipment)
                    except Exception as e:
                        logger.warning(f"Failed to parse shipment record: {e}")
                        continue

            logger.info(f"Found {len(matches)} shipments matching '{search_term}'")
            return matches

        except Exception as e:
            logger.error(f"Shipment search failed: {e}")
            raise SheetsAPIError(f"Failed to search shipments: {e}")

    @retry_on_api_error(max_attempts=3)
    def append_upload_log(self, metadata: DocumentMetadata) -> None:
        """
        Append upload log to Dashboard sheet

        Args:
            metadata: Document metadata to log
        """
        try:
            sheet = self.client.open_by_key(settings.dashboard_sheet_id)
            worksheet = sheet.worksheet(settings.dashboard_sheet_name)

            # Prepare row data (18 columns)
            row = [
                metadata.upload_timestamp.isoformat(),
                metadata.shipment_id,
                metadata.doc_type,
                metadata.file_name,
                metadata.drive_file_id,
                metadata.drive_url,
                metadata.drive_folder_id,
                metadata.uploader,
                metadata.file_size_bytes,
                metadata.status.value,
                metadata.error_message or '',
                metadata.carrier_name or '',
                metadata.carrier_mode or '',
                metadata.origin or '',
                metadata.destination or '',
                metadata.extracted_text or '',
                metadata.extracted_json or '',
                metadata.embedding_status or ''
            ]

            worksheet.append_row(row)
            logger.info(f"Upload log appended: {metadata.shipment_id}/{metadata.doc_type}")

        except Exception as e:
            logger.error(f"Failed to append upload log: {e}")
            raise SheetsAPIError(f"Failed to append upload log: {e}")

    @retry_on_api_error(max_attempts=3)
    def get_upload_logs(
        self,
        shipment_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get upload logs from Dashboard sheet

        Args:
            shipment_id: Filter by shipment ID (optional)
            limit: Maximum number of records to return

        Returns:
            List of upload log records
        """
        try:
            sheet = self.client.open_by_key(settings.dashboard_sheet_id)
            worksheet = sheet.worksheet(settings.dashboard_sheet_name)

            records = worksheet.get_all_records()

            if shipment_id:
                records = [r for r in records if r.get('shipment_id') == shipment_id]

            # Return most recent first
            records = list(reversed(records))[:limit]

            logger.info(f"Retrieved {len(records)} upload logs")
            return records

        except Exception as e:
            logger.error(f"Failed to get upload logs: {e}")
            raise SheetsAPIError(f"Failed to get upload logs: {e}")
