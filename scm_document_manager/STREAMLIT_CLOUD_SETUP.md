# Streamlit Cloud 배포 가이드

## 🚀 빠른 배포 (5분)

### 1. 레포지토리 푸시
```bash
git add .
git commit -m "Add SCM Document Manager"
git push
```

### 2. Streamlit Cloud 배포

1. https://share.streamlit.io 접속
2. "New app" 클릭
3. 레포지토리 선택: `ysjeon-bstrs/SCM_DOCBOARD`
4. Branch: `main` 또는 현재 브랜치
5. Main file path: `scm_document_manager/app.py`
6. **Advanced settings** 클릭

### 3. Secrets 설정

**Secrets 입력 (TOML 형식):**

```toml
GOOGLE_DRIVE_ROOT_FOLDER_ID = "1zI9kD1WC-iXKDo-_ILjsb8PDBFhQMLl9"
INVOICE_SHEET_ID = "1RYjKW2UDJ2kWJLAqQH26eqx2-r9Xb0_qE_hfwu9WIj8"
INVOICE_SHEET_NAME = "scm통합"
DASHBOARD_SHEET_ID = "1lMcYrjTOePfXTQIb6fMqluLAXyXuhTY3zAbzdeEehvs"
DASHBOARD_SHEET_NAME = "dashboard"
DEFAULT_UPLOADER = "전용수"
MAX_FILE_SIZE_MB = 8

[GOOGLE_CREDENTIALS_JSON]
type = "service_account"
project_id = "python-spreadsheet-409212"
private_key_id = "3df25e0dc166..."
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@python-spreadsheet-409212.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
```

### 4. Deploy 클릭!

앱이 빌드되고 몇 분 후 URL이 생성됩니다.

---

## 🐛 트러블슈팅

### "Your app is in the oven" 계속 돌아감

**원인:**
- Secrets 설정 오류
- Service account JSON 포맷 오류

**해결:**
1. Streamlit Cloud 로그 확인
2. Secrets에서 JSON 포맷 확인
   - `private_key`에 `\n` 이스케이프 확인
   - 모든 필드 존재 확인

### "ModuleNotFoundError"

**원인:** `requirements.txt` 누락

**해결:**
```bash
cd scm_document_manager
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add requirements"
git push
```

### "Failed to initialize Drive service"

**원인:** Service account 권한 부족

**해결:**
1. Google Drive 폴더를 service account 이메일과 공유
2. Google Sheets를 service account와 공유 (Editor 권한)

---

## 📝 로컬 테스트

배포 전에 로컬에서 Streamlit Secrets 테스트:

```bash
# 1. .streamlit/secrets.toml 생성
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# 2. secrets.toml 편집 (실제 값 입력)
vim .streamlit/secrets.toml

# 3. 앱 실행
streamlit run app.py
```

---

## 🔒 보안 주의사항

- ✅ `secrets.toml`은 절대 git에 커밋하지 않기
- ✅ `.gitignore`에 `secrets.toml` 포함되어 있는지 확인
- ✅ Service account는 최소 권한만 부여
- ✅ Drive/Sheets 공유는 조직 내부로 제한

---

## 📊 Dashboard 시트 준비

앱 첫 실행 전에 Dashboard 시트에 헤더 추가:

**첫 번째 줄에 다음 18개 컬럼 입력:**

```
upload_timestamp | shipment_id | doc_type | file_name | drive_file_id | drive_url | drive_folder_id | uploader | file_size_bytes | status | error_message | carrier_name | carrier_mode | origin | destination | extracted_text | extracted_json | embedding_status
```

또는 Google Sheets에서 수동으로:

1. Dashboard 시트 열기
2. 첫 번째 행에 컬럼명 입력
3. 저장

---

## ✅ 배포 체크리스트

- [ ] Service account JSON 준비
- [ ] Google Drive 폴더 공유
- [ ] Google Sheets 공유 (Editor)
- [ ] Dashboard 시트 헤더 추가
- [ ] Streamlit Secrets 설정
- [ ] 로컬 테스트 완료
- [ ] 레포지토리 푸시
- [ ] Streamlit Cloud 배포
- [ ] 배포된 앱 테스트

---

## 🎉 배포 완료 후

앱 URL: `https://your-app-name.streamlit.app`

**첫 번째 업로드 테스트:**
1. 📤 Upload Document 페이지로 이동
2. Shipment ID 검색
3. 파일 업로드
4. Drive 폴더 확인
5. Dashboard 시트 확인

모든 것이 작동하면 성공! 🚀
