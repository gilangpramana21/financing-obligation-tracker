# System Architecture

## Overview

The Financing Obligation Tracker is a multi-phase system for automated monitoring of financing agreements.

---

## Phase 2 Architecture (Current)

```
┌─────────────────────────────────────────────────────────────────┐
│                     DOCUMENT INGESTION                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  documents/      │
                    │  - loan1.pdf     │
                    │  - loan2.docx    │
                    │  - loan3.pdf     │
                    └──────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTRACTION PIPELINE                          │
│                      (extractor.py)                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
         ┌──────────┐  ┌──────────┐  ┌──────────┐
         │pdfplumber│  │ PyMuPDF  │  │python-   │
         │          │  │(fallback)│  │docx      │
         └──────────┘  └──────────┘  └──────────┘
                │             │             │
                └─────────────┼─────────────┘
                              ▼
                    ┌──────────────────┐
                    │  Extracted Text  │
                    │  (45,000 chars)  │
                    └──────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AI ANALYSIS                                │
│                  (Claude Sonnet 4)                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Structured JSON  │
                    │ - Agreement info │
                    │ - Reporting      │
                    │ - Covenants      │
                    │ - Other oblig.   │
                    └──────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    VALIDATION & STORAGE                         │
│                      (models.py)                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  SQLite Database │
                    │  obligation_     │
                    │  tracker.db      │
                    └──────────────────┘
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
         ┌──────────┐  ┌──────────┐  ┌──────────┐
         │agreements│  │reporting_│  │covenants │
         │          │  │obligations│  │          │
         └──────────┘  └──────────┘  └──────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │other_obligations │
                    └──────────────────┘
```

---

## Data Flow

### 1. Document Input
```
User Action: Drop PDF/Word file into documents/
↓
System: Detects file type (.pdf, .docx, .doc)
```

### 2. Text Extraction
```
PDF Path → pdfplumber.open()
         ↓
         Extract text from each page
         ↓
         Combine into single text string
         ↓
         (If fails) → PyMuPDF fallback
```

### 3. AI Extraction
```
Document Text → Build extraction prompt
              ↓
              Anthropic API call
              ↓
              Claude Sonnet 4 analysis
              ↓
              Structured JSON response
```

### 4. Validation
```
JSON Response → Check required fields
              ↓
              Validate date formats
              ↓
              Ensure lists exist
              ↓
              Type conversions
```

### 5. Database Storage
```
Validated Data → Create Agreement record
               ↓
               Create ReportingObligation records
               ↓
               Create Covenant records
               ↓
               Create OtherObligation records
               ↓
               Commit transaction
```

---

## Component Interaction

```
┌─────────────────┐
│  extractor.py   │ ◄─── Main entry point
└────────┬────────┘
         │
         ├─► DocumentExtractor class
         │   ├─► extract_text()
         │   ├─► extract_obligations_from_text()
         │   ├─► validate_extracted_data()
         │   └─► save_to_database()
         │
         ▼
┌─────────────────┐
│   models.py     │ ◄─── Database schema
└────────┬────────┘
         │
         ├─► Agreement (ORM model)
         ├─► ReportingObligation (ORM model)
         ├─► Covenant (ORM model)
         ├─► OtherObligation (ORM model)
         ├─► init_db()
         └─► get_session()
         │
         ▼
┌─────────────────┐
│ monitoring.py   │ ◄─── Status logic (Phase 1)
└────────┬────────┘
         │
         ├─► check_covenant_status()
         ├─► check_reporting_status()
         ├─► check_renewal_status()
         └─► get_status_emoji()
         │
         ▼
┌─────────────────┐
│ dashboard.py    │ ◄─── UI (Phase 1, to be built)
└─────────────────┘
```

---

## Database Schema

