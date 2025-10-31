"""
Pydantic models for SCM Document Manager
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl
from .enums import DocType, UploadStatus, ShipmentCategory


class ShipmentInfo(BaseModel):
    """SCM 통합 시트에서 로드한 발송 정보"""
    invoice_no: str = Field(..., description="인보이스 번호")
    ticket_name: Optional[str] = Field(None, description="티켓명")
    carrier_name: str = Field(..., description="운송사")
    carrier_mode: str = Field(..., description="운송 모드")
    origin: str = Field(..., description="출발창고")
    destination: str = Field(..., description="도착창고")
    onboard_date: Optional[str] = Field(None, description="선적일")
    bl_no: Optional[str] = Field(None, description="BL 번호")
    status: Optional[str] = Field(None, description="상태")


class DocumentMetadata(BaseModel):
    """문서 메타데이터 (Dashboard 시트 스키마)"""
    # 기본 정보 (15개)
    upload_timestamp: datetime = Field(default_factory=datetime.utcnow, description="업로드 시간")
    shipment_id: str = Field(..., min_length=1, description="인보이스 번호")
    doc_type: str = Field(..., description="서류 종류")
    file_name: str = Field(..., description="파일명")
    drive_file_id: str = Field(..., description="Drive 파일 ID")
    drive_url: str = Field(..., description="Drive 공유 링크")
    drive_folder_id: str = Field(..., description="Drive 폴더 ID")
    uploader: str = Field(..., description="업로더")
    file_size_bytes: int = Field(ge=0, description="파일 크기 (bytes)")
    status: UploadStatus = Field(default=UploadStatus.UPLOADED, description="업로드 상태")
    error_message: Optional[str] = Field(None, description="에러 메시지")

    # SCM 자동 입력 (4개)
    carrier_name: Optional[str] = Field(None, description="운송사")
    carrier_mode: Optional[str] = Field(None, description="운송 모드")
    origin: Optional[str] = Field(None, description="출발창고")
    destination: Optional[str] = Field(None, description="도착창고")

    # Phase 2 대비 (3개)
    extracted_text: Optional[str] = Field(None, description="AI 추출 텍스트")
    extracted_json: Optional[str] = Field(None, description="구조화된 데이터 (JSON)")
    embedding_status: Optional[str] = Field(None, description="임베딩 여부")

    class Config:
        json_schema_extra = {
            "example": {
                "shipment_id": "TA254003250731",
                "doc_type": "Commercial Invoice",
                "file_name": "20251030_CIPL_TA254003250731.pdf",
                "uploader": "전용수",
                "file_size_bytes": 123456,
                "carrier_name": "KW",
                "carrier_mode": "특송",
                "origin": "태광KR",
                "destination": "AMZUS"
            }
        }


class FolderPath(BaseModel):
    """폴더 경로 정보"""
    category: ShipmentCategory = Field(..., description="발송 카테고리")
    folder_id: str = Field(..., description="Google Drive 폴더 ID")
    folder_name: str = Field(..., description="폴더 이름")
    folder_path: str = Field(..., description="전체 경로")


class UploadResult(BaseModel):
    """업로드 결과"""
    success: bool = Field(..., description="성공 여부")
    message: str = Field(..., description="결과 메시지")
    metadata: Optional[DocumentMetadata] = Field(None, description="문서 메타데이터")
    error: Optional[str] = Field(None, description="에러 상세")


class DocumentTypeConfig(BaseModel):
    """서류 종류 설정 (Google Sheets에서 관리)"""
    doc_type_name: str = Field(..., description="서류 종류 이름")
    doc_type_abbr: str = Field(..., description="약어 (파일명용)")
    doc_type_desc: Optional[str] = Field(None, description="설명")
    is_required: bool = Field(default=False, description="필수 여부")
    carrier_mode: Optional[str] = Field(None, description="적용 운송 모드")
    carrier_name: Optional[str] = Field(None, description="적용 운송사")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = Field(..., description="등록자")
