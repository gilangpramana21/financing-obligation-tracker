# Quick Start Guide - Document Extraction

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key (GRATIS)
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your Gemini API key (FREE)
# Get key from: https://makersuite.google.com/app/apikey
```

### 3. Test the Extractor
```bash
# Test with sample text (no PDF needed)
python test_extractor.py
```

### 4. Process Real Documents
```bash
# Drop your PDF/Word files into documents/ folder
cp /path/to/agreement.pdf documents/

# Run extraction
python extractor.py
```

---

## Common Commands

```bash
# Process all documents in folder
python extractor.py

# Process specific document
python extractor.py documents/loan_agreement.pdf

# Test with sample text
python test_extractor.py

# Load dummy data (for testing without real docs)
python ingest.py

# View in dashboard (Phase 1)
streamlit run dashboard.py
```

---

## What Gets Extracted

✅ Agreement details (financier, amount, dates)  
✅ Reporting obligations (what, when, how often)  
✅ Financial covenants (thresholds, metrics)  
✅ Other obligations (notifications, approvals, restrictions)

---

## File Structure

```
obligation_tracker/
├── documents/           ← Drop PDF/Word files here
├── extractor.py         ← Main extraction script
├── test_extractor.py    ← Test without real PDFs
├── models.py            ← Database schema
├── monitoring.py        ← Status logic
├── ingest.py            ← Load dummy data
├── .env                 ← Your API key (create this)
└── obligation_tracker.db ← SQLite database (auto-created)
```

---

## Troubleshooting

**"ANTHROPIC_API_KEY not found"**
→ Create `.env` file with your API key

**PDF extraction fails**
→ Install poppler: `brew install poppler` (macOS)

**Incomplete extraction**
→ Check if PDF text is selectable (not scanned image)

---

## Cost Estimate

**Gemini (Default):** GRATIS - 1,500 docs/day
**Claude (Optional):** ~$0.20-0.50 per 50-100 page document

---

## Next Steps

1. Extract your agreements: `python extractor.py`
2. View dashboard: `streamlit run dashboard.py`
3. Update covenant values with actual financials
4. Set up alerts (Phase 3)

---

**Full documentation:** See `USAGE_GUIDE.md` and `README.md`
