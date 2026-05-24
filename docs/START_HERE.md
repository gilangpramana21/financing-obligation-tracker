# 🚀 START HERE

## Financing Obligation Tracker - Phase 2 Complete

Welcome! This project automatically extracts obligations from financing agreement PDFs using AI.

---

## ⚡ Quick Start (5 Minutes)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure (GRATIS)
cp .env.example .env
# Edit .env and add your Gemini API key from https://makersuite.google.com/app/apikey

# 3. Validate
python validate_setup.py

# 4. Test
python test_extractor.py

# 5. Process your documents
cp /path/to/agreement.pdf documents/
python extractor.py
```

---

## 📚 Documentation Guide

**New to the project?**
→ Read `GETTING_STARTED.md` for step-by-step setup

**Want quick reference?**
→ Read `QUICK_START.md` for essential commands

**Need detailed usage?**
→ Read `USAGE_GUIDE.md` for comprehensive guide

**Want full overview?**
→ Read `README.md` for complete documentation

**Interested in architecture?**
→ Read `ARCHITECTURE.md` for technical details

**Want a summary?**
→ Read `PROJECT_SUMMARY.txt` for quick overview

---

## 🎯 What This Does

Automatically extracts from financing agreements:
- ✅ Agreement details (financier, amount, dates)
- ✅ Reporting obligations (what, when, how often)
- ✅ Financial covenants (thresholds, metrics)
- ✅ Other obligations (notifications, approvals, restrictions)

---

## 📁 Project Structure

```
obligation_tracker/
├── documents/           # Drop PDF/Word files here
├── extractor.py         # Main extraction script ⭐
├── test_extractor.py    # Test without real PDFs
├── validate_setup.py    # Check your setup
├── models.py            # Database schema
├── monitoring.py        # Status logic
├── .env.example         # Config template
└── [documentation files]
```

---

## 🔧 Key Commands

```bash
# Validate setup
python validate_setup.py

# Test extraction (no PDF needed)
python test_extractor.py

# Process single document
python extractor.py documents/agreement.pdf

# Process all documents
python extractor.py

# Load dummy data for testing
python ingest.py
```

---

## ❓ Need Help?

1. Run `python validate_setup.py` to check configuration
2. Check `GETTING_STARTED.md` for troubleshooting
3. Review error messages carefully
4. See `USAGE_GUIDE.md` for detailed help

---

## 💰 Cost

**GRATIS** - Menggunakan Gemini 1.5 Flash (free tier: 1,500 docs/day)
**Opsional:** Claude Sonnet 4 (~$0.20-0.50/doc) jika butuh

---

## ✅ Success Checklist

- [ ] Dependencies installed
- [ ] API key configured in .env
- [ ] Validation passes (5/5 checks)
- [ ] Test extraction works
- [ ] First document processed

---

## 🎉 Ready to Go!

Once setup is complete:
1. Add your financing agreements to `documents/`
2. Run `python extractor.py`
3. AI extracts all obligations automatically
4. Data saved to database
5. Ready for monitoring!

---

**Next:** Read `GETTING_STARTED.md` for detailed setup instructions.
