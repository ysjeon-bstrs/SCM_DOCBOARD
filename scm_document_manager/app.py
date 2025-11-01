"""
SCM Document Manager - Streamlit App (Simplified Vertical Layout)
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

# Minimal CSS - Clean and simple
st.markdown("""
    <style>
    /* Hide sidebar completely */
    [data-testid="collapsedControl"] {
        display: none;
    }

    /* Reduce padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* Button styling */
    .stButton>button {
        background-color: #4f46e5;
        color: white;
        border-radius: 0.375rem;
        font-weight: 500;
    }

    .stButton>button:hover {
        background-color: #4338ca;
    }

    /* Enlarge file uploader area */
    [data-testid="stFileUploader"] {
        min-height: 180px;
    }

    [data-testid="stFileUploader"] > div {
        padding: 2rem;
    }

    /* Clean header */
    h1 {
        font-size: 1.75rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.25rem;
    }

    /* Section headers */
    h2 {
        font-size: 1.25rem;
        font-weight: 600;
        color: #111827;
        margin-top: 0.5rem;
        margin-bottom: 0.25rem;
    }

    /* Captions */
    .caption {
        font-size: 0.875rem;
        color: #6b7280;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("📦 SCM 서류 관리 시스템")
st.markdown(f"<div class='caption'>업로더: {settings.default_uploader} | 총 {len(st.session_state.all_shipments)}건의 선적</div>", unsafe_allow_html=True)

st.divider()

# ===== 1. 서류 업로드 (전체 너비, 최우선) =====
st.subheader("📤 서류 업로드")
st.caption("Drive에 저장하고 한 번에 벡터화합니다")

# File uploader (enlarged)
uploaded_file = st.file_uploader(
    "파일을 드래그하거나 클릭하여 업로드",
    type=['pdf', 'xlsx', 'xls', 'csv', 'png', 'jpg', 'jpeg'],
    help=f"최대 {settings.max_file_size_mb}MB",
    key="file_uploader"
)

# Invoice Number and Document Type in 2 columns
col1, col2 = st.columns(2)

with col1:
    # Invoice Number selectbox (검색 기능 내장)
    invoice_options = ["송장 선택..."] + [s.invoice_no for s in st.session_state.all_shipments]
    selected_invoice = st.selectbox(
        "송장 번호",
        options=invoice_options,
        key="invoice_select"
    )

with col2:
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
    height=80,
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

                        # Clear and reload
                        st.rerun()
                    else:
                        st.error(f"❌ 업로드 실패: {result.error}")

                except Exception as e:
                    st.error(f"❌ 업로드 오류: {e}")
        else:
            st.error("선택한 송장을 찾을 수 없습니다")

st.divider()

# ===== 2. 선적 서류 현황 (전체 너비) =====
st.subheader("📋 선적 서류 현황")
st.caption("진행 중인 모든 선적 및 필요 서류 개요")

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

st.divider()

# ===== 3. 최근 활동 (전체 너비) =====
st.subheader("📊 최근 활동")
st.caption("모든 서류 업로드 및 분석 로그")

# Get recent logs
try:
    logs = st.session_state.sheets_service.get_upload_logs(limit=10)

    if not logs:
        st.info("최근 활동 없음\n\n서류를 업로드하여 시작하세요")
    else:
        # Display logs in a clean list
        for log in logs[:10]:  # Show 10 most recent
            upload_time = log.get('upload_timestamp', '')
            shipment_id = log.get('shipment_id', '')
            doc_type = log.get('doc_type', '')
            file_name = log.get('file_name', '')
            status = log.get('status', '')
            status_icon = "✅" if status == 'uploaded' else "⚠️"

            col_icon, col_content = st.columns([0.05, 0.95])

            with col_icon:
                st.markdown(f"<div style='font-size: 1.5rem;'>{status_icon}</div>", unsafe_allow_html=True)

            with col_content:
                st.markdown(f"**{file_name}**")
                st.caption(f"{shipment_id} - {doc_type} | {upload_time}")

            st.markdown("<hr style='margin: 0.5rem 0; border: none; border-top: 1px solid #e5e7eb;'>", unsafe_allow_html=True)

except Exception as e:
    st.warning("최근 활동을 불러올 수 없습니다")

st.divider()

# ===== 4. 서류 Q&A (맨 아래, Phase 2-3 예정) =====
with st.expander("🔍 서류 Q&A (Phase 2-3 예정)", expanded=False):
    st.caption("업로드된 서류를 기반으로 질문하세요")

    question = st.text_area(
        "질문 입력",
        placeholder="예: 송장 INPHL00025082900044의 총 금액은?",
        height=100,
        key="question_input"
    )

    if st.button("💬 AI에게 물어보기", type="primary", use_container_width=True, key="ask_ai"):
        if question:
            with st.spinner("AI가 답변을 생성 중..."):
                st.info("⚠️ AI Q&A 기능은 Phase 2에서 제공될 예정입니다")
        else:
            st.warning("질문을 입력해주세요")

    st.markdown("**답변**")
    st.info("AI의 답변이 여기에 표시됩니다")

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.caption(
    f"SCM 서류 관리 시스템 v1.0 (MVP) | "
    f"Streamlit + Google Drive + Sheets 기반"
)
