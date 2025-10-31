"""
Custom exceptions for SCM Document Manager
"""


class SCMDocumentError(Exception):
    """Base exception for all SCM Document Manager errors"""
    pass


class DriveAPIError(SCMDocumentError):
    """Google Drive API related errors"""
    pass


class SheetsAPIError(SCMDocumentError):
    """Google Sheets API related errors"""
    pass


class DocumentParsingError(SCMDocumentError):
    """Document parsing/extraction errors"""
    pass


class ValidationError(SCMDocumentError):
    """Data validation errors"""
    pass


class FolderCreationError(DriveAPIError):
    """Folder creation failed"""
    pass


class FileUploadError(DriveAPIError):
    """File upload failed"""
    pass
