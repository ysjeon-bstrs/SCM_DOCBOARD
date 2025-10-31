# SCM Document Manager - Production Architecture v1.0

작성일: 2025-10-31
작성자: AI Assistant
목적: 확장 가능하고 유지보수 가능한 프로덕션급 문서 관리 시스템 아키텍처

---

## 🎯 설계 원칙

### 1. 확장성 (Extensibility)
- AI/벡터 DB 모듈을 플러그인 방식으로 추가 가능
- Phase 1: 파일 관리 → Phase 2: AI 분석 → Phase 3: 시계열 분석

### 2. 관찰 가능성 (Observability)
- 모든 함수 호출/에러를 추적 가능한 구조화된 로깅
- 타입 에러, 런타임 에러 즉시 감지 및 컨텍스트 제공

### 3. 견고성 (Robustness)
- API 호출 실패 시 자동 재시도 (exponential backoff)
- 타입 검증 (Pydantic)
- 방어적 프로그래밍

### 4. 테스트 가능성 (Testability)
- 의존성 주입 패턴
- Mock 가능한 인터페이스
- 유닛/통합 테스트 커버리지

---

## 📁 프로젝트 구조

```
scm_document_manager/
├── app.py                          # Streamlit 메인 앱
├── requirements.txt
├── pytest.ini
├── .env.example
├── README.md
│
├── config/
│   ├── __init__.py
│   ├── settings.py                 # 환경변수 로드 (Pydantic Settings)
│   └── logging_config.py           # 로깅 설정 (structlog)
│
├── core/
│   ├── __init__.py
│   ├── models.py                   # Pydantic 데이터 모델
│   ├── enums.py                    # Enum 정의
│   ├── exceptions.py               # 커스텀 예외
│   └── interfaces.py               # 추상 인터페이스 (ABC)
│
├── services/
│   ├── __init__.py
│   ├── drive_service.py            # Google Drive 연동
│   ├── sheets_service.py           # Google Sheets 연동
│   ├── document_service.py         # 문서 처리 오케스트레이션
│   │
│   ├── extractors/                 # Phase 2: 문서 추출
│   │   ├── __init__.py
│   │   ├── base.py                 # 추상 클래스
│   │   ├── pdf_extractor.py
│   │   └── excel_extractor.py
│   │
│   └── ai/                         # Phase 2: AI/벡터 DB
│       ├── __init__.py
│       ├── embedder.py             # 임베딩 생성
│       ├── vector_store.py         # ChromaDB 연동
│       └── qa_engine.py            # Gemini Q&A
│
├── utils/
│   ├── __init__.py
│   ├── retry.py                    # 재시도 데코레이터
│   ├── validators.py               # 데이터 검증
│   └── file_utils.py               # 파일 처리 유틸
│
├── ui/
│   ├── __init__.py
│   ├── pages/
│   │   ├── 1_📤_Upload.py
│   │   ├── 2_📊_Dashboard.py
│   │   └── 3_🤖_AI_Chat.py         # Phase 2
│   └── components/
│       ├── __init__.py
│       ├── upload_form.py
│       └── status_table.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # pytest fixtures
│   ├── unit/
│   │   ├── test_drive_service.py
│   │   ├── test_sheets_service.py
│   │   └── test_validators.py
│   ├── integration/
│   │   ├── test_upload_flow.py
│   │   └── test_search_flow.py
│   └── fixtures/
│       └── sample_data.json
│
└── scripts/
    ├── setup_google_cloud.sh       # GCP 설정 스크립트
    └── init_database.py            # DB 초기화
```

---

## 🔧 기술 스택 상세

### Phase 1 (MVP - 2-3주)

| 계층 | 기술 | 용도 |
|------|------|------|
| **Frontend** | Streamlit 1.30+ | 빠른 프로토타이핑 |
| **Type Safety** | Pydantic 2.5+ | 데이터 검증 및 타입 안전성 |
| **Logging** | structlog | 구조화된 로그 (JSON) |
| **File Storage** | Google Drive API | 파일 저장소 |
| **Metadata DB** | Google Sheets API | 인덱스 (Phase 1) |
| **Retry Logic** | tenacity | API 재시도 |
| **Testing** | pytest + pytest-mock | 유닛/통합 테스트 |
| **Env Management** | python-dotenv | 환경변수 관리 |

### Phase 2 (AI 확장 - 2-3주)

