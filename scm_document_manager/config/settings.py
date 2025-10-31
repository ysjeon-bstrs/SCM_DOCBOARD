"""
Settings management using Pydantic Settings
"""
import json
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Google Drive
    google_drive_root_folder_id: str = Field(
        ...,
        env="GOOGLE_DRIVE_ROOT_FOLDER_ID",
        description="Google Drive root folder ID"
    )

    # Google Sheets
    invoice_sheet_id: str = Field(
        ...,
        env="INVOICE_SHEET_ID",
        description="SCM 통합 시트 ID"
    )
    invoice_sheet_name: str = Field(
        default="scm통합",
        env="INVOICE_SHEET_NAME",
        description="SCM 통합 시트 탭 이름"
    )
    dashboard_sheet_id: str = Field(
        ...,
        env="DASHBOARD_SHEET_ID",
        description="Dashboard 시트 ID"
    )
    dashboard_sheet_name: str = Field(
        default="dashboard",
        env="DASHBOARD_SHEET_NAME",
        description="Dashboard 시트 탭 이름"
    )

    # Google Service Account
    google_credentials_path: Optional[str] = Field(
        default=None,
        env="GOOGLE_CREDENTIALS_PATH",
        description="Service account JSON file path"
    )
    google_credentials_json: Optional[str] = Field(
        default=None,
        env="GOOGLE_CREDENTIALS_JSON",
        description="Service account JSON string"
    )

    # Default Uploader (Phase 1)
    default_uploader: str = Field(
        default="전용수",
        env="DEFAULT_UPLOADER",
        description="Default uploader name"
    )

    # File Upload Settings
    max_file_size_mb: int = Field(
        default=8,
        env="MAX_FILE_SIZE_MB",
        description="Maximum file size in MB"
    )

    # Logging
    log_level: str = Field(
        default="INFO",
        env="LOG_LEVEL",
        description="Logging level"
    )

    # Phase 2: AI/Vector DB (optional)
    gemini_api_key: Optional[str] = Field(
        default=None,
        env="GEMINI_API_KEY"
    )
    chroma_api_key: Optional[str] = Field(
        default=None,
        env="CHROMA_API_KEY"
    )
    chroma_tenant: Optional[str] = Field(
        default=None,
        env="CHROMA_TENANT"
    )
    chroma_database: Optional[str] = Field(
        default=None,
        env="CHROMA_DATABASE"
    )
    chroma_collection: Optional[str] = Field(
        default=None,
        env="CHROMA_COLLECTION"
    )

    @field_validator("google_credentials_json", mode="before")
    @classmethod
    def parse_credentials_json(cls, v):
        """Parse JSON string if provided"""
        if v and isinstance(v, str) and v.startswith("{"):
            try:
                return json.dumps(json.loads(v))
            except json.JSONDecodeError:
                return v
        return v

    @property
    def max_file_size_bytes(self) -> int:
        """Get max file size in bytes"""
        return self.max_file_size_mb * 1024 * 1024

    @property
    def google_credentials(self) -> dict:
        """Get Google credentials as dict"""
        if self.google_credentials_json:
            return json.loads(self.google_credentials_json)
        elif self.google_credentials_path:
            with open(self.google_credentials_path, 'r') as f:
                return json.load(f)
        else:
            raise ValueError("Either GOOGLE_CREDENTIALS_PATH or GOOGLE_CREDENTIALS_JSON must be set")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Singleton instance
settings = Settings()
