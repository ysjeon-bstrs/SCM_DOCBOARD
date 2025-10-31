"""
Upload Document Page
"""
import streamlit as st
from services.sheets_service import SheetsService
from services.document_service import DocumentService
from core.enums import DocType


def render():
    """Render upload page"""
    st.markdown("## 📤 서류 업로드")

    # Initialize services (cached)
    if 'sheets_service' not in st.session_state:
        st.session_state.sheets_service = SheetsService()

    if 'document_service' not in st.session_state:
        st.session_state.document_service = DocumentService()

    # Step 1: Search Shipment
    st.markdown("### 1단계: 선적 선택")

    col1, col2 = st.columns([3, 1])

    with col1:
        search_term = st.text_input(
            "선적 ID 검색",
            placeholder="송장 번호 또는 티켓명 입력...",
            help="송장 번호 또는 티켓명으로 검색"
        )

    with col2:
        search_button = st.button("🔍 검색", use_container_width=True)

    if search_button and search_term:
        with st.spinner("선적 검색 중..."):
            try:
                matches = st.session_state.sheets_service.search_shipments(search_term)

                if matches:
                    st.success(f"{len(matches)}건의 선적을 찾았습니다")
                    st.session_state.search_results = matches
                else:
                    st.warning("검색 결과가 없습니다")
                    st.session_state.search_results = []

            except Exception as e:
                st.error(f"검색 실패: {e}")
                st.session_state.search_results = []

    # Display search results
    if 'search_results' in st.session_state and st.session_state.search_results:
        st.markdown("#### 선적 선택:")

        selected_shipment = None

        for i, shipment in enumerate(st.session_state.search_results):
            with st.expander(f"📦 {shipment.invoice_no} - {shipment.carrier_name} ({shipment.carrier_mode})"):
                col_a, col_b = st.columns(2)

                with col_a:
                    st.markdown(f"**송장번호:** {shipment.invoice_no}")
                    st.markdown(f"**운송사:** {shipment.carrier_name} ({shipment.carrier_mode})")
                    st.markdown(f"**경로:** {shipment.origin} → {shipment.destination}")

                with col_b:
                    if shipment.ticket_name:
                        st.markdown(f"**티켓명:** {shipment.ticket_name}")
                    if shipment.bl_no:
                        st.markdown(f"**BL 번호:** {shipment.bl_no}")
                    if shipment.status:
                        st.markdown(f"**상태:** {shipment.status}")

                if st.button(f"✅ 이 선적 선택", key=f"select_{i}"):
                    selected_shipment = shipment
                    st.session_state.selected_shipment = shipment
                    st.rerun()

    # Step 2: Document Type and Upload
    if 'selected_shipment' in st.session_state:
        shipment = st.session_state.selected_shipment

        st.markdown("---")
        st.markdown("### 2단계: 서류 업로드")

        st.info(f"**선택된 선적:** {shipment.invoice_no} ({shipment.carrier_name})")

        col_doc1, col_doc2 = st.columns(2)

        with col_doc1:
            doc_type = st.selectbox(
                "서류 유형",
                [dt.value for dt in DocType],
                help="업로드할 서류의 유형을 선택하세요"
            )

        with col_doc2:
            doc_abbr = st.text_input(
                "서류 약어",
                value="CIPL" if "Invoice" in doc_type else "DOC",
                help="파일명에 사용될 약어 (예: CIPL, BL, SETTLE)"
            )

        uploaded_file = st.file_uploader(
            "파일 선택",
            type=['pdf', 'xlsx', 'xls', 'csv', 'png', 'jpg', 'jpeg'],
            help=f"최대 파일 크기: {st.session_state.document_service.drive.settings.max_file_size_mb}MB"
        )

        if uploaded_file:
            file_size_mb = len(uploaded_file.getvalue()) / 1024 / 1024

            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.markdown(f"**파일명:** {uploaded_file.name}")
                st.markdown(f"**크기:** {file_size_mb:.2f} MB")
            with col_info2:
                st.markdown(f"**형식:** {uploaded_file.type}")

            if st.button("🚀 서류 업로드", type="primary", use_container_width=True):
                with st.spinner("업로드 중..."):
                    try:
                        result = st.session_state.document_service.upload_document(
                            file_content=uploaded_file.getvalue(),
                            file_name=uploaded_file.name,
                            shipment_id=shipment.invoice_no,
                            doc_type=doc_type,
                            doc_type_abbr=doc_abbr,
                            origin=shipment.origin,
                            destination=shipment.destination,
                            carrier_name=shipment.carrier_name,
                            carrier_mode=shipment.carrier_mode
                        )

                        if result.success:
                            st.success("✅ " + result.message)

                            if result.metadata:
                                with st.expander("📋 업로드 상세 정보"):
                                    st.json({
                                        "파일명": result.metadata.file_name,
                                        "드라이브 URL": result.metadata.drive_url,
                                        "폴더 경로": result.metadata.drive_folder_id,
                                        "업로더": result.metadata.uploader,
                                        "업로드 시간": result.metadata.upload_timestamp.isoformat()
                                    })

                            # Clear session
                            if st.button("다른 서류 업로드"):
                                del st.session_state.selected_shipment
                                st.rerun()
                        else:
                            st.error(f"❌ 업로드 실패: {result.error}")

                    except Exception as e:
                        st.error(f"❌ 업로드 오류: {e}")
