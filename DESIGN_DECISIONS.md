# SCM Document Manager - 설계 결정사항 분석

작성일: 2025-10-31
목적: 사용자 답변 분석 및 구현 방향 확정

---

## ✅ 확정된 사항 (즉시 구현 가능)

### 1. 인증 & 환경
- ✅ **서비스 계정 JSON**: 있음 (Streamlit Secrets 등록됨)
- ✅ **배포**: Streamlit Cloud
- ✅ **업로더 식별**: Phase 1은 간단한 방식, Phase 2에서 Google OAuth
- ✅ **에러 알림**: Streamlit 화면만
- ✅ **파일 크기**: 8MB 제한
- ✅ **다국어**: 한/영 혼용

### 2. Dashboard 시트 스키마
**확정 컬럼 (18개):**
```
기본 (15개):
1. upload_timestamp
2. shipment_id
3. doc_type
4. file_name
5. drive_file_id
6. drive_url
7. drive_folder_id
8. uploader
9. file_size_bytes
10. status
11. error_message
12. carrier_name
13. carrier_mode
14. origin
15. destination

Phase 2 대비 (3개):
16. extracted_text
17. extracted_json
18. embedding_status
```

### 3. SCM 시트 매핑
```python
{
    "인보이스 번호": "shipment_id",
    "티켓명": "ticket_name",  # 추가
    "carrier_name": "carrier_name",
    "carrier_mode": "carrier_mode",
    "출발창고": "origin",
    "도착창고": "destination"
}
```

**UX 플로우:**
```
사용자 shipment_id 입력 → SCM 시트 검색 →
검색 결과 목록 표시 → 사용자 선택 →
carrier/origin/destination 자동 입력
```

### 4. 파일 중복 처리
- ✅ **사용자에게 선택권**
  - 덮어쓰기 / 버전 추가 / 취소 선택 가능

### 5. 날짜 형식
- ✅ **YYYYMMDD → datetime 변환**

---

## ⚠️ 복잡한 요구사항 (설계 조정 필요)

### 🔴 **1. Q3: 폴더 구조 (매우 복잡!)**

**사용자 요구사항:**
```
/루트/
├── 00/                           # 정산 폴더
│   └── {carrier_name}/           # 예: KW
│       └── {YYYYMM}/             # 예: 202509
│           └── 파일들
│
├── 01/                           # 한국 → 해외거점 발송
│   └── {생성일}_{invoice}_{mode}_{carrier}/
│       └── 파일들
│       # 예: 250829_TA717001250829_SEA_CJ
│
├── 02/                           # 해외거점 → 출고
│   └── {창고번호}-{국가}/        # 예: 01-US
│       └── {생성일}_{invoice}_{carrier}/
│           └── 파일들
│           # 예: 251001_MV11050306202510-03_UPS
│
└── 03/                           # 한국 → 최종판매처 직접발송
    └── {판매처번호}_{판매처명}/  # 예: 01_AMAZON
        └── {생성일}_{invoice}_{mode}_{destination}/
            └── 파일들
            # 예: 251024_MV02050202202510-11_특송_AMZUS
```

**자동 분류 로직 필요:**
```python
def determine_folder_category(origin, destination, doc_type):
    """
    출발창고, 도착창고, 서류종류를 보고 폴더 카테고리 결정
    """
    if doc_type == "정산서":
        return "00"  # 정산
    elif origin == "태광KR" and destination in ["CJ서부US", "어크로스비US", ...]:
        return "01"  # 한국 → 해외거점
    elif origin in ["CJ서부US", "어크로스비US", ...]:
        return "02"  # 해외거점 → 출고
    elif origin == "태광KR" and destination in ["AMZUS", "SBSMY", ...]:
        return "03"  # 한국 → 최종판매처
    else:
        return "99"  # 기타 (fallback)
```

**문제점:**
1. **복잡도가 매우 높음** → 테스트/유지보수 어려움
2. **창고 목록이 하드코딩**되어야 함 → 확장성 낮음
3. **폴더명 생성 규칙이 카테고리마다 다름** → 버그 위험

**제안 (간소화 옵션):**

