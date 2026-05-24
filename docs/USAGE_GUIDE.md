# Financing Obligation Tracker - Usage Guide

## Phase 2: Document Extraction with AI

This guide covers how to use the AI-powered document extraction system to automatically extract obligations from financing agreement PDFs and Word documents.

---

## Prerequisites

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Anthropic API Key

1. Visit [https://console.anthropic.com/](https://console.anthropic.com/)
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy the key

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# Replace 'your_api_key_here' with your actual key
nano .env
```

Your `.env` file should look like:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
```

---

## How It Works

The extraction pipeline has three stages:

```
PDF/Word Document
    ↓
1. TEXT EXTRACTION (pdfplumber/python-docx)
    ↓
2. AI ANALYSIS (Claude Sonnet 4)
    ↓
3. DATABASE STORAGE (SQLite)
```

### What Gets Extracted

The AI identifies and extracts:

1. **Agreement Metadata**
   - Financier name
   - Agreement name
   - Contract start/end dates
   - Facility amount and currency

2. **Reporting Obligations**
   - Report names
   - Frequency (monthly/quarterly/semi-annual/annual)
   - Due dates
   - Descriptions

3. **Financial Covenants**
   - Covenant names
   - Type (minimum/maximum)
   - Metrics being measured
   - Threshold values
   - Units (IDR/USD/ratio/percent)

4. **Other Obligations**
   - Notifications required
   - Approvals needed
   - Restrictions
   - Ongoing actions

---

## Usage Methods

### Method 1: Process All Documents in Folder

```bash
# Place your PDF/Word files in the documents/ folder
cp /path/to/your/agreement.pdf documents/

# Run the extractor (processes all files)
python extractor.py
```

Output:
```
Found 3 document(s) to process

📄 Processing document: documents/loan_agreement.pdf
   Extracting text from document...
   ✓ Extracted 45231 characters
   Analyzing with Claude...
   ✓ Extracted obligations from Bank Mandiri
   Saving to database...
✅ Successfully saved agreement: Term Loan Facility Agreement
   📊 3 reporting obligations
   📈 4 covenants
   📋 5 other obligations
✅ Document processing complete (Agreement ID: 1)
```

### Method 2: Process Single Document

```bash
# Process a specific file
python extractor.py documents/my_agreement.pdf
```

### Method 3: Test with Sample Text

```bash
# Test the extraction with built-in sample text
python test_extractor.py
```

This will:
1. Extract obligations from sample agreement text
2. Display the structured JSON output
3. Show validation results
4. Offer to save to database

---

## Understanding the Output

### Extracted JSON Structure

```json
{
  "financier": "PT Bank Central Asia Tbk",
  "agreement_name": "Term Loan Facility Agreement",
  "contract_start": "2024-01-15",
  "contract_end": "2029-01-15",
  "facility_amount": 75000000000,
  "currency": "IDR",
  "reporting_obligations": [
    {
      "report_name": "Quarterly Financial Statements",
      "frequency": "quarterly",
      "due_day": 45,
      "description": "Unaudited quarterly financial statements",
      "next_due": "2026-08-15"
    }
  ],
  "covenants": [
    {
      "name": "Minimum Current Ratio",
      "type": "minimum",
      "metric": "Current Assets / Current Liabilities",
      "threshold": 1.2,
      "unit": "ratio",
      "description": "Maintain Current Ratio of not less than 1.2x"
    }
  ],
  "other_obligations": [
    {
      "category": "Notification",
      "description": "Notify lender within 10 days of management changes",
      "is_ongoing": true
    }
  ]
}
```

### Database Storage

After extraction, data is stored in `obligation_tracker.db`:

**Tables:**
- `agreements` - Master agreement records
- `reporting_obligations` - All reporting requirements
- `covenants` - Financial covenants to monitor
- `other_obligations` - Notifications, approvals, restrictions

---

## Programmatic Usage

### Use in Your Own Scripts

```python
from extractor import DocumentExtractor

# Initialize extractor
extractor = DocumentExtractor()

# Process a document
agreement_id = extractor.process_document('documents/loan.pdf')

print(f"Created agreement with ID: {agreement_id}")
```

### Extract Without Saving

```python
from extractor import DocumentExtractor

extractor = DocumentExtractor()

# Just extract text
text = extractor.extract_text('documents/agreement.pdf')

# Extract structured data (doesn't save to DB)
data = extractor.extract_obligations_from_text(text)

# Now you have the data as a Python dict
print(data['financier'])
print(f"Found {len(data['covenants'])} covenants")
```

### Batch Processing with Error Handling

```python
from pathlib import Path
from extractor import DocumentExtractor

extractor = DocumentExtractor()
documents = Path('documents').glob('*.pdf')

results = []
errors = []

for doc in documents:
    try:
        agreement_id = extractor.process_document(str(doc))
        results.append((doc.name, agreement_id))
    except Exception as e:
        errors.append((doc.name, str(e)))

print(f"✅ Processed: {len(results)}")
print(f"❌ Failed: {len(errors)}")
```

---

## Troubleshooting

### Issue: "ANTHROPIC_API_KEY not found"

**Solution:**
```bash
# Check if .env file exists
ls -la .env

# If not, create it
cp .env.example .env

# Edit and add your key
nano .env
```

### Issue: PDF text extraction fails

**Symptoms:**
```
⚠️  pdfplumber failed, trying PyMuPDF: ...
Failed to extract text from PDF: ...
```

**Solutions:**

1. **Install system dependencies:**
   ```bash
   # macOS
   brew install poppler

   # Ubuntu/Debian
   sudo apt-get install poppler-utils

   # Windows
   # Download from: https://github.com/oschwartz10612/poppler-windows
   ```

2. **Try different PDF:**
   - Scanned PDFs (images) won't work - need OCR
   - Password-protected PDFs need to be unlocked first
   - Some PDFs have text extraction disabled

3. **Convert to Word:**
   - Open PDF in Adobe/Preview
   - Export as Word document
   - Process the .docx file instead

### Issue: LLM returns incomplete data

**Symptoms:**
```
Missing required field: contract_end
```

**Solutions:**

1. **Check document quality:**
   ```python
   from extractor import DocumentExtractor
   
   extractor = DocumentExtractor()
   text = extractor.extract_text('documents/agreement.pdf')
   
   # Review extracted text
   print(text[:1000])  # First 1000 characters
   ```

2. **Improve extraction prompt:**
   - Edit `extractor.py`
   - Modify `build_extraction_prompt()` method
   - Add more specific instructions for your document format

3. **Manual correction:**
   ```python
   # Extract data
   data = extractor.extract_obligations_from_text(text)
   
   # Fix missing fields
   if not data.get('contract_end'):
       data['contract_end'] = '2029-12-31'
   
   # Save manually
   extractor.save_to_database(data)
   ```

### Issue: API rate limits or costs

**Claude API Limits:**
- Free tier: Limited requests per day
- Paid tier: Higher limits

**Cost Management:**

1. **Estimate before processing:**
   ```python
   text = extractor.extract_text('document.pdf')
   tokens = len(text) / 4  # Rough estimate
   cost = (tokens / 1_000_000) * 3  # $3 per million input tokens
   print(f"Estimated cost: ${cost:.4f}")
   ```

2. **Process in batches:**
   - Don't process all documents at once
   - Process 5-10 at a time
   - Monitor costs in Anthropic console

3. **Cache results:**
   - Save extracted JSON to files
   - Don't re-process same document

---

## Best Practices

### 1. Document Preparation

✅ **DO:**
- Use native PDFs (not scanned images)
- Ensure text is selectable in PDF
- Use clear, well-formatted documents
- Remove password protection

❌ **DON'T:**
- Use scanned/image PDFs without OCR
- Process encrypted documents
- Use corrupted files

### 2. Validation

Always review extracted data before using:

```python
# Extract
data = extractor.extract_obligations_from_text(text)

# Review
print(json.dumps(data, indent=2))

# Validate key fields
assert data['financier'], "Missing financier"
assert data['facility_amount'] > 0, "Invalid amount"
assert len(data['covenants']) > 0, "No covenants found"

# Then save
extractor.save_to_database(data)
```

### 3. Backup

```bash
# Backup database before bulk processing
cp obligation_tracker.db obligation_tracker.db.backup

# Process documents
python extractor.py

# If something goes wrong, restore
cp obligation_tracker.db.backup obligation_tracker.db
```

### 4. Version Control

```bash
# Don't commit sensitive data
echo "*.db" >> .gitignore
echo ".env" >> .gitignore
echo "documents/*.pdf" >> .gitignore

# Do commit code and structure
git add extractor.py models.py requirements.txt
git commit -m "Add document extraction pipeline"
```

---

## Next Steps

After extracting obligations:

1. **View in Dashboard** (Phase 1)
   ```bash
   streamlit run dashboard.py
   ```

2. **Update Covenant Values**
   - Current values need to be updated with actual financials
   - Use dashboard input fields or CSV upload

3. **Set Up Alerts** (Phase 3)
   - Configure email notifications
   - Set up daily monitoring scheduler

4. **Monitor Compliance**
   - Review covenant status regularly
   - Track reporting deadlines
   - Watch renewal dates

---

## Support

For issues or questions:
1. Check this guide first
2. Review error messages carefully
3. Test with `test_extractor.py` sample
4. Contact development team

---

## Appendix: Sample Documents

### Creating Test PDFs

If you need sample documents for testing:

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_sample_pdf():
    c = canvas.Canvas("documents/sample_agreement.pdf", pagesize=letter)
    
    c.drawString(100, 750, "LOAN AGREEMENT")
    c.drawString(100, 730, "Lender: Sample Bank")
    c.drawString(100, 710, "Amount: USD 5,000,000")
    c.drawString(100, 690, "Maturity: December 31, 2028")
    
    c.drawString(100, 650, "COVENANTS:")
    c.drawString(100, 630, "1. Minimum DSCR: 1.25x")
    c.drawString(100, 610, "2. Maximum Leverage: 3.0x")
    
    c.save()

create_sample_pdf()
```

### Document Checklist

Before processing, ensure your document contains:
- [ ] Lender/financier name
- [ ] Facility amount and currency
- [ ] Contract dates (start and end)
- [ ] Reporting requirements section
- [ ] Financial covenants section
- [ ] Other obligations/undertakings section
