# ⏱️ Rate Limit Guide - Avoid 429 Errors

## 🚨 What Happened?

You got this error:
```
429 RESOURCE_EXHAUSTED. You exceeded your current quota.
```

**Cause**: You uploaded 5 files at once, which exceeded the free tier rate limit.

## 📊 Free Tier Limits

### Gemini API Free Tier:
- **15 requests per minute** (RPM)
- **1,500 requests per day** (RPD)
- **1M tokens per minute** (TPM)

### What This Means:
- ✅ Can process ~15 PDFs per minute
- ❌ Cannot process 5 PDFs instantly (each needs ~5-10 seconds)
- ⏰ Need delays between files

## ✅ Solution Implemented

The system now automatically:

### 1. **Adds Delays Between Files**
```
File 1: Process immediately
  ↓
Wait 5 seconds
  ↓
File 2: Process
  ↓
Wait 5 seconds
  ↓
File 3: Process
...
```

### 2. **Shows Warnings for Large Batches**
When you upload > 3 files:
```
⚠️ Large batch detected! Processing 5 files will take time.
💡 Recommendation: Upload 1-3 files at a time.
Estimated time: ~75 seconds
```

### 3. **Handles Rate Limit Errors**
If rate limit is hit:
```
❌ Rate limit exceeded
⏳ Waiting 60 seconds for rate limit to reset...
✅ Cooldown complete. Continuing...
```

### 4. **Extracts Retry Delay from Error**
API tells us when to retry:
```
"Please retry in 32.095511097s"
  ↓
System waits 37 seconds (32 + 5 buffer)
  ↓
Continues processing
```

## 🎯 Best Practices

### ✅ Recommended: Upload 1-3 Files at a Time

**Why?**
- Faster processing (no delays needed)
- Lower chance of hitting rate limits
- Better user experience

**Example**:
```
Batch 1: Upload 3 PDFs → Process (30 seconds)
Wait for completion
Batch 2: Upload 3 PDFs → Process (30 seconds)
Wait for completion
Batch 3: Upload 3 PDFs → Process (30 seconds)

Total: 9 PDFs in ~90 seconds
```

### ❌ Avoid: Uploading 5+ Files at Once

**Why?**
- Triggers rate limits
- Requires long delays (5s between each)
- Slower overall processing

**Example**:
```
Upload 5 PDFs at once
  ↓
File 1: Process (10s)
Wait 5s
File 2: Process (10s)
Wait 5s
File 3: Process (10s)
Wait 5s
File 4: Process (10s)
Wait 5s
File 5: Process (10s)

Total: 5 PDFs in ~70 seconds
```

## ⏱️ Processing Time Estimates

| Files | With Delays | Without Delays | Recommended |
|-------|-------------|----------------|-------------|
| 1 file | ~10s | ~10s | ✅ Optimal |
| 2 files | ~25s | ~20s | ✅ Good |
| 3 files | ~40s | ~30s | ✅ Good |
| 4 files | ~55s | ~40s | ⚠️ Slow |
| 5 files | ~70s | ~50s | ❌ Too slow |
| 10 files | ~145s | ~100s | ❌ Very slow |

**Note**: "With Delays" includes 5s wait between files to avoid rate limits.

## 🔧 How the System Works Now

### Scenario 1: Small Batch (1-3 files)
```
1. Upload 3 PDFs
2. System processes with minimal delays
3. ✅ Complete in ~40 seconds
4. No rate limit issues
```

### Scenario 2: Large Batch (4+ files)
```
1. Upload 5 PDFs
2. System shows warning:
   "⚠️ Large batch! Will take ~75 seconds"
3. Processes with 5s delays between files
4. If rate limit hit:
   - Waits 60 seconds
   - Continues processing
5. ✅ Complete in ~75-135 seconds
```

### Scenario 3: Rate Limit Hit
```
1. Processing file 3 of 5
2. ❌ Rate limit error
3. System detects 429 error
4. Extracts retry delay (e.g., 32s)
5. Waits 37 seconds (32 + 5 buffer)
6. ✅ Continues with file 4
```

## 💡 Pro Tips

### For Fastest Processing:
1. **Upload 1-2 files at a time**
2. **Wait for completion**
3. **Upload next batch**

### For Bulk Processing:
1. **Upload 3 files at a time** (sweet spot)
2. **Let system handle delays**
3. **Be patient** (system is working!)

### If You Hit Rate Limits:
1. **Don't panic** - System handles it automatically
2. **Wait for cooldown** - Usually 30-60 seconds
3. **Continue normally** - System resumes automatically

### To Avoid Rate Limits:
1. **Smaller batches** - 1-3 files recommended
2. **Off-peak hours** - Late night/early morning
3. **Spread out uploads** - Don't rush
4. **Monitor progress** - Watch status messages

## 📈 Rate Limit Recovery

### Free Tier Resets:
- **Per-minute limits**: Reset every 60 seconds
- **Per-day limits**: Reset at midnight UTC
- **Token limits**: Reset every 60 seconds

### If You Exhaust Daily Quota:
1. **Wait until midnight UTC** - Quota resets
2. **Get another API key** - Create new project
3. **Upgrade to paid tier** - Higher limits

## 🆙 Upgrade Options

### If Free Tier Isn't Enough:

**Option 1: Multiple API Keys**
- Create multiple Google Cloud projects
- Get separate API key for each
- Rotate between keys
- **Cost**: FREE

**Option 2: Paid Tier (Gemini)**
- Higher rate limits
- More reliable
- **Cost**: Pay-as-you-go

**Option 3: Claude/Anthropic**
- No rate limits (paid tier)
- Better availability
- **Cost**: ~$3 per 1M tokens

## 🎯 Current System Behavior

### What You'll See:

**Normal Processing (1-3 files)**:
```
Processing file1.pdf (1/3)...
✅ Successfully processed: file1.pdf
Processing file2.pdf (2/3)...
✅ Successfully processed: file2.pdf
Processing file3.pdf (3/3)...
✅ Successfully processed: file3.pdf
```

**Large Batch (4+ files)**:
```
⚠️ Processing 5 files. This will take ~75 seconds.
💡 Tip: Upload 1-3 files at a time for faster processing.

Processing file1.pdf (1/5)...
✅ Successfully processed: file1.pdf
⏳ Waiting 5s to avoid rate limits...
Processing file2.pdf (2/5)...
✅ Successfully processed: file2.pdf
⏳ Waiting 5s to avoid rate limits...
...
```

**Rate Limit Hit**:
```
Processing file3.pdf (3/5)...
❌ Rate limit exceeded for file3.pdf
⚠️ API rate limit hit. Waiting before continuing...
⏳ Waiting 37 seconds for rate limit to reset...
✅ Cooldown complete. Continuing with remaining files...
Processing file4.pdf (4/5)...
```

## 📞 Summary

### ✅ Do This:
- Upload 1-3 files at a time
- Wait for completion before uploading more
- Let system handle delays automatically
- Be patient with large batches

### ❌ Don't Do This:
- Upload 5+ files at once
- Refresh page during processing
- Ignore rate limit warnings
- Rush the process

### 🎯 Optimal Workflow:
```
1. Upload 2-3 PDFs
2. Click "Process"
3. Wait ~30 seconds
4. Check results
5. Upload next batch
6. Repeat
```

**Result**: Fast, reliable processing without rate limit issues! 🎉

---

**Dashboard**: http://localhost:8501
**Status**: ✅ Rate limit handling active
**Recommendation**: Upload 1-3 files at a time for best experience
