"""
SCM Document Manager - Streamlit App
"""
import streamlit as st

# Page config (must be first)
st.set_page_config(
    page_title="SCM Document Manager",
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
    st.error(f"⚠️ Configuration Error: {e}")
    st.markdown("""
    ### Setup Required

    Please configure the following in Streamlit Secrets or .env file:

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
st.markdown('<div class="main-header">📦 SCM Document Manager</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-powered logistics document management system</div>', unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("### Navigation")
    page = st.radio(
        "Select Page",
        ["🏠 Home", "📤 Upload Document", "📊 Dashboard", "🔍 Search"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### System Info")
    st.info(f"**Uploader:** {settings.default_uploader}")
    st.info(f"**Max File Size:** {settings.max_file_size_mb}MB")

# Page routing
if page == "🏠 Home":
    st.markdown("## Welcome to SCM Document Manager")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Total Shipments",
            value="0",
            delta="Ready to upload"
        )

    with col2:
        st.metric(
            label="Documents Uploaded",
            value="0",
            delta="+0 today"
        )

    with col3:
        st.metric(
            label="Storage Used",
            value="0 MB"
        )

    st.markdown("---")
    st.markdown("### Quick Start")
    st.markdown("""
    1. **Upload Document**: Click '📤 Upload Document' in the sidebar
    2. **Select Shipment**: Search for your shipment ID
    3. **Choose Document Type**: Select the document type or create a new one
    4. **Upload**: Upload your file

    The system will:
    - ✅ Automatically categorize and store your document
    - ✅ Create proper folder structure
    - ✅ Log all metadata to Dashboard
    - ✅ Make it searchable (Phase 2: AI search)
    """)

elif page == "📤 Upload Document":
    # Import upload page
    try:
        from ui.pages import upload_page
        upload_page.render()
    except Exception as e:
        st.error(f"Error loading upload page: {e}")
        st.exception(e)

elif page == "📊 Dashboard":
    st.markdown("## 📊 Document Dashboard")
    st.info("Dashboard view coming soon...")

    st.markdown("### Recent Uploads")
    st.markdown("*No uploads yet*")

elif page == "🔍 Search":
    st.markdown("## 🔍 Search Documents")
    st.info("Search functionality coming soon...")

    search_term = st.text_input("Search by shipment ID, document type, or keywords")
    if st.button("Search"):
        st.warning("Search feature will be available in Phase 2 (AI/Vector DB)")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
    "SCM Document Manager v1.0 (MVP) | Built with Streamlit + Google Drive + Sheets"
    "</div>",
    unsafe_allow_html=True
)
