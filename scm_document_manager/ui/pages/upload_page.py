"""
Upload Document Page
"""
import streamlit as st
from services.sheets_service import SheetsService
from services.document_service import DocumentService
from core.enums import DocType


def render():
    """Render upload page"""
    st.markdown("## 📤 Upload Document")

    # Initialize services (cached)
    if 'sheets_service' not in st.session_state:
        st.session_state.sheets_service = SheetsService()

    if 'document_service' not in st.session_state:
        st.session_state.document_service = DocumentService()

    # Step 1: Search Shipment
    st.markdown("### Step 1: Select Shipment")

    col1, col2 = st.columns([3, 1])

    with col1:
        search_term = st.text_input(
            "Search Shipment ID",
            placeholder="Enter invoice number or ticket name...",
            help="Search by invoice number or ticket name"
        )

    with col2:
        search_button = st.button("🔍 Search", use_container_width=True)

    if search_button and search_term:
        with st.spinner("Searching shipments..."):
            try:
                matches = st.session_state.sheets_service.search_shipments(search_term)

                if matches:
                    st.success(f"Found {len(matches)} shipment(s)")
                    st.session_state.search_results = matches
                else:
                    st.warning("No shipments found")
                    st.session_state.search_results = []

            except Exception as e:
                st.error(f"Search failed: {e}")
                st.session_state.search_results = []

    # Display search results
    if 'search_results' in st.session_state and st.session_state.search_results:
        st.markdown("#### Select Shipment:")

        selected_shipment = None

        for i, shipment in enumerate(st.session_state.search_results):
            with st.expander(f"📦 {shipment.invoice_no} - {shipment.carrier_name} ({shipment.carrier_mode})"):
                col_a, col_b = st.columns(2)

                with col_a:
                    st.markdown(f"**Invoice:** {shipment.invoice_no}")
                    st.markdown(f"**Carrier:** {shipment.carrier_name} ({shipment.carrier_mode})")
                    st.markdown(f"**Route:** {shipment.origin} → {shipment.destination}")

                with col_b:
                    if shipment.ticket_name:
                        st.markdown(f"**Ticket:** {shipment.ticket_name}")
                    if shipment.bl_no:
                        st.markdown(f"**BL No:** {shipment.bl_no}")
                    if shipment.status:
                        st.markdown(f"**Status:** {shipment.status}")

                if st.button(f"✅ Select This Shipment", key=f"select_{i}"):
                    selected_shipment = shipment
                    st.session_state.selected_shipment = shipment
                    st.rerun()

    # Step 2: Document Type and Upload
    if 'selected_shipment' in st.session_state:
        shipment = st.session_state.selected_shipment

        st.markdown("---")
        st.markdown("### Step 2: Upload Document")

        st.info(f"**Selected Shipment:** {shipment.invoice_no} ({shipment.carrier_name})")

        col_doc1, col_doc2 = st.columns(2)

        with col_doc1:
            doc_type = st.selectbox(
                "Document Type",
                [dt.value for dt in DocType],
                help="Select the type of document you're uploading"
            )

        with col_doc2:
            doc_abbr = st.text_input(
                "Document Abbreviation",
                value="CIPL" if "Invoice" in doc_type else "DOC",
                help="Short abbreviation for file naming (e.g., CIPL, BL, SETTLE)"
            )

        uploaded_file = st.file_uploader(
            "Choose file",
            type=['pdf', 'xlsx', 'xls', 'csv', 'png', 'jpg', 'jpeg'],
            help=f"Maximum file size: {st.session_state.document_service.drive.settings.max_file_size_mb}MB"
        )

        if uploaded_file:
            file_size_mb = len(uploaded_file.getvalue()) / 1024 / 1024

            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.markdown(f"**File:** {uploaded_file.name}")
                st.markdown(f"**Size:** {file_size_mb:.2f} MB")
            with col_info2:
                st.markdown(f"**Type:** {uploaded_file.type}")

            if st.button("🚀 Upload Document", type="primary", use_container_width=True):
                with st.spinner("Uploading..."):
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
                                with st.expander("📋 Upload Details"):
                                    st.json({
                                        "File Name": result.metadata.file_name,
                                        "Drive URL": result.metadata.drive_url,
                                        "Folder Path": result.metadata.drive_folder_id,
                                        "Uploader": result.metadata.uploader,
                                        "Upload Time": result.metadata.upload_timestamp.isoformat()
                                    })

                            # Clear session
                            if st.button("Upload Another Document"):
                                del st.session_state.selected_shipment
                                st.rerun()
                        else:
                            st.error(f"❌ Upload failed: {result.error}")

                    except Exception as e:
                        st.error(f"❌ Upload error: {e}")