| 계층 | 기술 | 용도 |
|------|------|------|
| **Vector DB** | ChromaDB Cloud | 임베딩 저장 (managed) |
| **Embeddings** | sentence-transformers | 한국어 임베딩 |
| **LLM** | Google Gemini 2.5 Flash | 문서 분석 & Q&A |
| **Document Parsing** | pdfplumber + pytesseract | PDF 텍스트 추출 |

### Phase 3 (고도화 - 1개월)

| 계층 | 기술 | 용도 |
|------|------|------|
| **Database** | Supabase PostgreSQL | Sheets → 관계형 DB 마이그레이션 |
| **Time Series** | Pandas + Plotly | 시계열 분석 |
| **Background Jobs** | APScheduler | 주기적 작업 |

---

## 📊 데이터 모델 설계

### Phase 1: Google Sheets 스키마

**Sheet: `dashboard`**

```
컬럼 (15개):
1. upload_timestamp      # ISO 8601 형식
2. shipment_id          # "인보이스 번호" (예: TA254003250731)
3. doc_type             # 서류 종류
4. file_name            # 원본 파일명
5. drive_file_id        # Google Drive 파일 ID
6. drive_url            # 공유 링크
7. drive_folder_id      # 부모 폴더 ID
8. uploader             # 업로더 이름
9. file_size_bytes      # 파일 크기
10. status              # uploaded | processing | failed
11. error_message       # 에러 메시지 (있는 경우)
12. carrier_name        # 운송사
13. carrier_mode        # 운송 모드
14. origin              # 출발지
15. destination         # 도착지
```

### Pydantic 모델

```python
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from enum import Enum

class DocType(str, Enum):
    COMMERCIAL_INVOICE = "Commercial Invoice"
    BILL_OF_LADING = "Bill of Lading"
    PACKING_LIST = "Packing List"
    SETTLEMENT = "Settlement Statement"
    CUSTOMS = "Customs Declaration"
    EXPORT_DECLARATION = "수출신고필증"
    DUTY_TAX = "Duty Tax"
    QUOTATION = "Quotation"

class UploadStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    FAILED = "failed"

class DocumentMetadata(BaseModel):
    """문서 메타데이터"""
    upload_timestamp: datetime = Field(default_factory=datetime.utcnow)
    shipment_id: str = Field(..., min_length=1, description="인보이스 번호")
    doc_type: DocType
    file_name: str
    drive_file_id: str
    drive_url: HttpUrl
    drive_folder_id: str
    uploader: str
    file_size_bytes: int = Field(ge=0)
    status: UploadStatus = UploadStatus.UPLOADED
    error_message: str | None = None

    # SCM 데이터 (옵션)
    carrier_name: str | None = None
    carrier_mode: str | None = None
    origin: str | None = None
    destination: str | None = None

class ShipmentInfo(BaseModel):
    """SCM 통합 시트에서 로드한 발송 정보"""
    invoice_no: str
    carrier_name: str
    carrier_mode: str
    onboard_date: str | None
    origin: str
    destination: str
    bl_no: str | None
    status: str
```

---

## 🔐 에러 처리 전략

### 1. 계층화된 예외

```python
# core/exceptions.py

class SCMDocumentError(Exception):
    """Base exception"""
    pass

class DriveAPIError(SCMDocumentError):
    """Google Drive API 에러"""
    pass

class SheetsAPIError(SCMDocumentError):
    """Google Sheets API 에러"""
    pass

class DocumentParsingError(SCMDocumentError):
    """문서 파싱 에러"""
    pass

class ValidationError(SCMDocumentError):
    """데이터 검증 에러"""
    pass
```

### 2. 재시도 로직

```python
# utils/retry.py

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
import structlog

logger = structlog.get_logger()

def retry_on_api_error(max_attempts=3):
    """API 호출 재시도 데코레이터"""
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((DriveAPIError, SheetsAPIError)),
        before_sleep=lambda retry_state: logger.warning(
            "api_retry",
            attempt=retry_state.attempt_number,
            wait_seconds=retry_state.next_action.sleep
        )
    )
```

### 3. 구조화된 로깅

```python
# config/logging_config.py

import structlog
import logging
import sys

def setup_logging(log_level="INFO"):
    """
    구조화된 로깅 설정
    - JSON 포맷 (프로덕션)
    - 컬러 출력 (로컬 개발)
    """
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if is_production()
            else structlog.dev.ConsoleRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level)
    )

# 사용 예시
logger = structlog.get_logger()
logger.info(
    "file_uploaded",
    shipment_id="TA254003250731",
    file_name="invoice.pdf",
    file_size_bytes=123456,
    drive_file_id="abc123"
)
# 출력 (JSON):
# {"event": "file_uploaded", "shipment_id": "TA254003250731",
#  "file_name": "invoice.pdf", "timestamp": "2025-10-31T12:00:00Z"}
```

