# 🚀 Vercel Deployment Guide

## ⚠️ Important Limitations

**Vercel is a serverless platform with limitations:**

1. **No Background Scheduler** - APScheduler won't work on Vercel
   - Daily email alerts won't run automatically
   - You need to use Vercel Cron Jobs or external services

2. **No Persistent Storage** - SQLite database will reset on each deployment
   - Use external database (PostgreSQL, MySQL, etc.)
   - Or use Vercel Postgres addon

3. **File Upload Limitations** - Uploaded files stored in `/tmp` (temporary)
   - Files deleted after function execution
   - Consider using cloud storage (S3, Cloudinary, etc.)

## 📋 Prerequisites

1. GitHub account with repository
2. Vercel account (free tier available)
3. Gemini API key

## 🚀 Quick Deploy

### Option 1: Deploy via Vercel Dashboard (Easiest)

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/new
   - Login with GitHub

2. **Import Repository**
   - Click "Import Project"
   - Select: `gilangpramana21/financing-obligation-tracker`
   - Click "Import"

3. **Configure Environment Variables**
   Add these in Vercel dashboard:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   SECRET_KEY=your_random_secret_key_here
   VERCEL=true
   
   # Optional: Email notifications
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_app_password
   RECIPIENT_EMAILS=recipient@example.com
   ```

4. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your app will be live at: `https://your-project.vercel.app`

### Option 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from project directory
cd "/Users/ss/Documents/Automated financing agreement obligation tracker"
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? financing-obligation-tracker
# - Directory? ./
# - Override settings? No

# Set environment variables
vercel env add GEMINI_API_KEY
vercel env add SECRET_KEY
vercel env add VERCEL

# Deploy to production
vercel --prod
```

## 🗄️ Database Setup (Required for Production)

Since SQLite doesn't work on Vercel, you need an external database:

### Option A: Vercel Postgres (Recommended)

1. Go to your project in Vercel Dashboard
2. Click "Storage" tab
3. Click "Create Database" → "Postgres"
4. Follow setup instructions
5. Vercel will automatically add `POSTGRES_URL` to environment variables

Then update `models.py`:
```python
import os
from sqlalchemy import create_engine

def get_engine(db_path=None):
    """Create and return database engine."""
    # Use Postgres on Vercel, SQLite locally
    if os.getenv('VERCEL'):
        database_url = os.getenv('POSTGRES_URL')
        return create_engine(database_url, echo=False)
    else:
        return create_engine(f'sqlite:///{db_path or "obligation_tracker.db"}', echo=False)
```

### Option B: External PostgreSQL

Use services like:
- **Supabase** (free tier): https://supabase.com
- **Railway** (free tier): https://railway.app
- **ElephantSQL** (free tier): https://www.elephantsql.com

Add connection string to Vercel environment variables:
```
DATABASE_URL=postgresql://user:password@host:5432/database
```

## 📧 Email Notifications Setup

Since background scheduler doesn't work, use Vercel Cron Jobs:

1. **Create `vercel.json` with cron** (already included):
```json
{
  "crons": [{
    "path": "/api/cron/daily-check",
    "schedule": "0 9 * * *"
  }]
}
```

2. **Create cron endpoint** in `app.py`:
```python
@app.route('/api/cron/daily-check')
def cron_daily_check():
    """Cron endpoint for daily obligation check."""
    # Verify request is from Vercel Cron
    auth_header = request.headers.get('Authorization')
    if auth_header != f"Bearer {os.getenv('CRON_SECRET')}":
        return jsonify({'error': 'Unauthorized'}), 401
    
    run_daily_check()
    return jsonify({'success': True, 'message': 'Daily check completed'})
```

3. **Add CRON_SECRET** to Vercel environment variables

## 📁 File Upload Setup

For production file uploads, use cloud storage:

### Option A: Cloudinary (Recommended for PDFs)

1. Sign up: https://cloudinary.com (free tier)
2. Get API credentials
3. Install: `pip install cloudinary`
4. Update upload route to use Cloudinary

### Option B: AWS S3

1. Create S3 bucket
2. Get AWS credentials
3. Install: `pip install boto3`
4. Update upload route to use S3

## 🔧 Configuration Files

### `vercel.json` (Already Created)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

### `.vercelignore` (Already Created)
Excludes unnecessary files from deployment.

## 🧪 Testing Deployment

After deployment:

1. **Test Homepage**
   - Visit: `https://your-project.vercel.app`
   - Should show dashboard

2. **Test Upload** (Will fail without database setup)
   - Upload a PDF
   - Check if extraction works

3. **Test Email** (Optional)
   - Go to Settings
   - Click "Send Test Alert"

## 🐛 Troubleshooting

### Error: "Module not found"
- Check `requirements.txt` includes all dependencies
- Redeploy: `vercel --prod`

### Error: "Database locked" or "No such table"
- SQLite doesn't work on Vercel
- Setup external database (see Database Setup section)

### Error: "File not found" after upload
- Files in `/tmp` are temporary
- Setup cloud storage (see File Upload Setup section)

### Scheduler not working
- Background tasks don't work on serverless
- Use Vercel Cron Jobs (see Email Notifications Setup)

## 📊 Vercel Limits (Free Tier)

- **Bandwidth**: 100 GB/month
- **Function Duration**: 10 seconds max
- **Function Size**: 50 MB max
- **Deployments**: Unlimited
- **Team Members**: 1

For production with large PDFs, consider upgrading to Pro plan.

## 🔄 Alternative: Deploy to Traditional Server

If Vercel limitations are too restrictive, consider:

1. **Railway** - Supports background tasks, persistent storage
2. **Render** - Free tier with persistent disk
3. **DigitalOcean App Platform** - $5/month
4. **AWS EC2** - Full control
5. **Heroku** - Easy deployment (paid)

## 📚 Resources

- Vercel Docs: https://vercel.com/docs
- Vercel Python: https://vercel.com/docs/functions/serverless-functions/runtimes/python
- Vercel Cron Jobs: https://vercel.com/docs/cron-jobs
- Vercel Postgres: https://vercel.com/docs/storage/vercel-postgres

---

**Note**: For full functionality (background scheduler, persistent database, file uploads), consider deploying to a traditional server instead of Vercel.
