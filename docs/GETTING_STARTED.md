# Getting Started Checklist

Follow this checklist to get the Financing Obligation Tracker up and running.

---

## ☑️ Pre-Installation

- [ ] Python 3.11+ installed
- [ ] pip package manager available
- [ ] Internet connection (for API calls)
- [ ] Anthropic account created at https://console.anthropic.com/

---

## ☑️ Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed anthropic-0.18.0 sqlalchemy-2.0.0 ...
```

- [ ] All packages installed without errors

---

### 2. Configure API Key

```bash
# Copy template
cp .env.example .env
```

**Edit .env file:**
```
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
```

- [ ] .env file created
- [ ] API key added (get from https://console.anthropic.com/)
- [ ] API key is NOT the placeholder value

---

### 3. Validate Setup

```bash
python validate_setup.py
```

**Expected output:**
```
✅ PASS - Dependencies
✅ PASS - Environment
✅ PASS - Directories
✅ PASS - Database
✅ PASS - Extractor

🎉 All checks passed! System is ready to use.
```

- [ ] All 5 checks passed

---

## ☑️ First Test

### Option A: Test with Sample Text (No PDF needed)

```bash
python test_extractor.py
```

**What it does:**
- Extracts obligations from built-in sample agreement text
- Shows structured JSON output
- Offers to save to database

- [ ] Extraction completed successfully
- [ ] JSON output looks correct
- [ ] (Optional) Saved to database

---

### Option B: Test with Real Document

```bash
# 1. Add a PDF or Word document
cp /path/to/your/agreement.pdf documents/

# 2. Process it
python extractor.py documents/agreement.pdf
```

**Expected output:**
```
📄 Processing document: documents/agreement.pdf
   Extracting text from document...
   ✓ Extracted 45231 characters
   Analyzing with Claude...
   ✓ Extracted obligations from [Financier Name]
   Saving to database...
✅ Successfully saved agreement: [Agreement Name]
   📊 X reporting obligations
   📈 Y covenants
   📋 Z other obligations
✅ Document processing complete (Agreement ID: 1)
```

- [ ] Document processed successfully
- [ ] Obligations extracted
- [ ] Data saved to database

---

## ☑️ Verify Database

```bash
# Check database was created
ls -lh obligation_tracker.db
```

**Expected:**
```
-rw-r--r--  1 user  staff   20K May 21 10:30 obligation_tracker.db
```

- [ ] Database file exists
- [ ] File size > 0 bytes

---

## ☑️ Batch Processing

```bash
# Add multiple documents
cp loan1.pdf loan2.pdf loan3.docx documents/

# Process all at once
python extractor.py
```

**Expected output:**
```
Found 3 document(s) to process

📄 Processing document: documents/loan1.pdf
✅ Document processing complete (Agreement ID: 1)

📄 Processing document: documents/loan2.pdf
✅ Document processing complete (Agreement ID: 2)

📄 Processing document: documents/loan3.docx
✅ Document processing complete (Agreement ID: 3)
```

- [ ] All documents processed
- [ ] No errors
- [ ] Multiple agreements in database

---

## ☑️ Next Steps

### Phase 1: View Dashboard (To be built)
```bash
streamlit run dashboard.py
```

- [ ] Dashboard opens in browser
- [ ] Extracted agreements visible
- [ ] Status indicators working

### Phase 2: Regular Usage
- [ ] Create workflow for adding new agreements
- [ ] Set up folder monitoring
- [ ] Document extraction process for team

### Phase 3: Alerts & Automation (Future)
- [ ] Configure email alerts
- [ ] Set up daily scheduler
- [ ] Define alert rules

---

## ☑️ Troubleshooting Checklist

### If validation fails:

**Dependencies issue:**
```bash
pip install -r requirements.txt --upgrade
```

**API key issue:**
```bash
# Check .env file exists
cat .env

# Verify key format (should start with sk-ant-)
# Get new key from: https://console.anthropic.com/
```

**PDF extraction issue:**
```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils
```

**Database issue:**
```bash
# Remove and recreate
rm obligation_tracker.db
python validate_setup.py
```

---

## ☑️ Common Issues

### Issue: "ANTHROPIC_API_KEY not found"
- [ ] .env file exists in project root
- [ ] .env contains ANTHROPIC_API_KEY=...
- [ ] No spaces around the = sign
- [ ] Key is not the placeholder value

### Issue: "Failed to extract text from PDF"
- [ ] PDF is not password-protected
- [ ] PDF is not a scanned image (text must be selectable)
- [ ] Poppler installed (for pdfplumber)
- [ ] Try converting to Word format

### Issue: "Missing required field"
- [ ] Document contains all required information
- [ ] Document is a financing agreement (not other type)
- [ ] Text extraction worked (check extracted text)
- [ ] Try adjusting extraction prompt

### Issue: API rate limit or cost concerns
- [ ] Check usage at https://console.anthropic.com/
- [ ] Process documents in smaller batches
- [ ] Estimate cost before processing large batches
- [ ] Consider caching results

---

## ☑️ Success Criteria

You're ready to use the system when:

- [x] All dependencies installed
- [x] API key configured
- [x] Validation passes (5/5 checks)
- [x] Test extraction works
- [x] Database created
- [x] At least one document processed successfully

---

## ☑️ Quick Reference

### Process single document
```bash
python extractor.py documents/agreement.pdf
```

### Process all documents
```bash
python extractor.py
```

### Test without PDF
```bash
python test_extractor.py
```

### Validate setup
```bash
python validate_setup.py
```

### Load dummy data
```bash
python ingest.py
```

### View dashboard (Phase 1)
```bash
streamlit run dashboard.py
```

---

## ☑️ Documentation Reference

- **Quick start**: `QUICK_START.md` (5 minutes)
- **Detailed usage**: `USAGE_GUIDE.md` (comprehensive)
- **Architecture**: `ARCHITECTURE.md` (technical details)
- **Main docs**: `README.md` (overview)
- **Phase 2 summary**: `PHASE2_COMPLETE.md` (what was built)

---

## ☑️ Support

If you're stuck:

1. [ ] Read error message carefully
2. [ ] Check relevant documentation file
3. [ ] Run `python validate_setup.py`
4. [ ] Try `python test_extractor.py` first
5. [ ] Check API key and .env file
6. [ ] Review troubleshooting section above
7. [ ] Contact development team

---

## ☑️ Ready to Go!

Once all checks pass, you're ready to:

✅ Extract obligations from financing agreements  
✅ Monitor covenant compliance  
✅ Track reporting deadlines  
✅ Get renewal alerts  
✅ Automate obligation management  

**Start processing your agreements now!**

```bash
# Add your first agreement
cp /path/to/agreement.pdf documents/

# Process it
python extractor.py

# Success! 🎉
```