---

## 🧪 테스트 전략

### 1. 유닛 테스트 (pytest)

```python
# tests/unit/test_validators.py

import pytest
from core.models import DocumentMetadata, DocType
from pydantic import ValidationError

def test_document_metadata_valid():
    """정상적인 메타데이터 생성"""
    metadata = DocumentMetadata(
        shipment_id="TA254003250731",
        doc_type=DocType.COMMERCIAL_INVOICE,
        file_name="invoice.pdf",
        drive_file_id="abc123",
        drive_url="https://drive.google.com/file/d/abc123",
        drive_folder_id="folder123",
        uploader="전용수",
        file_size_bytes=123456
    )
    assert metadata.shipment_id == "TA254003250731"

def test_document_metadata_invalid_shipment_id():
    """빈 shipment_id 거부"""
    with pytest.raises(ValidationError):
        DocumentMetadata(
            shipment_id="",  # 빈 문자열
            doc_type=DocType.COMMERCIAL_INVOICE,
            # ... 나머지 필드
        )
```

### 2. 통합 테스트 (Mock 사용)

```python
# tests/integration/test_upload_flow.py

import pytest
from unittest.mock import MagicMock, patch
from services.document_service import DocumentService

@pytest.fixture
def mock_drive_service():
    """Drive Service Mock"""
    service = MagicMock()
    service.upload_file.return_value = {
        "file_id": "mock_file_id",
        "drive_url": "https://drive.google.com/file/d/mock_file_id"
    }
    return service

def test_upload_document_success(mock_drive_service):
    """문서 업로드 성공 시나리오"""
    doc_service = DocumentService(
        drive_service=mock_drive_service,
        sheets_service=MagicMock()
    )

    result = doc_service.upload_document(
        file_bytes=b"fake pdf content",
        shipment_id="TEST001",
        doc_type=DocType.COMMERCIAL_INVOICE,
        uploader="테스터"
    )

    assert result.status == "uploaded"
    assert result.drive_file_id == "mock_file_id"
    mock_drive_service.upload_file.assert_called_once()
```

### 3. Fixture 관리

```python
# tests/conftest.py

import pytest
from pathlib import Path

@pytest.fixture
def sample_pdf_path():
    """샘플 PDF 파일 경로"""
    return Path("samples/documents/sample_(CIPL)_MV02110604202510-01_CJ_BOOSTERS_2025-10-01.pdf")

@pytest.fixture
def sample_scm_data():
    """SCM 통합 시트 샘플 데이터"""
    return [
        {
            "invoice_no": "TA254003250731",
            "carrier_name": "KW",
            "carrier_mode": "특송",
            "origin": "태광KR",
            "destination": "AMZUS"
        }
    ]
```

---

## 🚀 Phase별 개발 계획

### Phase 1: Core File Management (2-3주)

**Week 1: 기반 구축**
- [ ] 프로젝트 구조 생성
- [ ] Pydantic 모델 정의
- [ ] 로깅 설정
- [ ] Google Drive/Sheets 연동
- [ ] 재시도 로직 구현

**Week 2: 업로드 플로우**
- [ ] 파일 업로드 UI
- [ ] 폴더 자동 생성 (`/Shipments/{shipment_id}/{doc_type}/`)
- [ ] Sheets 인덱싱
- [ ] 에러 처리

**Week 3: 대시보드 & 테스트**
- [ ] 누락 서류 체크 매트릭스
- [ ] 업로드 로그 페이지
- [ ] 유닛 테스트 (커버리지 80%+)
- [ ] 통합 테스트
- [ ] 배포 (Streamlit Cloud)

### Phase 2: AI Integration (2-3주)

**Week 4-5: 문서 추출 & 임베딩**
- [ ] PDF/Excel 텍스트 추출
- [ ] Gemini API로 구조화된 데이터 추출
- [ ] sentence-transformers 임베딩
- [ ] ChromaDB Cloud 연동

**Week 6: Q&A 시스템**
- [ ] RAG 파이프라인 구현
- [ ] AI Chat UI
- [ ] 출처 표시 기능
- [ ] 성능 최적화

### Phase 3: Analytics & Scaling (1개월)

- [ ] Supabase 마이그레이션
- [ ] 시계열 분석 대시보드
- [ ] 비용 집계 & 트렌드
- [ ] 알림 시스템 (이메일/Slack)

