# SCM Document Manager - 개발 시작 전 필수 정보

작성일: 2025-10-31
목적: 꼼꼼한 개발 준비를 위한 필수 정보 수집

---

## ✅ 확인된 정보

### 1. Google 리소스
- ✅ Drive 루트 폴더 ID: `1zI9kD1WC-iXKDo-_ILjsb8PDBFhQMLl9`
- ✅ 인덱스 시트 ID: `1lMcYrjTOePfXTQIb6fMqluLAXyXuhTY3zAbzdeEehvs`
- ✅ 인덱스 시트 이름: `dashboard`
- ✅ SCM 통합 시트 ID: `1RYjKW2UDJ2kWJLAqQH26eqx2-r9Xb0_qE_hfwu9WIj8`
- ✅ SCM 통합 시트 탭: `scm통합`

### 2. API 키
- ✅ Gemini API Key: 설정 완료
- ✅ ChromaDB API Key: 설정 완료
- ✅ ChromaDB Tenant: 설정 완료

### 3. 샘플 데이터
- ✅ SCM 통합 CSV (46KB, 41개 컬럼)
- ✅ 샘플 문서 14개 (PDF, CSV)

---

## ❓ 추가 필요 정보

### 📌 **우선순위 1: 즉시 답변 필요**

#### Q1. Google 서비스 계정 JSON
현재 `.env`에는 API 키만 있는데, Google Drive/Sheets API는 **서비스 계정 JSON**이 필요합니다.

**선택지:**
- [ ] A. 이미 있음 → 파일 경로 알려주세요: _______________
- [ ] B. 없음 → 생성 방법 가이드 필요
- [ ] C. 다른 인증 방법 사용 (OAuth 2.0)

**예상 파일 형식:**
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  ...
}
```

#### Q2. 서류 종류 정의 확정

**현재 샘플에서 발견된 서류 종류:**
1. ✅ Commercial Invoice + Packing List (CIPL)
2. ✅ Bill of Lading (BL)
3. ✅ 수출신고필증
4. ✅ Settlement Statement (정산서)
5. ✅ Duty Tax / Entry Summary
6. ✅ Quotation (견적서)
7. ✅ Certificate of Origin (원산지증명서)
8. ❓ 기타...

**질문:**
- [ ] 위 7개로 충분한가요?
- [ ] 추가 서류 종류: _______________
- [ ] 필수 서류 정의 필요? (예: 모든 발송 건에 BL, CIPL 필수)

**필수 서류 매핑 (선택 사항):**
```yaml
특송 (KW, DHL, FedEx, UPS):
  필수:
    - Commercial Invoice
    - 수출신고필증
  선택:
    - Settlement Statement

해상 (선박):
  필수:
    - Commercial Invoice
    - Bill of Lading
    - 수출신고필증
  선택:
    - Certificate of Origin
    - Settlement Statement
```

이렇게 정의할까요? (Y/N): _______________

#### Q3. 폴더 구조 최종 확정

**제안 1: 심플 (추천)**
```
/Shipments/
  └── TA254003250731/
      ├── Commercial Invoice/
      │   └── 20251030_Commercial_Invoice_sample.pdf
      ├── Bill of Lading/
      ├── 수출신고필증/
      └── Settlement Statement/
```

**제안 2: 날짜별 그룹핑**
```
/Shipments/
  └── 2025/
      └── 10/
          └── TA254003250731/
              └── ...
```

**제안 3: 운송사별 그룹핑**
```
/Shipments/
  └── KW/
      └── TA254003250731/
          └── ...
