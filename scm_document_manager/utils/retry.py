"""
Retry utilities using tenacity
"""
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from core.exceptions import DriveAPIError, SheetsAPIError


def retry_on_api_error(max_attempts=3):
    """Decorator for retrying API calls"""
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((DriveAPIError, SheetsAPIError)),
        reraise=True
    )
