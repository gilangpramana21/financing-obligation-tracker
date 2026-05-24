# 📤 How to Upload PDF Financing Agreements

## Quick Start

1. **Open Dashboard**
   - Go to: http://localhost:8501
   - Navigate to the **"📤 Upload PDF"** tab

2. **Upload PDF Files**
   - Click "Browse files" or drag & drop PDF files
   - You can upload multiple PDFs at once
   - Supported format: PDF only

3. **Process Files**
   - Click the **"🚀 Process PDF(s)"** button
   - Wait for extraction to complete
   - Review the processing summary

4. **View Results**
   - Click **"🔄 Refresh Dashboard"** to see new data
   - Check other tabs for extracted obligations

## What Gets Extracted

### 📋 Agreement Details
- Financier name
- Agreement name/type
- Facility amount and currency
- Contract start and end dates

### 📊 Reporting Obligations
- Report names (e.g., "Quarterly Financial Statements")
- Frequency (monthly, quarterly, semi-annual, annual)
- Due dates (days after period end)
- Next submission due date
- Description

### 📈 Financial Covenants
- Covenant name (e.g., "Minimum DSCR")
- Type (minimum or maximum)
- Threshold value
- Metric/measurement basis
- Current value (if available)
- Description

### 📌 Other Obligations
- Category (Notification, Approval Required, Restriction, Action Required)
- Description
- Ongoing vs one-time status

## Supported Agreement Types

✅ **Term Loans**
✅ **Revolving Credit Facilities**
✅ **Islamic Financing** (Musharakah, Murabaha, etc.)
✅ **Project Financing**
✅ **Senior Secured Loans**
✅ **Infrastructure Financing**
✅ **Syndicated Loans**

## Supported Languages

- 🇬🇧 English
- 🇮🇩 Bahasa Indonesia
- 🌐 Mixed language documents

## Tips for Best Results

1. **PDF Quality**
   - Use clear, text-based PDFs (not scanned images)
   - Ensure text is selectable in the PDF

2. **Document Structure**
   - Well-structured agreements with clear sections work best
   - Standard financing agreement formats are recognized

3. **Multiple Files**
   - Upload multiple agreements at once for batch processing
   - Each agreement will be processed independently

4. **Duplicate Detection**
   - System checks for existing agreements
   - Won't create duplicates if same financier + agreement name exists

## Troubleshooting

### ❌ "Failed to extract data"
- Check if PDF is text-based (not scanned image)
- Verify PDF is a financing agreement document
- Try uploading one file at a time

### ⚠️ "Agreement already exists"
- This agreement is already in the database
- Check the other tabs to see existing data
- Delete old agreement first if you want to re-upload

### 🔄 "Data not showing"
- Click the "🔄 Refresh Dashboard" button
- Or manually refresh your browser (F5 or Cmd+R)

## Alternative: Command Line Upload

If you prefer command line, you can also use:

```bash
# Activate virtual environment
source venv/bin/activate

# Place PDF files in documents/ folder
cp your-agreement.pdf documents/

# Run ingest script
python ingest.py
```

## Need Help?

Check the example PDFs in the `documents/` folder to see what format works best.