---

## 📈 모니터링 & 관찰 가능성

### 1. 로그 구조

모든 로그는 다음 필드 포함:

```json
{
  "timestamp": "2025-10-31T12:00:00Z",
  "level": "info",
  "event": "file_uploaded",
  "shipment_id": "TA254003250731",
  "doc_type": "Commercial Invoice",
  "file_size_bytes": 123456,
  "duration_ms": 450,
  "user": "전용수"
}
```

### 2. 에러 로그

```json
{
  "timestamp": "2025-10-31T12:05:00Z",
  "level": "error",
  "event": "drive_upload_failed",
  "shipment_id": "TA254003250731",
  "error_type": "DriveAPIError",
  "error_message": "Quota exceeded",
  "traceback": "...",
  "retry_attempt": 2
}
```

### 3. 성능 메트릭

```python
import time
import structlog

logger = structlog.get_logger()

def track_performance(func):
    """함수 실행 시간 추적"""
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
            duration_ms = (time.time() - start) * 1000
            logger.info(
                f"{func.__name__}_completed",
                duration_ms=round(duration_ms, 2)
            )
            return result
        except Exception as e:
            duration_ms = (time.time() - start) * 1000
            logger.error(
                f"{func.__name__}_failed",
                duration_ms=round(duration_ms, 2),
                error=str(e)
            )
            raise
    return wrapper
```

---

## 🔒 보안 고려사항

### 1. 환경변수 관리

```python
# config/settings.py

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """환경변수 설정"""

    # Google Drive
    google_drive_root_folder_id: str = Field(..., env="GOOGLE_DRIVE_ROOT_FOLDER_ID")
    google_credentials_json: str = Field(..., env="GOOGLE_CREDENTIALS_JSON")

    # Google Sheets
    invoice_sheet_id: str = Field(..., env="INVOICE_SHEET_ID")
    invoice_sheet_name: str = Field(default="dashboard", env="INVOICE_SHEET_NAME")

    # Gemini API (Phase 2)
    gemini_api_key: str | None = Field(default=None, env="GEMINI_API_KEY")

    # ChromaDB (Phase 2)
    chroma_api_key: str | None = Field(default=None, env="CHROMA_API_KEY")
    chroma_tenant: str | None = Field(default=None, env="CHROMA_TENANT")

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# 싱글톤
settings = Settings()
```

### 2. API 키 보안

- ✅ `.env` 파일은 `.gitignore`에 포함
- ✅ Streamlit Cloud Secrets 사용
- ✅ 서비스 계정 JSON은 환경변수로 전달
- ❌ 코드에 하드코딩 절대 금지

---

## 🎯 의사결정 기록

### Q1: Google Sheets vs PostgreSQL?
**결정**: Phase 1은 Sheets, Phase 3에서 Supabase로 마이그레이션
**이유**:
- Sheets: 빠른 MVP, 설정 간단
- Supabase: 확장성, JOIN 지원, 트랜잭션

### Q2: ChromaDB 로컬 vs Cloud?
**결정**: ChromaDB Cloud (managed)
**이유**:
- 로컬: Streamlit Cloud에서 persistence 문제
- Cloud: 관리 불필요, 안정적

### Q3: 임베딩 모델?
**결정**: sentence-transformers `paraphrase-multilingual-MiniLM-L12-v2`
**이유**:
- 한국어 지원
- 무료
- 384차원 (ChromaDB 효율적)

### Q4: 폴더 구조에 Settlements 폴더?
**결정**: Phase 1은 `/Shipments/` 만, Settlements는 논리적 그룹핑
**이유**:
- Shortcut 로직 복잡함
- MVP 범위 축소
- metadata로 그룹핑 충분

---

## 📋 체크리스트

### 개발 시작 전

- [x] 샘플 파일 확인
- [x] Google Drive 루트 폴더 ID 확인
- [x] Google Sheets ID 확인
- [ ] 서비스 계정 JSON 준비
- [ ] Gemini API 키 확인
- [ ] ChromaDB Cloud 계정 생성 (Phase 2)

### Phase 1 완료 조건

- [ ] 파일 업로드 성공률 99%+
- [ ] Sheets 인덱싱 성공률 99%+
- [ ] 에러 발생 시 상세 로그 기록
- [ ] 유닛 테스트 커버리지 80%+
- [ ] 실제 파일로 E2E 테스트 통과

---

**다음 단계**: 추가 필요 정보 확인 문서 작성
