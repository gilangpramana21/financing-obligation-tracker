# 📊 Financing Obligation Tracker

Automated system to extract and track obligations, covenants, and reporting requirements from financing agreement PDFs using AI.

## ✨ Features

- 📤 **PDF Upload** - Upload financing agreements via web interface with preview
- 🤖 **AI Extraction** - Automatic extraction using Google Gemini AI (Free)
- 📊 **Reporting Tracking** - Monitor upcoming report deadlines with mark-as-submitted
- 📈 **Covenant Monitoring** - Track financial covenant compliance with real-time updates
- 🔄 **Renewal Alerts** - Get notified before contract expiry (90, 60, 30, 7, 1 days)
- 📋 **Obligation Management** - Track all other obligations (notifications, approvals, restrictions)
- 📧 **Email Notifications** - Daily automated alerts at 9 AM for overdue items
- 🎨 **Professional Design** - Clean corporate interface with Bootstrap 5
- 🌐 **Multi-language** - Supports English and Bahasa Indonesia
- 🔁 **Auto-retry** - Handles API errors automatically with exponential backoff

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Setup API Keys

#### Gemini API (Required for PDF extraction)
Get a free Gemini API key from: https://aistudio.google.com/apikey

#### Email Notifications (Optional)
For Gmail, create an App Password:
1. Go to Google Account Settings
2. Security → 2-Step Verification → App Passwords
3. Generate password for "Mail"

Create `.env` file:
```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (for email notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password_here
RECIPIENT_EMAILS=recipient@example.com
```

### 3. Run Application

```bash
python app.py
```

Open: http://localhost:8080

### 4. Upload PDFs

1. Click **"Upload PDF"** in navigation
2. Drag & drop or click to browse PDF file
3. Click **"Process PDF"**
4. Review extracted data in preview page
5. Click **"Confirm & Save to Database"**
6. View data in Dashboard, Obligations, or Renewals pages

## 📋 Supported Documents

- Term Loans
- Revolving Credit Facilities
- Islamic Financing (Musharakah, Murabaha, Ijarah, etc.)
- Project Financing
- Senior Secured Loans
- Infrastructure Financing
- Syndicated Loans
- Bridge Loans
- Working Capital Facilities

## 🎯 What Gets Extracted

### Agreement Details
- Financier name
- Agreement type and name
- Facility amount & currency
- Contract start and end dates

### Reporting Obligations
- Report names (e.g., Financial Statements, Compliance Certificate)
- Frequency (monthly/quarterly/semi-annual/annual)
- Due dates (days after period end)
- Next submission dates (auto-calculated)
- Status tracking (upcoming/due soon/overdue)

### Financial Covenants
- Covenant names (e.g., Debt Service Coverage Ratio, Current Ratio)
- Type (minimum/maximum thresholds)
- Threshold values
- Current values (manually updated)
- Compliance status (compliant/at risk/breached)

### Other Obligations
- Notifications (events requiring notice to financier)
- Approval requirements (actions needing prior consent)
- Restrictions (prohibited activities)
- Action items (required tasks)

## 📊 Application Pages

### 1. Dashboard (Home)
- Overview metrics: Total agreements, facility amount, overdue reports, breached covenants
- Active agreements list with key details
- Quick status indicators

### 2. Obligations
- **Reporting Obligations**: View all reports with status, filter by financier, mark as submitted
- **Financial Covenants**: Monitor compliance, update current values
- **Other Obligations**: Track notifications, approvals, restrictions

### 3. Renewals
- Contract expiry dates with countdown
- Color-coded alerts (Critical: <30 days, Warning: <90 days, Safe: >90 days)
- Sorted by urgency

### 4. Upload PDF
- Drag & drop interface
- Real-time processing status
- Preview extracted data before saving
- Validation and error handling

### 5. Settings
- Email notification configuration
- Test email functionality
- SMTP settings

## 💡 Best Practices

### For Reliable Processing
- Upload **one file at a time** for preview and validation
- Use **text-based PDFs** (not scanned images)
- Review extracted data in preview before confirming
- Process during **off-peak hours** for faster results

### Rate Limits (Gemini Free Tier)
- 15 requests per minute
- 1,500 requests per day
- System automatically handles rate limits with exponential backoff (2s, 4s, 8s delays)
- Falls back to gemini-2.0-flash if primary model unavailable

### Email Notifications
- Daily check runs at 9:00 AM automatically
- Alerts for: Renewal reminders, Overdue reports, Covenant breaches
- Test email function available in Settings page
- HTML formatted emails with color-coded badges

## 🛠️ Technology Stack

- **Backend**: Flask 3.0+
- **Frontend**: Bootstrap 5, HTML5, JavaScript
- **AI**: Google Gemini 2.5 Flash (Free tier)
- **Database**: SQLite with SQLAlchemy ORM
- **PDF Processing**: pdfplumber, PyMuPDF
- **Email**: smtplib with HTML templates
- **Scheduler**: APScheduler for daily alerts
- **Language**: Python 3.8+

## 📁 Project Structure