#### 옵션 A: 2-tier 구조 (추천)
```
/{shipment_category}/
  └── {shipment_id}/
      └── {doc_type}/
          └── 파일들

예시:
/00_SETTLEMENT/KW_202509/정산서/
/01_KR_TO_3PL/TA717001250829/BL/
/02_3PL_OUTBOUND/MV11050306202510-03/Invoice/
/03_KR_TO_CUSTOMER/MV02050202202510-11/정산서/
```

**장점:**
- 구조 단순화
- 카테고리는 자동 분류, 폴더는 shipment_id 기준
- 확장 용이

#### 옵션 B: Metadata 기반 (Phase 2)
```
/Shipments/{shipment_id}/{doc_type}/
  └── 파일들

카테고리/폴더 구조는 시트에서 논리적으로만 관리
Drive에서는 단순 구조 유지
```

**장점:**
- Drive 구조 극도로 단순
- 유연성 최대
- AI 검색으로 카테고리 무관하게 찾기 가능

#### 옵션 C: 사용자 요구사항 그대로 (복잡)
```
현재 요구사항 그대로 구현
→ 개발 시간: +2-3일
→ 테스트 복잡도: 매우 높음
→ 버그 가능성: 높음
```

**질문: 어느 옵션을 선호하시나요?**
- [ ] A: 2-tier 구조 (단순, 빠름)
- [ ] B: Metadata 기반 (가장 단순)
- [ ] C: 요구사항 그대로 (복잡, 시간 소요)

---

### 🟡 **2. Q2: 서류 종류 동적 관리**

**요구사항:**
> 최초 업로드 시 서류 종류 - 필수/비필수 - 서류 설명을 등록
> AI가 서류 설명과 내용을 토대로 답변

**구현 방식 제안:**

#### 방식 A: 별도 관리 시트 생성
```
Google Sheets: "document_types" 시트

컬럼:
- doc_type_id (자동생성)
- doc_type_name (예: "정산서")
- doc_type_abbr (예: "SETTLE")
- doc_type_desc (예: "운송사 월별 비용 정산 서류")
- is_required (TRUE/FALSE)
- carrier_mode (특송/해운/항공)
- carrier_name (KW/DHL/...)
- created_at
- created_by
```

**업로드 플로우:**
```
1. 사용자 파일 선택
2. shipment_id 입력 → SCM 검색 → 선택
3. 서류 종류 선택:
   - 기존 서류 종류 드롭다운
   - 또는 "새 서류 종류 등록" 버튼 클릭
4. 새 등록 시:
   - 서류 이름 입력
   - 약어 입력
   - 설명 입력
   - 필수 여부 체크
   - → document_types 시트에 저장
5. 업로드 진행
```

#### 방식 B: JSON 파일로 관리 (로컬)
```python
# config/document_types.json
{
  "CIPL": {
    "name": "Commercial Invoice + Packing List",
    "abbr": "CIPL",
    "desc": "상업 송장 및 포장 리스트",
    "required": ["특송", "해운"],
    "optional": ["항공"]
  },
  "SETTLE": {
    "name": "정산서",
    "abbr": "SETTLE",
    "desc": "운송사 비용 정산 서류",
    "required": [],
    "optional": ["특송", "해운", "항공"]
  }
}
```

**질문: 어느 방식을 선호하시나요?**
- [ ] A: Google Sheets (추천 - 웹에서 관리 가능)
- [ ] B: JSON 파일 (코드 배포 필요)

---

### 🟡 **3. Q5: 업로더 식별 (OAuth)**

**요구사항:**
> Google OAuth (나중에)

**Phase 1 임시 방안:**

#### 옵션 1: 환경변수 (가장 간단)
```python
# Streamlit Secrets
default_uploader = "전용수"

# 모든 업로드는 이 이름으로 기록
```

#### 옵션 2: 세션 기반 이름 입력
```python
# 앱 실행 시 1회만 이름 입력
if "uploader_name" not in st.session_state:
    st.session_state.uploader_name = st.text_input("이름을 입력하세요")
```

#### 옵션 3: 업로드 시마다 이름 선택
```python
# 업로드 폼에 드롭다운
uploader = st.selectbox("업로더", ["전용수", "유진", "재현"])
```

**질문: Phase 1에서 어떻게 할까요?**
- [ ] 옵션 1: 환경변수 (가장 빠름)
- [ ] 옵션 2: 세션 입력 (중간)
- [ ] 옵션 3: 매번 선택 (가장 정확)

