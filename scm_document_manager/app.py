"""
SCM Document Manager - Streamlit App (React-style UI)
"""
import streamlit as st
from datetime import datetime

# Page config (must be first) - WIDE MODE
st.set_page_config(
    page_title="SCM 서류 관리 시스템",
    page_icon="📦",
    layout="wide",  # Wide mode for full-width layout
    initial_sidebar_state="collapsed"  # Hide sidebar by default
)

# Lazy imports after page config
from config.logging_config import setup_logging
from config.settings import get_settings
from services.sheets_service import SheetsService
from services.document_service import DocumentService

# Setup logging
setup_logging()

# Get settings (lazy loaded)
try:
    settings = get_settings()
except Exception as e:
    st.error(f"⚠️ 설정 오류: {e}")
    st.stop()

# Initialize services (cached in session)
if 'sheets_service' not in st.session_state:
    st.session_state.sheets_service = SheetsService()

if 'document_service' not in st.session_state:
    st.session_state.document_service = DocumentService()

# Custom CSS for React-style UI
st.markdown("""
    <style>
    /* Hide sidebar completely */
    [data-testid="collapsedControl"] {
        display: none;
    }

    /* Card styling */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        margin-bottom: 1rem;
    }

    .card-header {
        border-bottom: 1px solid #e5e7eb;
        padding-bottom: 1rem;
        margin-bottom: 1rem;
    }

    .card-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #111827;
        margin: 0;
    }

    .card-description {
        font-size: 0.875rem;
        color: #6b7280;
        margin-top: 0.25rem;
    }

    /* Stat card styling */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    }

    .stat-value {
        font-size: 1.875rem;
        font-weight: 600;
        color: #111827;
    }

    .stat-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Button styling */
    .stButton>button {
        background-color: #4f46e5;
        color: white;
        border-radius: 0.375rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
        border: none;
        transition: background-color 0.2s;
    }

    .stButton>button:hover {
        background-color: #4338ca;
    }

    /* Table styling */
    .dataframe {
        font-size: 0.875rem;
    }

    /* Upload button */
    .upload-button {
        background-color: #4f46e5;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 600;
        text-align: center;
        cursor: pointer;
        transition: background-color 0.2s;
    }

    .upload-button:hover {
        background-color: #4338ca;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div style='background: white; padding: 1.5rem; margin-bottom: 2rem; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);'>
        <h1 style='margin: 0; font-size: 1.875rem; font-weight: 700; color: #111827;'>📦 SCM 서류 관리 시스템</h1>
        <p style='margin: 0.5rem 0 0 0; color: #6b7280;'>AI 기반 물류 서류 자동 관리 시스템</p>
    </div>
""", unsafe_allow_html=True)

# Analytics Overview (4 cards)
st.markdown("### 대시보드 개요")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class='stat-card'>
            <div class='stat-label'>총 선적 건수</div>
            <div class='stat-value'>0</div>
            <div style='color: #6b7280; font-size: 0.75rem; margin-top: 0.25rem;'>전체</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='stat-card'>
            <div class='stat-label'>업로드된 서류</div>
            <div class='stat-value'>0</div>
            <div style='color: #6b7280; font-size: 0.75rem; margin-top: 0.25rem;'>전체</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class='stat-card'>
            <div class='stat-label'>누락된 서류</div>
            <div class='stat-value'>0</div>
            <div style='color: #6b7280; font-size: 0.75rem; margin-top: 0.25rem;'>주의 필요</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class='stat-card'>
            <div class='stat-label'>완료율</div>
            <div class='stat-value'>0%</div>
            <div style='color: #6b7280; font-size: 0.75rem; margin-top: 0.25rem;'>총 0 건</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Content (Dashboard 2/3 + Recent Activity 1/3)
col_main, col_side = st.columns([2, 1])