```

**선택**: 제안 ____ 번 (또는 다른 구조 설명): _______________

#### Q4. 파일명 규칙 확정

**현재 기획서:**
```
YYYYMMDD_[서류종류]_[원본파일명].[확장자]
```

**예시:**
```
20251030_Commercial_Invoice_sample_CIPL_MV02110604202510-01.pdf
```

**문제점:**
- 서류 종류가 길면 파일명이 너무 길어짐
- 원본 파일명에 이미 날짜가 있을 수 있음

**대안 제안:**
```
# 옵션 A: 서류 종류 약어 사용
20251030_CIPL_MV02110604202510-01.pdf
20251030_BL_COKR25013204.pdf
20251030_SETTLE_부스터스_REV00.pdf

# 옵션 B: shipment_id를 앞에
TA254003250731_20251030_CIPL.pdf
TA254003250731_20251030_BL.pdf

# 옵션 C: 원본 파일명 유지 (가장 단순)
sample_CIPL_MV02110604202510-01.pdf  # 원본 그대로
```

**선택**: 옵션 ____ (또는 직접 정의): _______________

---

### 📌 **우선순위 2: 곧 필요**

#### Q5. 업로더 식별 방법

현재 Streamlit에는 인증이 없는데, 누가 업로드했는지 어떻게 기록할까요?

**선택지:**
- [ ] A. 업로드 시 이름 입력 (드롭다운)
  - 사용자 목록: _______________
- [ ] B. 업로드 시 이름 텍스트 입력
- [ ] C. 로그인 시스템 구현 (Streamlit Authentication)
  - 사용자/비밀번호: _______________
- [ ] D. Google OAuth (나중에)

#### Q6. Dashboard 시트 컬럼 확정

**제안 컬럼 (15개):**
```
1. upload_timestamp       # 업로드 시간
2. shipment_id           # 인보이스 번호
3. doc_type              # 서류 종류
4. file_name             # 파일명
5. drive_file_id         # Drive 파일 ID
6. drive_url             # 공유 링크
7. drive_folder_id       # 폴더 ID
8. uploader              # 업로더
9. file_size_bytes       # 파일 크기
10. status               # uploaded | processing | failed
11. error_message        # 에러 (있으면)
12. carrier_name         # 운송사 (SCM 시트에서 자동)
13. carrier_mode         # 운송 모드
14. origin               # 출발지
15. destination          # 도착지
```

**질문:**
- [ ] 위 컬럼으로 OK?
- [ ] 추가 필요 컬럼: _______________
- [ ] 삭제할 컬럼: _______________

**Phase 2 대비 컬럼 (지금은 비워둠):**
```
16. extracted_text       # AI 추출 텍스트 (Phase 2)
17. extracted_json       # 구조화된 데이터 (Phase 2)
18. embedding_status     # 임베딩 여부 (Phase 2)
```

이것들도 지금 추가할까요? (Y/N): _______________

#### Q7. SCM 통합 시트 매핑

현재 SCM 통합 시트에서 업로드 시 자동으로 가져올 정보:

**매핑:**
```
업로드 시 shipment_id 입력 → SCM 시트 검색
→ carrier_name, carrier_mode, origin, destination 자동 입력
```

**SCM 시트 컬럼 매핑:**
```python
{
    "인보이스 번호": "shipment_id",
    "carrier_name": "carrier_name",
    "carrier_mode": "carrier_mode",
    "출발창고": "origin",
    "도착창고": "destination",
    # 추가 필요한 컬럼?
}
```

**질문:**
- [ ] 위 매핑으로 OK?
- [ ] 추가로 가져올 컬럼: _______________

---

### 📌 **우선순위 3: 나중에 결정 가능**

#### Q8. 에러 알림 방법

파일 업로드 실패 시 알림?

**선택지:**
- [ ] A. Streamlit 화면에만 표시 (MVP)
- [ ] B. 이메일 발송
  - 수신자: _______________
- [ ] C. Slack 알림
  - Webhook URL: _______________
- [ ] D. 나중에

#### Q9. 파일 중복 처리

같은 shipment_id + doc_type에 파일 재업로드 시?

**선택지:**
- [ ] A. 덮어쓰기 (기존 파일 삭제)
- [ ] B. 버전 관리 (v1, v2, v3...)
- [ ] C. 업로드 거부 (중복 경고)
- [ ] D. 사용자에게 선택권

#### Q10. 배포 환경

**선택지:**
- [ ] A. Streamlit Cloud (무료, 간단)
  - 리소스 제한: 1GB RAM
- [ ] B. Google Cloud Run (유료, 유연)
  - 예상 비용: ~$10/월
- [ ] C. 로컬에서만 사용
- [ ] D. 나중에 결정

---

## 🔧 기술적 세부사항

### Q11. SCM 통합 시트 데이터 타입 확인

**발견된 날짜 형식:**
```
onboard_date: 45870 (Excel 시리얼 날짜)
exp_date: 20280616 (YYYYMMDD)
```

**질문:**
날짜를 어떻게 처리할까요?
- [ ] Excel 시리얼 → datetime 변환
- [ ] YYYYMMDD → datetime 변환
- [ ] 문자열 그대로 저장

### Q12. 대용량 파일 처리

**현재 샘플:**
- 최대 파일 크기: 1.6MB (PDF)

**질문:**
예상 최대 파일 크기는?
- [ ] < 10MB (대부분 문서)
- [ ] 10-50MB (스캔 PDF)
- [ ] > 50MB (대용량 첨부)

업로드 크기 제한 설정: _______________MB

### Q13. 다국어 지원

**현재 발견된 언어:**
- 한국어 (서류 종류, 필드명)
- 영어 (일부 서류)

**질문:**
UI 언어는?
- [ ] 한국어만
- [ ] 영어/한국어 혼용 (현재 샘플처럼)
- [ ] 완전 영어

---

## 📋 최종 확인 체크리스트

### Phase 1 개발 시작 전 필수

- [ ] Q1. 서비스 계정 JSON 확인
- [ ] Q2. 서류 종류 확정
- [ ] Q3. 폴더 구조 확정
- [ ] Q4. 파일명 규칙 확정
- [ ] Q5. 업로더 식별 방법
- [ ] Q6. Dashboard 시트 컬럼 확정

### 선택 사항 (개발 중 결정 가능)

- [ ] Q7. SCM 시트 매핑
- [ ] Q8. 에러 알림
- [ ] Q9. 파일 중복 처리
- [ ] Q10. 배포 환경
- [ ] Q11. 날짜 형식
- [ ] Q12. 파일 크기 제한
- [ ] Q13. 다국어

---

## 🎯 제안: 빠른 시작 경로

**최소한의 결정으로 시작하려면:**

1. ✅ **Q1**: 서비스 계정 JSON만 준비
2. ✅ **Q2**: 샘플에 있는 7개 서류 종류 사용
3. ✅ **Q3**: 제안 1 (심플 구조)
4. ✅ **Q4**: 옵션 C (원본 파일명 유지)
5. ✅ **Q5**: 옵션 B (이름 텍스트 입력)
6. ✅ **Q6**: 제안 15개 컬럼 사용

**나머지는 기본값:**
- Q7: 자동 매핑 (SCM 시트 검색)
- Q8: Streamlit 화면만
- Q9: 덮어쓰기
- Q10: Streamlit Cloud
- Q11: 자동 감지
- Q12: 50MB 제한
- Q13: 한국어/영어 혼용

**이렇게 하면**: 30분 내 개발 시작 가능!

---

## 📞 다음 단계

**당신이 할 일:**
1. 위 질문들 중 **Q1-Q6** 답변
2. 서비스 계정 JSON 준비 (또는 생성 가이드 요청)

**제가 할 일:**
1. 답변 받으면 즉시 개발 시작
2. 프로젝트 구조 생성
3. 첫 번째 작동하는 버전 제공

**예상 시간:**
- 질문 답변: 10분
- 개발: 1-2시간
- 테스트: 10분
= **총 2시간 후 작동하는 앱!**
