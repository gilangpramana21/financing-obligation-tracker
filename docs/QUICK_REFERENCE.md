# 🚀 Quick Reference Card

## 📤 Upload PDF - 3 Simple Steps

```
1. Open → http://localhost:8501
2. Click → "📤 Upload PDF" tab
3. Upload → Drag & drop or browse PDF files
4. Process → Click "🚀 Process PDF(s)"
5. Refresh → Click "🔄 Refresh Dashboard"
```

## 🎯 What You Can Do

| Feature | Location | Action |
|---------|----------|--------|
| **Upload new PDFs** | 📤 Upload PDF tab | Drag & drop or browse |
| **View upcoming reports** | 📊 Reporting tab | See due dates & status |
| **Monitor covenants** | 📈 Covenants tab | Check compliance status |
| **Update covenant values** | 📈 Covenants tab | Enter new values & save |
| **Check renewals** | 🔄 Renewals tab | See contract expiry dates |
| **View other obligations** | 📋 Other Obligations | See notifications & approvals |

## 🎨 Status Indicators

### Reporting Status
- 🔴 **Overdue** - Past due date
- 🟠 **Due Soon** - Within 7 days
- 🔵 **Upcoming** - Within 30 days
- 🟢 **OK** - More than 30 days

### Covenant Status
- 🔴 **Breach** - Threshold violated
- 🟡 **At Risk** - Within 10% of threshold
- 🟢 **OK** - Compliant
- ⚪ **Unknown** - No current value set

### Renewal Status
- 🔴 **Expired** - Past maturity date
- 🔴 **Critical** - Less than 30 days
- 🟠 **Warning** - 30-90 days
- 🟡 **Watch** - 90-180 days
- 🟢 **OK** - More than 180 days

## 📊 Dashboard Metrics

Top row shows at-a-glance summary:
- **Covenant Alerts** - Breaches & at-risk covenants
- **Reporting Due** - Overdue & due soon reports
- **Renewal Alerts** - Contracts needing attention
- **Other Obligations** - Total ongoing obligations

## 🔧 Common Tasks

### Add New Agreement
```bash
1. Go to "📤 Upload PDF" tab
2. Upload PDF file
3. Click "Process"
4. Refresh dashboard
```

### Update Covenant Value
```bash
1. Go to "📈 Covenants" tab
2. Expand covenant card
3. Enter new value
4. Click "Update"
```

### Check What's Due Soon
```bash
1. Go to "📊 Reporting" tab
2. Look for 🔴 or 🟠 indicators
3. Expand to see details
```

### Filter by Financier
```bash
1. Use sidebar dropdown
2. Select specific financier
3. View filtered data
```

## 📁 File Locations

```
Project Structure:
├── dashboard.py          # Main dashboard app
├── ingest.py            # PDF processing script
├── extractor.py         # LLM extraction logic
├── models.py            # Database models
├── monitoring.py        # Status checking logic
├── documents/           # Place PDFs here for CLI
├── obligation_tracker.db # SQLite database
└── .env                 # API keys (Gemini/Claude)
```

## 🔑 Environment Setup

Required in `.env` file:
```bash
# Choose ONE:
GEMINI_API_KEY=your_key_here    # For Google Gemini
# OR
ANTHROPIC_API_KEY=your_key_here # For Claude
```

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Dashboard won't start | Run: `source venv/bin/activate && streamlit run dashboard.py` |
| PDF extraction fails | Check `.env` has valid API key |
| Data not showing | Click "🔄 Refresh Dashboard" button |
| Duplicate error | Agreement already exists - check other tabs |
| No covenants showing | PDF may not have covenant section |

## 📞 Command Line Alternative

```bash
# Activate environment
source venv/bin/activate

# Place PDFs in documents/ folder
cp your-file.pdf documents/

# Run extraction
python ingest.py

# Start dashboard
streamlit run dashboard.py
```

## 💡 Pro Tips

1. **Batch Processing**: Upload multiple PDFs at once
2. **Auto-Refresh**: Dashboard updates when you change values
3. **Expand All**: Click items with 🔴 or 🟠 to see urgent items
4. **Filter View**: Use sidebar to focus on one financier
5. **Export Data**: Database is SQLite - easy to export

## 🎯 Current System Status

```
✅ Dashboard: http://localhost:8501
✅ Database: obligation_tracker.db
✅ Sample Data: 3 agreements loaded
✅ Upload Feature: Active in "📤 Upload PDF" tab
```

## 📚 More Help

- `HOW_TO_UPLOAD.md` - Detailed upload guide
- `UPLOAD_DEMO.md` - Visual step-by-step demo
- `USAGE_GUIDE.md` - Complete user manual
- `TROUBLESHOOTING_GEMINI.md` - API setup help

---

**Ready to go!** Open http://localhost:8501 and start tracking! 🚀
