# Google Drive 권한 문제 해결 요청

## 📋 요약

**문제**: SCM 서류 자동 업로드 시스템이 Google Drive 폴더에 접근하지 못하고 있습니다.

**원인**: Service Account의 권한이 "콘텐츠 관리자"로 설정되어 있어 **하위 폴더 생성이 불가능**합니다.

**해결**: Service Account를 **"편집자" 권한**으로 변경 필요합니다.

---

## 🔍 문제 상세

### 현재 상황

**Service Account 이메일:**
```
boosters-chyoo@python-spreadsheet-409212.iam.gserviceaccount.com
```

**대상 폴더:**
```
Boosters Internal > 01-SCM > 10-Global Logistics
```

**현재 권한:** 콘텐츠 관리자 ❌
**필요 권한:** 편집자 ✅

### 발생하는 오류

```
HttpError 404: File not found
Cannot access root folder (ID: 1zI9kD1WC-iXKDo-_ILjsb8PDBFhQMLl9)
```

---

## 🔑 Google Drive 권한 차이

### 콘텐츠 관리자 (Content Manager)
- ✅ 기존 폴더에 파일 추가 가능
- ✅ 파일 삭제 가능
- ❌ **새 폴더 생성 불가능** ← 문제!
- ❌ 공유 설정 변경 불가능

### 편집자 (Editor)
- ✅ 기존 폴더에 파일 추가 가능
- ✅ 파일 삭제 가능
- ✅ **새 폴더 생성 가능** ← 필요!
- ✅ 파일 구조 관리 가능

---

## 💻 시스템이 하는 작업

서류 업로드 시 시스템이 자동으로 수행하는 작업:

```
1. 루트 폴더 접근: 10-Global Logistics
   ↓
2. 카테고리 폴더 확인/생성: 03_KR_TO_CUSTOMER
   ↓  (없으면 자동 생성 필요!)
3. 송장 폴더 확인/생성: MV02050205202509-04
   ↓  (없으면 자동 생성 필요!)
4. 서류 유형 폴더 확인/생성: Commercial Invoice + Packing List
   ↓  (없으면 자동 생성 필요!)
5. 파일 업로드
```

**콘텐츠 관리자 권한**: 2~4단계에서 새 폴더 생성 불가 → 실패
**편집자 권한**: 모든 단계 정상 작동 → 성공

---

## ✅ 해결 방법

### 요청 사항

다음 폴더들에 Service Account를 **"편집자" 권한**으로 추가/변경 부탁드립니다:

1. **Boosters Internal** (최상위 폴더)
   - Service Account: `boosters-chyoo@python-spreadsheet-409212.iam.gserviceaccount.com`
   - 권한: **편집자** (Editor)

2. **01-SCM** (중간 폴더)
   - Service Account: `boosters-chyoo@python-spreadsheet-409212.iam.gserviceaccount.com`
   - 권한: **편집자** (Editor)

3. **10-Global Logistics** (루트 작업 폴더)
   - Service Account: `boosters-chyoo@python-spreadsheet-409212.iam.gserviceaccount.com`
   - 권한: **편집자** (Editor)

### 설정 방법

1. Google Drive에서 각 폴더 우클릭 → "공유" 또는 "액세스 권한 관리"
2. 기존에 있는 `boosters-chyoo@python-spreadsheet-409212.iam.gserviceaccount.com` 찾기
3. 권한을 **"콘텐츠 관리자" → "편집자"**로 변경
4. 저장

또는

1. 새로 추가: `boosters-chyoo@python-spreadsheet-409212.iam.gserviceaccount.com`
2. 권한: **"편집자"** 선택
3. "알림 보내기" 체크 해제 (선택사항)
4. 저장

---

## 📊 예상 효과

### 변경 전 (현재)
```
❌ 폴더 생성 실패
❌ 파일 업로드 불가
❌ "File not found" 오류
```

### 변경 후
```
✅ 자동 폴더 구조 생성
✅ 파일 업로드 성공
✅ 다음과 같은 구조 자동 생성:

10-Global Logistics/
  └─ 03_KR_TO_CUSTOMER/
      └─ MV02050205202509-04/
          └─ Commercial Invoice + Packing List/
              └─ 20251106_CIPL_파일명.pdf
```

---

## 🔐 보안 고려사항

### Service Account란?
- 사람이 아닌 **프로그램 전용 가상 계정**
- 자동화 작업에만 사용
- 실제 사용자 계정과 분리되어 안전

### 편집자 권한 부여 시 가능한 작업
- ✅ 폴더/파일 생성
- ✅ 파일 업로드
- ✅ 파일 수정/삭제
- ❌ 폴더 소유권 변경 불가
- ❌ 다른 사용자 권한 변경 불가

### 위험도
- **낮음**: Service Account는 코드로만 제어되며, 인증 키는 안전하게 보관됨
- Streamlit Cloud의 Secrets 기능으로 암호화되어 저장

---

## 📝 참고: 테스트 결과

### 로그 분석
```
2025-11-06 08:46:46,368
ERROR - Cannot access folder 1zI9kD1WC-iXKDo-_ILjsb8PDBFhQMLl9
HttpError 404: File not found
```

### 시도한 해결책
1. ✅ Service Account 이메일 확인 - 정확함
2. ✅ 폴더 ID 확인 - 정확함
3. ✅ Google Drive API 활성화 확인 - 정상
4. ✅ Credentials 로딩 확인 - 정상
5. ❌ **폴더 접근 권한** - 문제 발견!

### 권한 확인 결과
```
현재 상태:
- 사용자 계정: 콘텐츠 관리자 (공유 권한 없음)
- Service Account: 콘텐츠 관리자 (폴더 생성 불가)

필요 상태:
- Service Account: 편집자 (폴더 생성 가능)
```

---

## ⏱️ 예상 작업 시간

- **권한 변경 작업**: 5분
- **권한 전파 대기**: 5-10분 (Google 서버 처리 시간)
- **테스트 및 확인**: 5분

**총 소요 시간**: 약 15-20분

---

## 📞 추가 질문사항

궁금한 점이 있으시면 언제든지 문의 부탁드립니다.

- Service Account 작동 원리
- 권한 설정 방법
- 보안 관련 우려사항
- 테스트 방법

---

**작성자**: 전용수
**작성일**: 2025-11-06
**문서 버전**: 1.0
