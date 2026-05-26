# 🚀 Google Drive Auto-Sync Setup Guide

## Overview

This system automatically monitors a Google Drive folder for new PDF files and processes them without any manual intervention.

**Flow:**
1. Finance team drops PDF into Google Drive folder
2. Google Apps Script detects new file (every 10 minutes)
3. Script sends PDF to Vercel API
4. Vercel extracts data with AI
5. Data saved to database
6. Email notification sent
7. **ZERO CLICKS REQUIRED!**

---

## Step 1: Create Google Drive Folder (2 minutes)

1. **Go to Google Drive**: https://drive.google.com
2. **Create new folder**: "Financing Agreements" (or any name)
3. **Open the folder**
4. **Copy Folder ID** from URL:
   ```
   https://drive.google.com/drive/folders/1ABC123xyz...
                                            ^^^^^^^^^^^
                                            This is the Folder ID
   ```
5. **Save this ID** - you'll need it later

---

## Step 2: Setup Google Apps Script (10 minutes)

### 2.1 Create Script Project

1. **Go to**: https://script.google.com
2. **Click**: "New Project"
3. **Name it**: "Financing Tracker Sync"

### 2.2 Add Code

1. **Delete** default code
2. **Copy** entire content from `GoogleAppsScript.js` file
3. **Paste** into the editor

### 2.3 Configure Settings

Find the `CONFIG` section at the top and update:

```javascript
const CONFIG = {
  // Your folder ID from Step 1
  DRIVE_FOLDER_ID: '1ABC123xyz...',
  
  // Your Vercel URL (already set)
  API_ENDPOINT: 'https://financing-obligation-tracker-cj62zfaqi.vercel.app/api/sync/google-drive',
  
  // Generate a random secret
  API_SECRET: 'your-random-secret-here',
  
  // Email for notifications
  NOTIFICATION_EMAIL: 'your-email@example.com'
};
```

**Generate API_SECRET:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 2.4 Save and Authorize

1. **Click**: Save icon (💾)
2. **Click**: Run → "setup"
3. **Authorize** the script:
   - Click "Review permissions"
   - Choose your Google account
   - Click "Advanced" → "Go to Financing Tracker Sync (unsafe)"
   - Click "Allow"
4. **Check logs**: View → Logs
   - Should see "✅ Setup Complete"

---

## Step 3: Add API Secret to Vercel (2 minutes)

1. **Go to Vercel**: https://vercel.com/gilangpramana21/financing-obligation-tracker
2. **Click**: Settings → Environment Variables
3. **Add new variable**:
   ```
   Key: API_SECRET
   Value: [same secret from GoogleAppsScript.js CONFIG]
   ```
4. **Save**
5. **Redeploy**: Deployments → ... → Redeploy

---

## Step 4: Setup Trigger (3 minutes)

### 4.1 Create Time-Driven Trigger

1. **In Google Apps Script**, click: ⏰ Triggers (left sidebar)
2. **Click**: "+ Add Trigger"
3. **Configure**:
   - Choose function: `checkForNewPDFs`
   - Deployment: Head
   - Event source: **Time-driven**
   - Type: **Minutes timer**
   - Interval: **Every 10 minutes** (or hourly for less frequent checks)
4. **Click**: Save

### 4.2 Test the Trigger

1. **Upload a test PDF** to your Google Drive folder
2. **Wait 10 minutes** (or run manually: Run → "manualTest")
3. **Check**:
   - Google Apps Script logs (View → Executions)
   - Email notification
   - Vercel dashboard (should show new agreement)

---

## Step 5: Test End-to-End (5 minutes)

### Test Scenario:

1. **Drop PDF** into Google Drive folder
2. **Wait** 10 minutes (or less if you set shorter interval)
3. **Check email** - should receive notification
4. **Check dashboard** - https://financing-obligation-tracker-cj62zfaqi.vercel.app
5. **Verify** data is correct

---

## 🎉 Done! System is Now Fully Automated

### What Happens Now:

**Finance Team:**
- Just drops PDF into Google Drive folder
- That's it! No website, no clicks, nothing else

**System:**
- Automatically detects new PDF (every 10 minutes)
- Extracts all data with AI
- Saves to database
- Sends email notification
- Updates dashboard

**Result:**
- ✅ Zero manual data entry
- ✅ Zero clicks required
- ✅ Fully automated
- ✅ Real-time processing (10 min delay)
- ✅ Email notifications
- ✅ 100% free (Google Apps Script + Vercel free tier)

---

## 📊 Monitoring & Maintenance

### Check Script Execution

1. **Go to**: https://script.google.com
2. **Open your project**
3. **Click**: ⏰ Triggers
4. **View**: Executions tab
5. **See**: All runs, successes, failures

### View Logs

1. **In script editor**: View → Logs
2. **Or**: View → Executions → Click on execution → View logs

### Email Notifications

You'll receive emails for:
- ✅ Successful processing (with summary)
- ❌ Errors (with details)
- 📊 Daily summary (if multiple files processed)

---

## 🐛 Troubleshooting

### Script not running?

**Check:**
1. Trigger is enabled (⏰ Triggers tab)
2. Script has permissions (Run → "setup" again)
3. Folder ID is correct in CONFIG

### PDF not processing?

**Check:**
1. File is actually a PDF (not image or scan)
2. API_SECRET matches in both script and Vercel
3. Vercel logs for errors (Deployments → View Function Logs)

### No email notification?

**Check:**
1. NOTIFICATION_EMAIL is correct in CONFIG
2. Check spam folder
3. Gmail might block automated emails (whitelist script.google.com)

### API errors?

**Check:**
1. Vercel deployment is successful
2. API_SECRET environment variable is set in Vercel
3. GEMINI_API_KEY is set in Vercel
4. Database is connected (POSTGRES_URL)

---

## 🔧 Advanced Configuration

### Change Check Frequency

**More frequent** (every 5 minutes):
- Edit trigger → Interval: Every 5 minutes

**Less frequent** (hourly):
- Edit trigger → Type: Hour timer → Every hour

**Real-time** (not recommended, uses more quota):
- Use Google Drive API Push Notifications (complex setup)

### Process Multiple Folders

Duplicate the script and create separate triggers for each folder.

### Move Processed Files

Uncomment this line in `GoogleAppsScript.js`:
```javascript
// moveToProcessedFolder(file, folder);
```

Files will be moved to "Processed" subfolder after processing.

### Custom Notifications

Edit `sendSummaryNotification()` function in script to customize email format.

---

## 💰 Costs

**100% FREE:**
- ✅ Google Apps Script (free, unlimited)
- ✅ Google Drive (15 GB free)
- ✅ Vercel (free tier)
- ✅ Vercel Postgres (256 MB free)
- ✅ Gemini API (free tier)

**No monthly fees!**

---

## 📞 Support

**Issues?**
1. Check script logs
2. Check Vercel logs
3. Test API endpoint manually
4. Verify all environment variables

**Need help?**
- Check Google Apps Script documentation
- Check Vercel documentation
- Review error messages in logs

---

**🎉 Congratulations! Your system is now fully automated!**

Finance team can now just drop PDFs into Google Drive and everything happens automatically. Zero clicks, zero manual work!