```
┌─────────────────────────────────────────┐
│            agreements                   │
├─────────────────────────────────────────┤
│ id (PK)                                 │
│ financier                               │
│ agreement_name                          │
│ contract_start                          │
│ contract_end                            │
│ facility_amount                         │
│ currency                                │
│ created_at                              │
└─────────────────────────────────────────┘
         │
         │ 1:N
         ├──────────────────────────────────┐
         │                                  │
         ▼                                  ▼
┌──────────────────────┐      ┌──────────────────────┐
│ reporting_obligations│      │     covenants        │
├──────────────────────┤      ├──────────────────────┤
│ id (PK)              │      │ id (PK)              │
│ agreement_id (FK)    │      │ agreement_id (FK)    │
│ report_name          │      │ name                 │
│ frequency            │      │ type                 │
│ due_day              │      │ metric               │
│ description          │      │ threshold            │
│ next_due             │      │ unit                 │
└──────────────────────┘      │ description          │
                              │ current_value        │
                              │ last_updated         │
                              └──────────────────────┘
         │
         │ 1:N
         ▼
┌──────────────────────┐
│  other_obligations   │
├──────────────────────┤
│ id (PK)              │
│ agreement_id (FK)    │
│ category             │
│ description          │
│ is_ongoing           │
└──────────────────────┘
```

---

## LLM Extraction Prompt Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    EXTRACTION PROMPT                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. CONTEXT                                                 │
│     "You are analyzing a financing agreement document..."   │
│                                                             │
│  2. DOCUMENT TEXT                                           │
│     [Full extracted text from PDF/Word]                     │
│                                                             │
│  3. SCHEMA DEFINITION                                       │
│     {                                                       │
│       "financier": "string",                                │
│       "agreement_name": "string",                           │
│       ...                                                   │
│     }                                                       │
│                                                             │
│  4. EXTRACTION RULES                                        │
│     - Date format: YYYY-MM-DD                               │
│     - Amounts: Pure numbers                                 │
│     - Frequencies: Exact values                             │
│     - Covenant types: minimum/maximum                       │
│     - Categories: Specific list                             │
│                                                             │
│  5. OUTPUT INSTRUCTION                                      │
│     "Return ONLY the JSON object, no other text"            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Error Handling Flow

```
┌─────────────────┐
│ Process Document│
└────────┬────────┘
         │
         ▼
    File exists? ──No──► FileNotFoundError
         │
         Yes
         ▼
    Supported format? ──No──► ValueError
         │
         Yes
         ▼
    Extract text
         │
         ├─► pdfplumber fails? ──Yes──► Try PyMuPDF
         │                               │
         │                               ├─► Success ──┐
         │                               │             │
         │                               └─► Fail ─────┤
         │                                             │
         ▼                                             │
    LLM extraction ◄──────────────────────────────────┘
         │
         ├─► API error? ──Yes──► Exception
         │
         ▼
    Parse JSON
         │
         ├─► Invalid JSON? ──Yes──► JSONDecodeError
         │
         ▼
    Validate schema
         │
         ├─► Missing fields? ──Yes──► ValueError
         │
         ▼
    Save to database
         │
         ├─► DB error? ──Yes──► Rollback + Exception
         │
         ▼
    Success ✓
```

---

## Status Logic (Phase 1)

### Covenant Status
```
Input: covenant.current_value, covenant.threshold, covenant.type

If type == "minimum":
    current < threshold           → BREACH 🔴
    current < threshold * 1.10    → AT RISK 🟡
    current >= threshold * 1.10   → OK 🟢

If type == "maximum":
    current > threshold           → BREACH 🔴
    current > threshold * 0.90    → AT RISK 🟡
    current <= threshold * 0.90   → OK 🟢
```

### Reporting Status
```
Input: reporting.next_due, today

days_left = next_due - today

days_left < 0      → OVERDUE 🔴
days_left <= 7     → DUE SOON 🟠
days_left <= 30    → UPCOMING 🔵
days_left > 30     → OK 🟢
```

### Renewal Status
```
Input: agreement.contract_end, today

days_left = contract_end - today

days_left < 0      → EXPIRED ⚫
days_left <= 7     → CRITICAL 🔴
days_left <= 30    → WARNING 🟠
days_left <= 90    → WATCH 🟡
days_left > 90     → OK 🟢
```

---

## API Integration

### Anthropic API Call
```python
client.messages.create(
    model="claude-sonnet-4",
    max_tokens=8000,
    temperature=0,  # Deterministic
    messages=[{
        "role": "user",
        "content": extraction_prompt
    }]
)
```

