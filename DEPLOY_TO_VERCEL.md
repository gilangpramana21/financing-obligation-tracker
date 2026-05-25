# 🚀 Deploy to Vercel - Complete Guide

## 📋 Prerequisites

1. GitHub account (already done ✅)
2. Vercel account (free) - https://vercel.com
3. Cloudinary account (free) - https://cloudinary.com
4. Gemini API key (already have ✅)

---

## Step 1: Deploy to Vercel (5 minutes)

### 1.1 Import Project

1. Go to: **https://vercel.com/new**
2. Login with GitHub
3. Click **"Import Project"**
4. Search for: `gilangpramana21/financing-obligation-tracker`
5. Click **"Import"**

### 1.2 Configure Project

- **Framework Preset**: Other
- **Root Directory**: `./`
- **Build Command**: (leave empty)
- **Output Directory**: (leave empty)
- **Install Command**: `pip install -r requirements.txt`

### 1.3 Add Environment Variables

Click **"Environment Variables"** and add:

```
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_random_secret_key_here
VERCEL=true
```

### 1.4 Deploy

1. Click **"Deploy"**
2. Wait 2-3 minutes
3. You'll get URL like: `https://financing-obligation-tracker.vercel.app`

**⚠️ Website akan jalan tapi database belum ada! Lanjut ke Step 2.**

---

## Step 2: Setup Vercel Postgres (5 minutes)

### 2.1 Create Database

1. Go to your project dashboard in Vercel
2. Click tab **"Storage"**
3. Click **"Create Database"**
4. Select **"Postgres"**
5. Choose region: **US East (closest to your users)**
6. Click **"Create"**

### 2.2 Connect Database

Vercel will automatically add these environment variables:
- `POSTGRES_URL`
- `POSTGRES_PRISMA_URL`
- `POSTGRES_URL_NON_POOLING`
- `POSTGRES_USER`
- `POSTGRES_HOST`
- `POSTGRES_PASSWORD`
- `POSTGRES_DATABASE`

**No action needed!** Code sudah configured untuk detect `POSTGRES_URL`.

### 2.3 Initialize Database

1. Go to **Storage** tab → **Data** tab
2. Click **"Query"**
3. Run this SQL to create tables:

```sql
-- Create agreements table
CREATE TABLE agreements (
    id SERIAL PRIMARY KEY,
    financier VARCHAR(200) NOT NULL,
    agreement_name VARCHAR(300) NOT NULL,
    contract_start DATE NOT NULL,
    contract_end DATE NOT NULL,
    facility_amount FLOAT NOT NULL,
    currency VARCHAR(10) NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE
);

-- Create reporting_obligations table
CREATE TABLE reporting_obligations (
    id SERIAL PRIMARY KEY,
    agreement_id INTEGER REFERENCES agreements(id) ON DELETE CASCADE,
    report_name VARCHAR(300) NOT NULL,
    frequency VARCHAR(50) NOT NULL,
    due_day INTEGER NOT NULL,
    description TEXT,
    next_due DATE NOT NULL
);

-- Create covenants table
CREATE TABLE covenants (
    id SERIAL PRIMARY KEY,
    agreement_id INTEGER REFERENCES agreements(id) ON DELETE CASCADE,
    name VARCHAR(300) NOT NULL,
    type VARCHAR(20) NOT NULL,
    metric VARCHAR(200) NOT NULL,
    threshold FLOAT NOT NULL,
    unit VARCHAR(50) NOT NULL,
    description TEXT,
    current_value FLOAT,
    last_updated DATE
);

-- Create other_obligations table
CREATE TABLE other_obligations (
    id SERIAL PRIMARY KEY,
    agreement_id INTEGER REFERENCES agreements(id) ON DELETE CASCADE,
    category VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    is_ongoing BOOLEAN DEFAULT TRUE
);
```

4. Click **"Run Query"**

**✅ Database ready!**

---

## Step 3: Setup Cloudinary (5 minutes)

### 3.1 Create Account

1. Go to: **https://cloudinary.com/users/register/free**
2. Sign up (free tier: 25 GB storage, 25 GB bandwidth/month)
3. Verify email

### 3.2 Get API Credentials

1. Go to Dashboard: https://console.cloudinary.com/
2. You'll see:
   - **Cloud Name**: `dxxxxx`
   - **API Key**: `123456789012345`
   - **API Secret**: `abcdefghijklmnopqrstuvwxyz`

### 3.3 Add to Vercel

1. Go back to Vercel project
2. Click **"Settings"** → **"Environment Variables"**
3. Add these:

