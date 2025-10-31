# SCM Document Manager

AI-powered logistics document management system for global shipment documentation.

## 🎯 Features (Phase 1 MVP)

### ✅ Implemented
- **Automatic Document Categorization**: 2-tier folder structure based on shipment type
- **Google Drive Integration**: Automatic folder creation and file upload
- **Google Sheets Integration**: SCM data lookup and upload logging
- **Shipment Search**: Search by invoice number or ticket name
- **Document Upload**: With metadata logging (18 columns)
- **Folder Rules**:
  - `00_SETTLEMENT`: 정산 documents
  - `01_KR_TO_3PL`: Korea → Overseas 3PL
  - `02_3PL_OUTBOUND`: 3PL → Outbound
  - `03_KR_TO_CUSTOMER`: Korea → Direct to customer
- **Structured Logging**: All operations logged with context
- **Error Handling**: Automatic retry with exponential backoff
- **Type Safety**: Pydantic models for data validation

### 🚧 Coming Soon (Phase 2)
- AI Document Extraction (Gemini API)
- Vector Database (ChromaDB)
- Natural Language Q&A
- Duplicate Detection
- Cost Analysis Dashboard

---

## 📁 Project Structure

```
scm_document_manager/
├── app.py                      # Streamlit main app
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
│
├── config/
│   ├── settings.py             # Pydantic Settings
│   └── logging_config.py       # Logging setup
│
├── core/
│   ├── models.py               # Pydantic data models
│   ├── enums.py                # Enumerations
│   └── exceptions.py           # Custom exceptions
│
├── services/
│   ├── drive_service.py        # Google Drive API
│   ├── sheets_service.py       # Google Sheets API
│   └── document_service.py     # Orchestration
│
├── ui/
│   └── pages/
│       └── upload_page.py      # Upload UI
│
├── utils/
│   ├── retry.py                # Retry decorator
│   └── folder_utils.py         # Folder categorization
│
└── tests/
    ├── unit/
    ├── integration/
    └── fixtures/
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Google Cloud Project with Drive/Sheets API enabled
- Service Account JSON key

### Installation

1. **Clone and navigate**
```bash
cd scm_document_manager
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` with your values:
```env
GOOGLE_DRIVE_ROOT_FOLDER_ID=your_folder_id
INVOICE_SHEET_ID=your_scm_sheet_id
DASHBOARD_SHEET_ID=your_dashboard_sheet_id
GOOGLE_CREDENTIALS_PATH=path/to/service-account.json
DEFAULT_UPLOADER=your_name
```

5. **Run the app**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🔧 Configuration

### Google Service Account Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable APIs:
   - Google Drive API
   - Google Sheets API
4. Create Service Account:
   - IAM & Admin → Service Accounts → Create
   - Download JSON key
5. Share Google Drive folder with service account email
6. Share Google Sheets with service account email (Editor access)

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_DRIVE_ROOT_FOLDER_ID` | Root folder ID for shipments | Yes |
| `INVOICE_SHEET_ID` | SCM 통합 sheet ID | Yes |
| `INVOICE_SHEET_NAME` | SCM sheet tab name | Yes |
| `DASHBOARD_SHEET_ID` | Dashboard sheet ID | Yes |
| `DASHBOARD_SHEET_NAME` | Dashboard tab name | Yes |
| `GOOGLE_CREDENTIALS_PATH` | Path to service account JSON | Yes* |
| `GOOGLE_CREDENTIALS_JSON` | Service account JSON string | Yes* |
| `DEFAULT_UPLOADER` | Default uploader name | No |
| `MAX_FILE_SIZE_MB` | Max file size (default: 8MB) | No |
| `LOG_LEVEL` | Logging level (default: INFO) | No |

*Either `GOOGLE_CREDENTIALS_PATH` or `GOOGLE_CREDENTIALS_JSON` is required

---

## 📊 Dashboard Schema

The system automatically logs uploads to Google Sheets with 18 columns:

| Column | Type | Description |
|--------|------|-------------|
| upload_timestamp | datetime | Upload time |
| shipment_id | string | Invoice number |
| doc_type | string | Document type |
| file_name | string | File name |
| drive_file_id | string | Drive file ID |
| drive_url | string | Drive URL |
| drive_folder_id | string | Folder ID |
| uploader | string | Uploader name |
| file_size_bytes | int | File size |
| status | enum | uploaded/processing/failed |
| error_message | string | Error message |
| carrier_name | string | Carrier name |
| carrier_mode | string | Transport mode |
| origin | string | Origin warehouse |
| destination | string | Destination warehouse |
| extracted_text | string | AI extracted text (Phase 2) |
| extracted_json | string | Structured data (Phase 2) |
| embedding_status | string | Embedding status (Phase 2) |

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/unit/test_folder_utils.py
```

---

## 📝 Usage Example

### Upload a Document

1. Navigate to "📤 Upload Document"
2. Search for shipment ID (e.g., "TA254003250731")
3. Select the matching shipment
4. Choose document type (e.g., "Commercial Invoice")
5. Upload your file
6. System will:
   - Determine folder category automatically
   - Create folder path: `01_KR_TO_3PL/TA254003250731/Commercial Invoice/`
   - Upload with standardized name: `20251030_CIPL_invoice.pdf`
   - Log to Dashboard sheet

---

## 🔒 Security

- ✅ Service account credentials stored securely
- ✅ Drive folders shared only with organization
- ✅ All API calls logged
- ✅ File size validation
- ✅ MIME type validation
- ✅ Retry logic with exponential backoff

---

## 🐛 Troubleshooting

### "Failed to initialize Drive service"
- Check service account JSON is valid
- Verify Drive API is enabled
- Ensure service account has access to Drive folder

### "Failed to search shipments"
- Check Sheets API is enabled
- Verify sheet ID is correct
- Ensure service account has Editor access to sheet

### "Folder creation failed"
- Verify root folder ID is correct
- Check service account has write permission
- Ensure folder doesn't already exist with same name

---

## 🛠️ Development

### Adding a new document type

Edit `core/enums.py`:
```python
class DocType(str, Enum):
    # ... existing types
    NEW_TYPE = "New Document Type"
```

### Customizing folder structure

Edit `utils/folder_utils.py`:
```python
def determine_shipment_category(...):
    # Add your logic
    pass
```

---

## 📈 Roadmap

### Phase 1 (MVP) ✅
- [x] File upload with Google Drive
- [x] Automatic folder categorization
- [x] SCM data integration
- [x] Dashboard logging
- [x] Basic UI

### Phase 2 (2-3 weeks)
- [ ] AI document extraction (Gemini)
- [ ] Vector database (ChromaDB)
- [ ] Natural language Q&A
- [ ] Duplicate detection
- [ ] Cost analysis

### Phase 3 (1-2 months)
- [ ] Time series analysis
- [ ] Anomaly detection
- [ ] Email/Slack notifications
- [ ] Mobile app
- [ ] Multi-language support

---

## 🤝 Contributing

1. Follow Python PEP 8 style guide
2. Add type hints
3. Write unit tests
4. Update documentation

---

## 📄 License

Internal use only - Boosters Inc.

---

## 💬 Support

For issues or questions, contact: 전용수 (SCM Team)

---

**Built with** ❤️ **using Streamlit, Google APIs, and Pydantic**
