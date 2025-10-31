"""
Folder categorization and path utilities
"""
from core.enums import (
    ShipmentCategory,
    KR_WAREHOUSES,
    OVERSEAS_3PL_WAREHOUSES,
    CUSTOMER_WAREHOUSES
)
from config.logging_config import get_logger

logger = get_logger(__name__)


def determine_shipment_category(
    origin: str,
    destination: str,
    doc_type: str
) -> ShipmentCategory:
    """
    Determine shipment category based on origin, destination, and document type

    Args:
        origin: 출발창고
        destination: 도착창고
        doc_type: 서류 종류

    Returns:
        ShipmentCategory
    """
    # 정산서는 무조건 00_SETTLEMENT
    if "정산" in doc_type or "settlement" in doc_type.lower():
        return ShipmentCategory.SETTLEMENT

    # 한국 → 해외거점 (태광KR → CJ서부US 등)
    if origin in KR_WAREHOUSES and destination in OVERSEAS_3PL_WAREHOUSES:
        return ShipmentCategory.KR_TO_3PL

    # 해외거점 → 출고 (CJ서부US → ...)
    if origin in OVERSEAS_3PL_WAREHOUSES:
        return ShipmentCategory.OUTBOUND_3PL

    # 한국 → 최종판매처 (태광KR → AMZUS 등)
    if origin in KR_WAREHOUSES and destination in CUSTOMER_WAREHOUSES:
        return ShipmentCategory.KR_TO_CUSTOMER

    # 기본값: 한국 → 최종판매처로 처리
    logger.warning(
        f"Unknown warehouse combination: {origin} → {destination}. "
        f"Defaulting to {ShipmentCategory.KR_TO_CUSTOMER}"
    )
    return ShipmentCategory.KR_TO_CUSTOMER


def build_folder_path(
    category: ShipmentCategory,
    shipment_id: str,
    doc_type: str
) -> str:
    """
    Build folder path in 2-tier structure

    Structure:
        /{category}/{shipment_id}/{doc_type}/

    Example:
        /01_KR_TO_3PL/TA717001250829/Bill of Lading/

    Args:
        category: Shipment category
        shipment_id: Invoice number
        doc_type: Document type

    Returns:
        Folder path string
    """
    return f"{category.value}/{shipment_id}/{doc_type}"


def build_file_name(
    upload_date: str,
    doc_type_abbr: str,
    original_name: str
) -> str:
    """
    Build standardized file name

    Format: YYYYMMDD_{abbr}_{original_name}.{ext}
    Example: 20251030_CIPL_invoice_001.pdf

    Args:
        upload_date: Upload date (YYYYMMDD)
        doc_type_abbr: Document type abbreviation
        original_name: Original file name

    Returns:
        Standardized file name
    """
    return f"{upload_date}_{doc_type_abbr}_{original_name}"
