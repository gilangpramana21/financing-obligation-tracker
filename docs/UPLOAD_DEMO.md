# 📤 Upload PDF Demo Guide

## Step-by-Step Visual Guide

### Step 1: Open Dashboard
```
🌐 Open your browser and go to:
   http://localhost:8501
```

### Step 2: Navigate to Upload Tab
```
Dashboard Layout:
┌─────────────────────────────────────────────────────┐
│  📊 Financing Obligation Tracker                    │
├─────────────────────────────────────────────────────┤
│  [📊 Reporting] [📈 Covenants] [📋 Other] [🔄 Renewals] [📤 Upload PDF] ← Click here!
└─────────────────────────────────────────────────────┘
```

### Step 3: Upload Your PDF
```
┌─────────────────────────────────────────────────────┐
│  📤 Upload Financing Agreement PDF                  │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  Choose PDF file(s)                        │    │
│  │  [Browse files] or drag & drop here        │    │
│  │                                             │    │
│  │  Accepted: .pdf files                      │    │
│  │  Multiple files: Yes                       │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  Selected files:                                    │
│  - 📄 Bank-Mandiri-Loan.pdf (2.3 MB)              │
│  - 📄 IFC-Agreement.pdf (1.8 MB)                   │
│                                                      │
│  [🚀 Process PDF(s)]  ← Click to start extraction  │
└─────────────────────────────────────────────────────┘
```

### Step 4: Processing
```
┌─────────────────────────────────────────────────────┐
│  Processing Bank-Mandiri-Loan.pdf...                │
│  ████████████████████░░░░░░░░░░ 60%                │
│                                                      │
│  ✅ Successfully processed: Bank-Mandiri-Loan.pdf   │
│  ⏳ Processing IFC-Agreement.pdf...                 │
└─────────────────────────────────────────────────────┘
```

### Step 5: Results Summary
```
┌─────────────────────────────────────────────────────┐
│  📊 Processing Summary                               │
│  ┌──────────┬──────────┬──────────┐                │
│  │ Total    │ Success  │ Errors   │                │
│  │ Files    │          │          │                │
│  ├──────────┼──────────┼──────────┤                │
│  │    2     │    2     │    0     │                │
│  └──────────┴──────────┴──────────┘                │
│                                                      │
│  ✅ Successfully processed: Bank-Mandiri-Loan.pdf   │
│  ✅ Successfully processed: IFC-Agreement.pdf       │
│                                                      │
│  🔄 Refresh the page to see new agreements          │
│  [🔄 Refresh Dashboard]  ← Click to reload          │
└─────────────────────────────────────────────────────┘
```

### Step 6: View Extracted Data
```
After refresh, check other tabs:

📊 Reporting Tab:
  - Shows all extracted reporting obligations
  - Due dates automatically calculated
  - Status indicators (overdue, due soon, upcoming)

📈 Covenants Tab:
  - Financial covenants with thresholds
  - Current values (can be updated)
  - Status: OK, At Risk, or Breach

📋 Other Obligations Tab:
  - Grouped by category
  - Notifications, approvals, restrictions

🔄 Renewals Tab:
  - Contract expiry tracking
  - Days until renewal
  - Critical alerts
```

## Example: What Gets Extracted

### From This PDF Section:
```
3. REPORTING OBLIGATIONS
3.1 Quarterly Financial Statements
    Submit within 45 days after quarter end.
    Next due: 15 May 2026

4. FINANCIAL COVENANTS
    Minimum DSCR: 1.25x
    Current: 1.30x
```

### Becomes This Data:
```
📊 Reporting Obligation:
   Name: Quarterly Financial Statements
   Frequency: Quarterly
   Due: 45 days after period end
   Next Due: 2026-05-15
   Status: 🟢 Upcoming (23 days)

📈 Covenant:
   Name: Minimum DSCR
   Type: Minimum
   Threshold: 1.25
   Current: 1.30
   Status: 🟢 OK (+4.0% margin)
```

## Quick Test

Want to test right now? Use the sample PDFs already in your system:

1. The system already has 3 sample agreements loaded
2. Try uploading a new PDF to see the extraction in action
3. Or check the existing data in the other tabs

## Pro Tips

💡 **Batch Upload**: Upload multiple PDFs at once to save time

💡 **Duplicate Check**: System won't create duplicates - safe to re-upload

💡 **Auto-Calculate**: Due dates are automatically calculated based on frequency

💡 **Real-time Updates**: Update covenant values directly in the dashboard

💡 **Export Ready**: All data stored in SQLite database for easy export

## Current Status

Your system currently has:
- ✅ 3 Agreements loaded (Bank Mandiri, BRI Syariah, IFC)
- ✅ 8 Reporting obligations tracked
- ✅ 8 Financial covenants monitored
- ✅ 9 Other obligations recorded

Ready to add more! 🚀