---

## 📊 복잡도 분석

### 현재 요구사항 그대로 구현 시:

| 기능 | 복잡도 | 개발 시간 | 테스트 시간 |
|------|--------|----------|------------|
| 폴더 자동 분류 (00/01/02/03) | ⭐⭐⭐⭐⭐ | 1.5일 | 1일 |
| 동적 서류 종류 관리 | ⭐⭐⭐ | 0.5일 | 0.5일 |
| SCM 시트 검색/선택 | ⭐⭐ | 0.3일 | 0.2일 |
| 파일명 규칙 (약어) | ⭐⭐ | 0.2일 | 0.1일 |
| Dashboard 시트 18컬럼 | ⭐⭐ | 0.3일 | 0.1일 |
| 파일 중복 선택권 | ⭐⭐⭐ | 0.4일 | 0.2일 |
| 기본 업로드 플로우 | ⭐⭐ | 0.5일 | 0.2일 |

**총 예상 시간: 3.7일 개발 + 2.3일 테스트 = 6일**

### 간소화 옵션 적용 시:

| 기능 | 복잡도 | 개발 시간 | 테스트 시간 |
|------|--------|----------|------------|
| 폴더 2-tier 구조 (옵션 A) | ⭐⭐ | 0.4일 | 0.3일 |
| 서류 종류 Sheets 관리 | ⭐⭐ | 0.4일 | 0.2일 |
| SCM 시트 검색/선택 | ⭐⭐ | 0.3일 | 0.2일 |
| 파일명 규칙 (약어) | ⭐⭐ | 0.2일 | 0.1일 |
| Dashboard 시트 18컬럼 | ⭐⭐ | 0.3일 | 0.1일 |
| 파일 중복 선택권 | ⭐⭐⭐ | 0.4일 | 0.2일 |
| 기본 업로드 플로우 | ⭐⭐ | 0.5일 | 0.2일 |

**총 예상 시간: 2.5일 개발 + 1.3일 테스트 = 3.8일**

**시간 절감: 2.2일 (37%)**

---

## 🎯 최종 권장사항

### 🚀 **빠른 시작 (추천)**

**Phase 1a (1-2일):**
- 폴더 구조: 옵션 B (Metadata 기반, 가장 단순)
- 서류 종류: 7개 하드코딩 시작
- 업로더: 환경변수
- 중복 처리: 덮어쓰기만

**Phase 1b (2-3일):**
- 폴더 구조: 옵션 A (2-tier)
- 서류 종류: Sheets 관리
- 업로더: 세션 입력
- 중복 처리: 선택권

**Phase 1c (완전 구현, 4-6일):**
- 폴더 구조: 요구사항 그대로 (00/01/02/03)
- 모든 기능 완전 구현

### 💡 **제 제안**

**"Phase 1a → 1b → 1c" 순서로 진행:**

1. **Phase 1a (오늘-내일)**
   - 가장 단순한 버전
   - 바로 테스트 가능
   - 피드백 받기

2. **Phase 1b (2-3일 후)**
   - 사용자 피드백 반영
   - 기능 점진적 확장

3. **Phase 1c (필요 시)**
   - 복잡한 폴더 구조 구현
   - 프로덕션 완성

---

## 🤔 **당신의 결정**

**질문 3가지:**

**Q_FOLDER: 폴더 구조**
- [ ] A: 2-tier (단순, 빠름) - 추천
- [ ] B: Metadata 기반 (가장 단순) - 초추천
- [ ] C: 요구사항 그대로 (복잡)

**Q_DOCTYPE: 서류 종류 관리**
- [ ] A: Google Sheets (추천)
- [ ] B: JSON 파일

**Q_UPLOADER: Phase 1 업로더**
- [ ] 1: 환경변수 (빠름)
- [ ] 2: 세션 입력 (중간)
- [ ] 3: 매번 선택 (정확)

**또는:**
- [ ] "일단 가장 빠른 것(1a)으로 시작해줘"
- [ ] "시간 걸려도 요구사항 그대로 해줘"

---

## 📝 다음 단계

**답변 후:**
1. 제가 선택한 옵션으로 구현 시작
2. 2시간 내 첫 버전 완성
3. 실제 파일로 테스트

**지금 결정해주세요!** 🚀