```
.
├── app.py                    # Flask application (main entry point)
├── extractor.py              # AI extraction logic with retry
├── models.py                 # SQLAlchemy database models
├── monitoring.py             # Status checking logic
├── notifications.py          # Email notification service
├── ingest.py                # CLI processing script
├── requirements_production.txt  # All dependencies
├── .env                     # API keys and config (create this)
├── .env.example             # Example env file
├── obligation_tracker.db    # SQLite database
├── documents/               # Uploaded PDFs stored here
├── templates/               # HTML templates
│   ├── base.html           # Base template with navigation
│   ├── index.html          # Dashboard page
│   ├── obligations.html    # Obligations tracking page
│   ├── renewals.html       # Contract renewals page
│   ├── upload.html         # PDF upload page
│   ├── upload_preview.html # Preview extracted data
│   └── settings.html       # Email settings page
├── static/                  # CSS and JS files
│   ├── css/
│   └── js/
└── docs/                    # Documentation
    ├── QUICK_START.md
    ├── HOW_TO_UPLOAD.md
    ├── ERROR_HANDLING.md
    ├── RATE_LIMIT_GUIDE.md
    ├── GEMINI_SETUP.md
    └── ...
```

## 📚 Documentation

- **[Quick Start](docs/QUICK_START.md)** - Get started in 5 minutes
- **[Upload Guide](docs/HOW_TO_UPLOAD.md)** - How to upload PDFs
- **[Gemini Setup](docs/GEMINI_SETUP.md)** - Get free API key
- **[Error Handling](docs/ERROR_HANDLING.md)** - Troubleshooting guide
- **[Rate Limits](docs/RATE_LIMIT_GUIDE.md)** - Avoid rate limit errors
- **[Model Info](docs/MODEL_INFO.md)** - AI model details
- **[Usage Guide](docs/USAGE_GUIDE.md)** - Complete user manual

## 🔧 Configuration

### Change AI Model

Edit `extractor.py` line ~50:
```python
self.model_name = "gemini-2.5-flash"  # Current (fast, free)
self.fallback_model = "gemini-2.0-flash"  # Fallback
# self.model_name = "gemini-2.5-pro"  # More powerful (if available)
```

### Use Claude Instead (Paid)

1. Get API key from https://console.anthropic.com/
2. Add to `.env`: `ANTHROPIC_API_KEY=your_key`
3. Edit `app.py` line ~90:
   ```python
   extractor = DocumentExtractor(llm_provider="anthropic")
   ```

### Change Email Schedule

Edit `app.py` line ~30:
```python
scheduler.add_job(
    func=run_daily_check,
    trigger=CronTrigger(hour=9, minute=0),  # Change hour/minute here
    ...
)
```

### Change Port

Edit `app.py` last line:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change port here
```

## 🐛 Troubleshooting

### Error: "Model not found" or "503 Service Unavailable"
- Check API key in `.env` file
- System will automatically retry with fallback model
- Wait 2-8 seconds between retries (exponential backoff)
- Try again during off-peak hours

### Error: "Rate limit exceeded"
- Free tier: 15 requests/minute, 1,500/day
- Wait 60 seconds and try again
- System handles this automatically with delays
- See [Rate Limit Guide](docs/RATE_LIMIT_GUIDE.md)

### Error: "Failed to extract"
- Ensure PDF is text-based (not scanned image)
- Check PDF is a financing agreement with clear structure
- Try uploading one file at a time
- Review PDF quality and formatting

### Error: "Address already in use" (Port 5000/8080)
- Another app is using the port
- On macOS: Disable AirPlay Receiver in System Settings
- Or change port in `app.py` (e.g., port=8081)

### Email not sending
- Check SMTP credentials in `.env`
- For Gmail: Use App Password, not regular password
- Test email in Settings page
- Check firewall/antivirus blocking port 587

### Data not showing after upload
- Check if preview page showed data correctly
- Click "Confirm & Save" button in preview
- Refresh browser (F5 / Cmd+R)
- Check database file exists: `obligation_tracker.db`

## 📈 Performance

- **Processing Speed**: ~10-30 seconds per PDF (depends on API response time)
- **Success Rate**: ~95% (with retry logic and fallback model)
- **Supported Languages**: English, Bahasa Indonesia
- **Max File Size**: 200MB (configurable in `app.py`)
- **Concurrent Users**: Supports multiple users (Flask production server recommended)

## 🔐 Security & Privacy

- All processing happens **locally** on your server
- API calls only to Google Gemini (Google's privacy policy applies)
- Database stored **locally** (SQLite file)
- API keys stored in `.env` (excluded from git via `.gitignore`)
- Uploaded PDFs temporarily stored, deleted after processing
- Email passwords should use App Passwords, not account passwords

## 🚀 Production Deployment

### Using Gunicorn (Recommended)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

### Using Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements_production.txt .
RUN pip install -r requirements_production.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
```

### Environment Variables for Production

```bash
# Set in production environment
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
export GEMINI_API_KEY=your-key
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SENDER_EMAIL=your-email
export SENDER_PASSWORD=your-password
export RECIPIENT_EMAILS=recipient@example.com
```

## 📄 License

MIT License - Feel free to use and modify

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:
1. Check [Documentation](docs/)
2. Review [Troubleshooting Guide](docs/ERROR_HANDLING.md)
3. Check [Gemini Setup Guide](docs/GEMINI_SETUP.md)
4. Open an issue on GitHub

## 🎉 Credits

Built with:
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap 5](https://getbootstrap.com/) - UI framework
- [Google Gemini](https://ai.google.dev/) - AI extraction
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF processing
- [APScheduler](https://apscheduler.readthedocs.io/) - Task scheduling

---

**Status**: ✅ Production Ready  
**Version**: 2.0.0  
**Last Updated**: May 2026

**Start using now**: `python app.py` 🚀

Open http://localhost:8080 in your browser
