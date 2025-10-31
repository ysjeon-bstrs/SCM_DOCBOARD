"""
Enumerations for SCM Document Manager
"""
from enum import Enum


class DocType(str, Enum):
    """Document types"""
    CIPL = "Commercial Invoice + Packing List"
    BILL_OF_LADING = "Bill of Lading"
    EXPORT_DECLARATION = "수출신고필증"
    SETTLEMENT = "Settlement Statement"
    DUTY_TAX = "Duty Tax / Entry Summary"
    QUOTATION = "Quotation"
    CERTIFICATE_OF_ORIGIN = "Certificate of Origin"


class UploadStatus(str, Enum):
    """Upload status"""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    FAILED = "failed"


class ShipmentCategory(str, Enum):
    """Shipment categories for 2-tier folder structure"""
    SETTLEMENT = "00_SETTLEMENT"  # 정산
    KR_TO_3PL = "01_KR_TO_3PL"  # 한국 → 해외거점
    OUTBOUND_3PL = "02_3PL_OUTBOUND"  # 해외거점 → 출고
    KR_TO_CUSTOMER = "03_KR_TO_CUSTOMER"  # 한국 → 최종판매처


class CarrierMode(str, Enum):
    """Carrier modes"""
    EXPRESS = "특송"
    SEA = "해운"
    AIR = "항공"


# Warehouse mappings for automatic categorization
KR_WAREHOUSES = {"태광KR"}
OVERSEAS_3PL_WAREHOUSES = {"CJ서부US", "어크로스비US", "01-US", "02-US"}
CUSTOMER_WAREHOUSES = {"AMZUS", "SBSMY", "SBSPH", "SBSSG", "SBSTH", "REVEVN"}