```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

4. Click **"Save"**

### 3.4 Redeploy

1. Go to **"Deployments"** tab
2. Click **"..."** on latest deployment
3. Click **"Redeploy"**

**✅ PDF upload now works!**

---

## Step 4: Setup Email Notifications (Optional, 3 minutes)

### 4.1 Add Email Environment Variables

Go to **Settings** → **Environment Variables**, add:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_gmail_app_password
RECIPIENT_EMAILS=recipient@example.com
```

### 4.2 Setup Cron Secret

Add one more variable:

```
CRON_SECRET=your_random_secret_here
```

Generate random secret:
```bash
openssl rand -base64 32
```

### 4.3 Enable Cron Jobs

Vercel Cron is already configured in `vercel.json`:
- Runs daily at 9:00 AM UTC
- Calls `/api/cron/daily-check` endpoint
- Sends email alerts automatically

**✅ Email alerts now work!**

---

## Step 5: Test Everything (5 minutes)

### 5.1 Test Homepage

Visit: `https://your-project.vercel.app`

Should show:
- ✅ Dashboard with 0 agreements
- ✅ Navigation working
- ✅ No errors

### 5.2 Test Upload

1. Go to **Upload** page
2. Upload a PDF (use sample: `documents/01_Bank_Mandiri_Term_Loan_Agreement.pdf`)
3. Should show preview page
4. Click **"Confirm & Save"**
5. Should redirect to dashboard
6. Check if data appears

### 5.3 Test Database

1. Go to **Obligations** page
2. Should show uploaded data
3. Try **"Mark Submitted"** button
4. Should update next due date

### 5.4 Test Email (Optional)

1. Go to **Settings** page
2. Click **"Send Test Alert"**
3. Check email inbox

---

## ✅ Deployment Complete!

Your app is now live at: `https://your-project.vercel.app`

### What's Working:

- ✅ Website online and accessible
- ✅ PostgreSQL database (persistent)
- ✅ PDF upload via Cloudinary (persistent)
- ✅ AI extraction with Gemini
- ✅ All CRUD operations
- ✅ Email notifications (daily at 9 AM UTC)
- ✅ Auto-scaling
- ✅ HTTPS enabled
- ✅ Custom domain support

---

## 🎨 Optional: Add Custom Domain

1. Go to **Settings** → **Domains**
2. Add your domain (e.g., `tracker.yourdomain.com`)
3. Update DNS records as instructed
4. Wait for SSL certificate (automatic)

---

## 📊 Monitoring

### View Logs

1. Go to **Deployments** tab
2. Click on deployment
3. Click **"View Function Logs"**

### View Database

1. Go to **Storage** tab
2. Click **"Data"** tab
3. Browse tables and data

### View Usage

1. Go to **Analytics** tab
2. See requests, bandwidth, function executions

---

## 🐛 Troubleshooting

### Error: "Module not found"

**Solution**: Redeploy
```bash
git push origin main
```

### Error: "Database connection failed"

**Solution**: Check `POSTGRES_URL` in environment variables

### Error: "Cloudinary upload failed"

**Solution**: Check Cloudinary credentials in environment variables

### PDF upload not working

**Solution**: 
1. Check Cloudinary credentials
2. Check file size (max 10MB on free tier)
3. Check logs in Vercel dashboard

### Email not sending

**Solution**:
1. Check SMTP credentials
2. Use Gmail App Password (not regular password)
3. Check logs for error messages

---

## 💰 Costs

### Free Tier Limits:

**Vercel:**
- 100 GB bandwidth/month
- 100 GB-hours compute/month
- Unlimited deployments
- 1 team member

**Vercel Postgres:**
- 256 MB storage
- 60 hours compute/month
- Enough for ~1000 agreements

**Cloudinary:**
- 25 GB storage
- 25 GB bandwidth/month
- 25,000 transformations/month

**Total: $0/month** for typical usage! 🎉

---

## 🚀 Next Steps

1. **Add Custom Domain** (optional)
2. **Invite Team Members** (Vercel Pro: $20/month)
3. **Setup Monitoring** (Sentry, LogRocket)
4. **Add Analytics** (Google Analytics, Plausible)
5. **Backup Database** (pg_dump via Vercel CLI)

---

## 📞 Support

**Issues?**
- Check logs in Vercel dashboard
- Read error messages carefully
- Check environment variables
- Redeploy if needed

**Need Help?**
- Vercel Docs: https://vercel.com/docs
- Cloudinary Docs: https://cloudinary.com/documentation
- GitHub Issues: https://github.com/gilangpramana21/financing-obligation-tracker/issues

---

**🎉 Congratulations! Your app is now live on Vercel!**
