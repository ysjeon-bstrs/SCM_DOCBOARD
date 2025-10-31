"""
SCM Document Manager - Streamlit App
"""
import streamlit as st

# Page config (must be first)
st.set_page_config(
    page_title="SCM 서류 관리 시스템",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Lazy imports after page config
from config.logging_config import setup_logging
from config.settings import get_settings

# Setup logging
setup_logging()

# Get settings (lazy loaded)
try:
    settings = get_settings()
except Exception as e:
    st.error(f"⚠️ 설정 오류: {e}")
    st.markdown("""
    ### 설정 필요

    Streamlit Secrets 또는 .env 파일에 다음을 설정하세요:

    ```toml
    # .streamlit/secrets.toml
    GOOGLE_DRIVE_ROOT_FOLDER_ID = "your_folder_id"
    INVOICE_SHEET_ID = "your_invoice_sheet_id"
    DASHBOARD_SHEET_ID = "your_dashboard_sheet_id"

    [GOOGLE_CREDENTIALS_JSON]
    type = "service_account"
    project_id = "your-project"
    private_key_id = "..."
    private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
    client_email = "your-service-account@your-project.iam.gserviceaccount.com"
    # ... rest of service account JSON
    ```
    """)
    st.stop()

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Main UI
st.markdown('<div class="main-header">📦 SCM 서류 관리 시스템</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI 기반 물류 서류 자동 관리 시스템</div>', unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("### 메뉴")
    page = st.radio(
        "페이지 선택",
        ["🏠 홈", "📤 서류 업로드", "📊 대시보드", "🔍 검색"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 시스템 정보")
    st.info(f"**업로더:** {settings.default_uploader}")
    st.info(f"**최대 파일 크기:** {settings.max_file_size_mb}MB")

# Page routing
if page == "🏠 홈":
    st.markdown("## SCM 서류 관리 시스템에 오신 것을 환영합니다")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="총 선적 건수",
            value="0",
            delta="업로드 준비"
        )

    with col2:
        st.metric(
            label="업로드된 서류",
            value="0",
            delta="오늘 +0"
        )

    with col3:
        st.metric(
            label="사용 중인 저장공간",
            value="0 MB"
        )

    st.markdown("---")
    st.markdown("### 빠른 시작 가이드")
    st.markdown("""
    1. **서류 업로드**: 사이드바에서 '📤 서류 업로드' 클릭
    2. **선적 선택**: 송장 번호로 선적 검색
    3. **서류 유형 선택**: 서류 유형 선택
    4. **업로드**: 파일 업로드

    시스템이 자동으로:
    - ✅ 서류를 분류하고 저장
    - ✅ 폴더 구조 생성
    - ✅ 대시보드에 메타데이터 기록
    - ✅ 검색 가능하게 만듦 (Phase 2: AI 검색)
    """)

elif page == "📤 서류 업로드":
    # Import upload page
    try:
        from ui.pages import upload_page
        upload_page.render()
    except Exception as e:
        st.error(f"업로드 페이지 로딩 오류: {e}")
        st.exception(e)

elif page == "📊 대시보드":
    st.markdown("## 📊 서류 대시보드")
    st.info("대시보드 뷰 준비 중...")

    st.markdown("### 최근 업로드")
    st.markdown("*아직 업로드된 서류가 없습니다*")

elif page == "🔍 검색":
    st.markdown("## 🔍 서류 검색")
    st.info("검색 기능 준비 중...")

    search_term = st.text_input("선적 ID, 서류 유형, 키워드로 검색")
    if st.button("검색"):
        st.warning("검색 기능은 Phase 2 (AI/Vector DB)에서 제공될 예정입니다")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
    "SCM 서류 관리 시스템 v1.0 (MVP) | Streamlit + Google Drive + Sheets 기반"
    "</div>",
    unsafe_allow_html=True
)