### Response Processing
```
API Response → Extract text from content[0]
            ↓
            Remove markdown code blocks if present
            ↓
            Parse as JSON
            ↓
            Return structured dict
```

---

## File Organization

```
obligation_tracker/
│
├── Input Layer
│   └── documents/              # User drops files here
│
├── Processing Layer
│   ├── extractor.py            # Extraction pipeline
│   ├── models.py               # Data models
│   └── monitoring.py           # Business logic
│
├── Data Layer
│   └── obligation_tracker.db   # SQLite database
│
├── Testing Layer
│   ├── test_extractor.py       # Unit tests
│   ├── validate_setup.py       # Setup validation
│   └── dummy_data.py           # Test data
│
├── Configuration Layer
│   ├── .env                    # Secrets (not in git)
│   ├── .env.example            # Template
│   └── requirements.txt        # Dependencies
│
└── Documentation Layer
    ├── README.md               # Main docs
    ├── USAGE_GUIDE.md          # How-to guide
    ├── QUICK_START.md          # Quick reference
    ├── ARCHITECTURE.md         # This file
    └── PHASE2_COMPLETE.md      # Implementation summary
```

---

## Future Architecture (Phase 3)

```
                    ┌──────────────────┐
                    │   Scheduler      │
                    │  (APScheduler)   │
                    └────────┬─────────┘
                             │
                    Daily at 8:00 AM
                             │
                             ▼
                    ┌──────────────────┐
                    │  monitoring.py   │
                    │  - Check covenants│
                    │  - Check reports │
                    │  - Check renewals│
                    └────────┬─────────┘
                             │
                    Alerts triggered?
                             │
                             ▼
                    ┌──────────────────┐
                    │    alerts.py     │
                    │  - Email alerts  │
                    │  - Notifications │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Finance Team    │
                    │  Inbox           │
                    └──────────────────┘
```

---

## Security Considerations

### API Key Management
```
.env file (not in git)
    ↓
Environment variables
    ↓
DocumentExtractor initialization
    ↓
Secure API calls
```

### Data Protection
- SQLite database (local file)
- No cloud storage
- Sensitive financial data stays on-premises

### Input Validation
- File type checking
- Size limits (implicit in LLM token limits)
- Schema validation
- SQL injection protection (SQLAlchemy ORM)

---

## Performance Characteristics

### Time Complexity
- Text extraction: O(n) where n = pages
- LLM analysis: O(1) per document (API call)
- Database save: O(m) where m = obligations

### Space Complexity
- Text storage: ~1KB per page
- Database: ~10KB per agreement
- Memory: ~50MB peak during processing

### Scalability
- Sequential processing (one document at a time)
- Can be parallelized for batch processing
- Database supports thousands of agreements

---

## Testing Strategy

### Unit Tests
```
test_extractor.py
    ├─► Test text extraction
    ├─► Test LLM extraction
    ├─► Test validation
    └─► Test database save
```

### Integration Tests
```
validate_setup.py
    ├─► Check dependencies
    ├─► Check configuration
    ├─► Check database
    └─► Check end-to-end flow
```

### Manual Testing
```
1. Process sample document
2. Verify extracted data
3. Check database records
4. Validate status calculations
```

---

## Deployment

### Local Development
```bash
git clone <repo>
pip install -r requirements.txt
cp .env.example .env
# Add API key
python validate_setup.py
python extractor.py
```

### Production Deployment
```bash
# Same as development, plus:
- Set up scheduled jobs (Phase 3)
- Configure email alerts (Phase 3)
- Set up monitoring/logging
- Regular database backups
```

---

## Monitoring & Observability

### Logging
- Console output for immediate feedback
- File logging (to be added in Phase 3)
- Error tracking

### Metrics
- Documents processed
- Extraction success rate
- API costs
- Processing time

### Alerts
- Extraction failures
- API errors
- Database errors
- Validation failures

---

This architecture supports the current Phase 2 implementation and is designed to scale into Phase 3 (alerts & scheduling) and beyond.