with col_main:
    # Shipment Document Status
    st.markdown("""
        <div class='card'>
            <div class='card-header'>
                <div class='card-title'>선적 서류 현황</div>
                <div class='card-description'>진행 중인 모든 선적 및 필요 서류 개요</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Get shipment data
    try:
        # Search for all shipments (empty search returns all or recent ones)
        # For now, show a placeholder
        st.info("선적 데이터를 불러오는 중...")

        # Placeholder table
        st.dataframe(
            {
                "송장번호": ["INV-001", "INV-002", "INV-003"],
                "일자": ["2025-11-01", "2025-11-01", "2025-11-01"],
                "경로": ["KR → US", "KR → SG", "KR → MY"],
                "Invoice": ["✅", "❌", "✅"],
                "Packing List": ["✅", "✅", "❌"],
                "BL": ["✅", "❌", "✅"],
            },
            use_container_width=True,
            hide_index=True
        )
    except Exception as e:
        st.error(f"데이터 로딩 오류: {e}")

with col_side:
    # Recent Activity
    st.markdown("""
        <div class='card'>
            <div class='card-header'>
                <div class='card-title'>최근 활동</div>
                <div class='card-description'>모든 서류 업로드 및 분석 로그</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Get recent logs
    try:
        logs = st.session_state.sheets_service.get_upload_logs(limit=10)

        if not logs:
            st.markdown("""
                <div style='text-align: center; padding: 3rem 1.5rem;'>
                    <svg style='width: 3rem; height: 3rem; margin: 0 auto; color: #9ca3af;' fill='none' viewBox='0 0 24 24' stroke='currentColor'>
                        <path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z' />
                    </svg>
                    <h3 style='margin-top: 0.5rem; font-size: 0.875rem; font-weight: 500; color: #111827;'>최근 활동 없음</h3>
                    <p style='margin-top: 0.25rem; font-size: 0.875rem; color: #6b7280;'>서류를 업로드하여 시작하세요.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            for log in logs[:5]:  # Show only 5 most recent
                upload_time = log.get('upload_timestamp', '')
                shipment_id = log.get('shipment_id', '')
                doc_type = log.get('doc_type', '')
                file_name = log.get('file_name', '')

                st.markdown(f"""
                    <div style='padding: 0.75rem; border-bottom: 1px solid #e5e7eb;'>
                        <div style='font-size: 0.875rem; font-weight: 500; color: #111827;'>{file_name}</div>
                        <div style='font-size: 0.75rem; color: #6b7280; margin-top: 0.25rem;'>
                            <strong>{shipment_id}</strong> - {doc_type}
                        </div>
                        <div style='font-size: 0.625rem; color: #9ca3af; margin-top: 0.25rem;'>
                            {upload_time}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.warning("최근 활동을 불러올 수 없습니다.")

# Upload Section (floating button or inline)
st.markdown("<br>", unsafe_allow_html=True)

with st.expander("📤 서류 업로드", expanded=False):
    upload_col1, upload_col2 = st.columns(2)

    with upload_col1:
        search_term = st.text_input(
            "선적 검색",
            placeholder="송장 번호 또는 티켓명 입력...",
            key="search_shipment"
        )

        if st.button("🔍 검색", key="search_btn"):
            if search_term:
                with st.spinner("검색 중..."):
                    try:
                        matches = st.session_state.sheets_service.search_shipments(search_term)
                        if matches:
                            st.success(f"{len(matches)}건의 선적을 찾았습니다")
                            st.session_state.search_results = matches
                        else:
                            st.warning("검색 결과가 없습니다")
                    except Exception as e:
                        st.error(f"검색 실패: {e}")

    with upload_col2:
        if 'search_results' in st.session_state and st.session_state.search_results:
            selected_shipment = st.selectbox(
                "선적 선택",
                options=st.session_state.search_results,
                format_func=lambda x: f"{x.invoice_no} - {x.carrier_name}",
                key="select_shipment"
            )

            if selected_shipment:
                st.session_state.selected_shipment = selected_shipment

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6b7280; font-size: 0.875rem;'>"
    "SCM 서류 관리 시스템 v1.0 (MVP) | Streamlit + Google Drive + Sheets 기반"
    "</div>",
    unsafe_allow_html=True
)
