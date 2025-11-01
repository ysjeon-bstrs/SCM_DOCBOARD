"""
SCM Document Manager - Streamlit App (React-style UI)
"""
import streamlit as st
from datetime import datetime
import pandas as pd

# Page config (must be first) - WIDE MODE
st.set_page_config(
    page_title="SCM 서류 관리 시스템",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Lazy imports after page config
from config.logging_config import setup_logging
from config.settings import get_settings
from services.sheets_service import SheetsService
from services.document_service import DocumentService
from core.enums import DocType

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

# Load all shipments on first load
if 'all_shipments' not in st.session_state:
    try:
        with st.spinner("선적 데이터 로딩 중..."):
            st.session_state.all_shipments = st.session_state.sheets_service.get_all_shipments(limit=200)
    except Exception as e:
        st.error(f"선적 데이터 로딩 실패: {e}")
        st.session_state.all_shipments = []

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

    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 1.5rem;
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

    /* Header */
    .main-header {
        background: white;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        border-radius: 0.5rem;
    }

    .main-title {
        margin: 0;
        font-size: 1.875rem;
        font-weight: 700;
        color: #111827;
    }

    .main-subtitle {
        margin: 0.5rem 0 0 0;
        color: #6b7280;
        font-size: 0.875rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class='main-header'>
        <h1 class='main-title'>📦 SCM 서류 관리 시스템</h1>
        <p class='main-subtitle'>AI 기반 물류 서류 자동 관리 시스템</p>
    </div>
""", unsafe_allow_html=True)

# ===== TOP SECTION: Upload Document + Document Q&A =====
col_upload, col_qa = st.columns([1, 1], gap="large")

with col_upload:
    st.markdown("""
        <div style='background: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);'>
            <h2 style='margin: 0 0 0.5rem 0; font-size: 1.25rem; font-weight: 600;'>📤 서류 업로드</h2>
            <p style='margin: 0; font-size: 0.875rem; color: #6b7280;'>Drive에 저장하고 한 번에 벡터화합니다</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # File uploader
    uploaded_file = st.file_uploader(
        "파일 선택",
        type=['pdf', 'xlsx', 'xls', 'csv', 'png', 'jpg', 'jpeg'],
        help=f"최대 {settings.max_file_size_mb}MB",
        key="file_uploader"
    )

    # Invoice Number and Document Type in 2 columns
    subcol1, subcol2 = st.columns(2)

    with subcol1:
        # Invoice Number selectbox (검색 기능 내장)
        invoice_options = ["송장 선택..."] + [s.invoice_no for s in st.session_state.all_shipments]
        selected_invoice = st.selectbox(
            "송장 번호",
            options=invoice_options,
            key="invoice_select"
        )

    with subcol2:
        # Document Type selectbox
        doc_type_options = [dt.value for dt in DocType]
        selected_doc_type = st.selectbox(
            "서류 유형",
            options=doc_type_options,
            key="doctype_select"
        )

    # Description (optional)
    description = st.text_area(
        "설명 (선택사항)",
        placeholder="이 서류에 대한 간단한 메모를 추가하세요...",
        height=100,
        key="description_input"
    )

    # Upload button
    if st.button("🚀 업로드 & 벡터화", type="primary", use_container_width=True):
        if not uploaded_file:
            st.error("파일을 선택해주세요")
        elif selected_invoice == "송장 선택...":
            st.error("송장 번호를 선택해주세요")
        else:
            # Find selected shipment
            shipment = next((s for s in st.session_state.all_shipments if s.invoice_no == selected_invoice), None)

            if shipment:
                with st.spinner("업로드 중..."):
                    try:
                        # Get doc type abbreviation
                        doc_abbr = "CIPL" if "Invoice" in selected_doc_type else selected_doc_type[:4].upper()

                        result = st.session_state.document_service.upload_document(
                            file_content=uploaded_file.getvalue(),
                            file_name=uploaded_file.name,
                            shipment_id=shipment.invoice_no,
                            doc_type=selected_doc_type,
                            doc_type_abbr=doc_abbr,
                            origin=shipment.origin,
                            destination=shipment.destination,
                            carrier_name=shipment.carrier_name,
                            carrier_mode=shipment.carrier_mode
                        )

                        if result.success:
                            st.success(f"✅ {uploaded_file.name} 업로드 완료!")

                            if result.metadata:
                                with st.expander("📋 업로드 상세 정보"):
                                    st.json({
                                        "파일명": result.metadata.file_name,
                                        "드라이브 URL": result.metadata.drive_url,
                                        "폴더 경로": result.metadata.drive_folder_id,
                                        "업로더": result.metadata.uploader,
                                        "업로드 시간": result.metadata.upload_timestamp.isoformat()
                                    })

                            # Clear file uploader
                            st.rerun()
                        else:
                            st.error(f"❌ 업로드 실패: {result.error}")

                    except Exception as e:
                        st.error(f"❌ 업로드 오류: {e}")
            else:
                st.error("선택한 송장을 찾을 수 없습니다")

with col_qa:
    st.markdown("""
        <div style='background: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);'>
            <h2 style='margin: 0 0 0.5rem 0; font-size: 1.25rem; font-weight: 600;'>🔍 서류 Q&A</h2>
            <p style='margin: 0; font-size: 0.875rem; color: #6b7280;'>업로드된 서류를 기반으로 질문하세요</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    question = st.text_area(
        "질문 입력",
        placeholder="예: 송장 INPHL00025082900044의 총 금액은?",
        height=150,
        key="question_input"
    )

    if st.button("💬 AI에게 물어보기", type="primary", use_container_width=True):
        if question:
            with st.spinner("AI가 답변을 생성 중..."):
                st.info("⚠️ AI Q&A 기능은 Phase 2에서 제공될 예정입니다")
        else:
            st.warning("질문을 입력해주세요")

    st.markdown("### 답변")
    st.info("AI의 답변이 여기에 표시됩니다")

# Divider
st.markdown("<br>", unsafe_allow_html=True)
st.divider()

# ===== BOTTOM SECTION: Shipment Document Status + Recent Activity =====
col_main, col_side = st.columns([2, 1], gap="large")

with col_main:
    # Shipment Document Status
    st.markdown("""
        <div style='background: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1); margin-bottom: 1rem;'>
            <div style='border-bottom: 1px solid #e5e7eb; padding-bottom: 1rem; margin-bottom: 1rem;'>
                <h2 style='margin: 0; font-size: 1.125rem; font-weight: 600; color: #111827;'>선적 서류 현황</h2>
                <p style='margin: 0.25rem 0 0 0; font-size: 0.875rem; color: #6b7280;'>진행 중인 모든 선적 및 필요 서류 개요</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Display shipment data
    if st.session_state.all_shipments:
        # Create DataFrame
        shipment_data = []
        for s in st.session_state.all_shipments[:50]:  # Show first 50
            shipment_data.append({
                "송장번호": s.invoice_no,
                "티켓명": s.ticket_name or "-",
                "일자": s.onboard_date or "-",
                "경로": f"{s.origin} → {s.destination}",
                "운송사": f"{s.carrier_name} ({s.carrier_mode})",
                "BL번호": s.bl_no or "-",
                "상태": s.status or "-"
            })

        df = pd.DataFrame(shipment_data)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=400
        )

        st.caption(f"총 {len(st.session_state.all_shipments)}건의 선적 중 {len(shipment_data)}건 표시")
    else:
        st.info("선적 데이터가 없습니다")

with col_side:
    # Recent Activity
    st.markdown("""
        <div style='background: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1); margin-bottom: 1rem;'>
            <div style='border-bottom: 1px solid #e5e7eb; padding-bottom: 1rem; margin-bottom: 1rem;'>
                <h2 style='margin: 0; font-size: 1.125rem; font-weight: 600; color: #111827;'>최근 활동</h2>
                <p style='margin: 0.25rem 0 0 0; font-size: 0.875rem; color: #6b7280;'>모든 서류 업로드 및 분석 로그</p>
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
                    <p style='margin-top: 0.25rem; font-size: 0.875rem; color: #6b7280;'>서류를 업로드하여 시작하세요</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            for log in logs[:8]:  # Show only 8 most recent
                upload_time = log.get('upload_timestamp', '')
                shipment_id = log.get('shipment_id', '')
                doc_type = log.get('doc_type', '')
                file_name = log.get('file_name', '')
                status_icon = "✅" if log.get('status') == 'uploaded' else "⚠️"

                st.markdown(f"""
                    <div style='padding: 0.75rem; border-bottom: 1px solid #e5e7eb; background: white; border-radius: 0.25rem; margin-bottom: 0.5rem;'>
                        <div style='display: flex; align-items: center;'>
                            <span style='font-size: 1.25rem; margin-right: 0.5rem;'>{status_icon}</span>
                            <div style='flex: 1;'>
                                <div style='font-size: 0.875rem; font-weight: 500; color: #111827;'>{file_name}</div>
                                <div style='font-size: 0.75rem; color: #6b7280; margin-top: 0.25rem;'>
                                    <strong>{shipment_id}</strong> - {doc_type}
                                </div>
                                <div style='font-size: 0.625rem; color: #9ca3af; margin-top: 0.25rem;'>
                                    {upload_time}
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.warning("최근 활동을 불러올 수 없습니다")

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6b7280; font-size: 0.875rem;'>"
    f"SCM 서류 관리 시스템 v1.0 | 업로더: {settings.default_uploader} | "
    f"총 {len(st.session_state.all_shipments)}건의 선적"
    "</div>",
    unsafe_allow_html=True
)
