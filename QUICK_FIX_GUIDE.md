# 🚨 긴급 권한 변경 요청 (1분 요약)

## 문제
SCM 서류 업로드가 안됩니다.

## 원인
```
Service Account: boosters-chyoo@python-spreadsheet-409212.iam.gserviceaccount.com
현재 권한: "콘텐츠 관리자" ❌
→ 새 폴더 생성 불가능
```

## 해결
**다음 3개 폴더의 Service Account 권한을 "편집자"로 변경:**

1. `Boosters Internal`
2. `01-SCM`
3. `10-Global Logistics`

## 설정 방법
```
각 폴더 우클릭 → 공유 →
boosters-chyoo@python-spreadsheet-409212.iam.gserviceaccount.com 찾기 →
권한을 "편집자"로 변경 → 저장
```

## 이유
시스템이 자동으로 하위 폴더를 생성해야 하는데:
- **콘텐츠 관리자**: 폴더 생성 불가 ❌
- **편집자**: 폴더 생성 가능 ✅

## 예상 결과
```
변경 전: ❌ File not found 오류
변경 후: ✅ 자동 폴더 생성 및 파일 업로드 성공
```

**소요 시간**: 5분 (권한 변경 후 5-10분 대기)

---

**상세 설명**: `PERMISSION_ISSUE_EXPLANATION.md` 참고
