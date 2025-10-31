"""
Settings management using Pydantic Settings
"""
import json
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
import streamlit as st


def get_from_streamlit_secrets(key: str, default=None):
    """Get value from Streamlit secrets or return default"""
    try:
        return st.secrets.get(key, default)
    except:
        return default


class Settings(BaseSettings):
    """Application settings from environment variables or Streamlit secrets"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Google Drive
    google_drive_root_folder_id: str = Field(
        default="",
        description="Google Drive root folder ID"
    )

    # Google Sheets
    invoice_sheet_id: str = Field(
        default="",
        description="SCM 통합 시트 ID"
    )
    invoice_sheet_name: str = Field(
        default="scm통합",
        description="SCM 통합 시트 탭 이름"
    )
    dashboard_sheet_id: str = Field(
        default="",
        description="Dashboard 시트 ID"
    )
    dashboard_sheet_name: str = Field(
        default="dashboard",
        description="Dashboard 시트 탭 이름"
    )

    # Google Service Account
    google_credentials_path: Optional[str] = Field(
        default=None,
        description="Service account JSON file path"
    )
    google_credentials_json: Optional[str] = Field(
        default=None,
        description="Service account JSON string"
    )

    # Default Uploader (Phase 1)
    default_uploader: str = Field(
        default="Admin",
        description="Default uploader name"
    )

    # File Upload Settings
    max_file_size_mb: int = Field(
        default=8,
        description="Maximum file size in MB"
    )

    # Logging
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )

    # Phase 2: AI/Vector DB (optional)
    gemini_api_key: Optional[str] = Field(default=None)
    chroma_api_key: Optional[str] = Field(default=None)
    chroma_tenant: Optional[str] = Field(default=None)
    chroma_database: Optional[str] = Field(default=None)
    chroma_collection: Optional[str] = Field(default=None)

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
        import logging
        logger = logging.getLogger(__name__)

        # Try Streamlit secrets first (as a TOML section)
        # Check multiple possible key names
        possible_keys = ["GOOGLE_CREDENTIALS_JSON", "google_credentials_json", "google_sheets"]

        if hasattr(st, 'secrets'):
            for key in possible_keys:
                try:
                    if key in st.secrets:
                        logger.info(f"Found credentials key: {key}")
                        secrets_creds = st.secrets[key]
                        logger.info(f"Credentials type: {type(secrets_creds)}")

                        # Try to convert to dict
                        if isinstance(secrets_creds, dict):
                            result = dict(secrets_creds)
                            logger.info(f"Successfully loaded credentials from {key} as dict")
                            return result
                        elif isinstance(secrets_creds, str):
                            result = json.loads(secrets_creds)
                            logger.info(f"Successfully loaded credentials from {key} as JSON string")
                            return result
                        else:
                            # Try to convert to dict anyway (Streamlit secrets proxy)
                            try:
                                result = dict(secrets_creds)
                                logger.info(f"Successfully converted {key} to dict")
                                return result
                            except Exception as conv_error:
                                logger.warning(f"Could not convert {key} to dict: {conv_error}")
                except Exception as e:
                    logger.warning(f"Error accessing key '{key}': {e}", exc_info=True)

        # Try environment variables
        if self.google_credentials_json:
            return json.loads(self.google_credentials_json)
        elif self.google_credentials_path and os.path.exists(self.google_credentials_path):
            with open(self.google_credentials_path, 'r') as f:
                return json.load(f)
        else:
            # Debug info
            has_secrets = hasattr(st, 'secrets')
            secrets_keys = list(st.secrets.keys()) if has_secrets else []

            raise ValueError(
                f"Google credentials not found. "
                f"Streamlit secrets available: {has_secrets}, "
                f"Keys in secrets: {secrets_keys}. "
                f"Set GOOGLE_CREDENTIALS_JSON in Streamlit secrets "
                f"or GOOGLE_CREDENTIALS_PATH in environment"
            )

    def load_from_streamlit_secrets(self):
        """Load settings from Streamlit secrets"""
        try:
            if hasattr(st, 'secrets'):
                self.google_drive_root_folder_id = st.secrets.get(
                    "GOOGLE_DRIVE_ROOT_FOLDER_ID",
                    self.google_drive_root_folder_id
                )
                self.invoice_sheet_id = st.secrets.get(
                    "INVOICE_SHEET_ID",
                    self.invoice_sheet_id
                )
                self.dashboard_sheet_id = st.secrets.get(
                    "DASHBOARD_SHEET_ID",
                    self.dashboard_sheet_id
                )
                self.default_uploader = st.secrets.get(
                    "DEFAULT_UPLOADER",
                    self.default_uploader
                )
        except Exception:
            pass


def get_settings() -> Settings:
    """Get settings instance (cached in Streamlit session)"""
    if 'settings' not in st.session_state:
        settings = Settings()
        settings.load_from_streamlit_secrets()
        st.session_state.settings = settings
    return st.session_state.settings
