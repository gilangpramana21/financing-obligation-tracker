# 🤖 AI Model Information

## Current Configuration

### Primary Model
**Model**: `gemini-2.5-flash`
- **Provider**: Google Gemini
- **Cost**: FREE (with rate limits)
- **Speed**: Very fast (~2-5 seconds per PDF)
- **Quality**: Excellent for structured data extraction
- **Availability**: High (latest stable release)

### Fallback Model
**Model**: `gemini-2.0-flash`
- **Provider**: Google Gemini
- **Cost**: FREE
- **Speed**: Fast (~3-6 seconds per PDF)
- **Quality**: Excellent
- **Purpose**: Backup if primary model is overloaded

## How It Works

```
Upload PDF
    ↓
Try gemini-2.5-flash (3 attempts with retry)
    ↓ (if fails)
Try gemini-2.0-flash (3 attempts with retry)
    ↓
Success or Error
```

## Available Models

Based on your API key, these models are available:

### Recommended for This Project:
- ✅ **gemini-2.5-flash** (Current primary)
- ✅ **gemini-2.0-flash** (Current fallback)
- ✅ **gemini-2.5-pro** (More powerful, slower)
- ✅ **gemini-3.5-flash** (Experimental, may be unstable)

### Other Available Models:
- `gemini-flash-latest` - Always points to latest flash model
- `gemini-pro-latest` - Always points to latest pro model
- `gemini-3-flash-preview` - Preview of Gemini 3
- `gemini-3-pro-preview` - Preview of Gemini 3 Pro

## Model Comparison

| Model | Speed | Quality | Cost | Stability | Best For |
|-------|-------|---------|------|-----------|----------|
| **gemini-2.5-flash** | ⚡⚡⚡ | ⭐⭐⭐⭐ | FREE | 🟢 High | Production use |
| **gemini-2.0-flash** | ⚡⚡⚡ | ⭐⭐⭐⭐ | FREE | 🟢 High | Fallback |
| **gemini-2.5-pro** | ⚡⚡ | ⭐⭐⭐⭐⭐ | FREE | 🟢 High | Complex documents |
| **gemini-3.5-flash** | ⚡⚡⚡ | ⭐⭐⭐⭐ | FREE | 🟡 Medium | Testing |

## Rate Limits (Free Tier)

### Gemini Free Tier:
- **Requests per minute**: 15 RPM
- **Requests per day**: 1,500 RPD
- **Tokens per minute**: 1M TPM

### What This Means:
- ✅ Can process ~15 PDFs per minute
- ✅ Can process ~1,500 PDFs per day
- ✅ More than enough for most use cases

### If You Hit Limits:
1. Wait 1 minute (RPM resets)
2. Upload fewer files at once
3. Process during off-peak hours
4. Consider paid tier for higher limits

## Switching Models

### To Use a Different Primary Model:

Edit `extractor.py` line ~50:

```python
# Change this:
self.model_name = "gemini-2.5-flash"

# To one of these:
self.model_name = "gemini-2.5-pro"      # More powerful
self.model_name = "gemini-3.5-flash"    # Experimental
self.model_name = "gemini-flash-latest" # Always latest
```

### To Change Fallback Model:

```python
# Change this:
self.fallback_model = "gemini-2.0-flash"

# To:
self.fallback_model = "gemini-2.5-pro"  # More powerful fallback
```

## Alternative: Use Claude (Paid)

If you need guaranteed availability:

### 1. Get Claude API Key
- Sign up: https://console.anthropic.com/
- Get API key from dashboard

### 2. Update .env
```bash
ANTHROPIC_API_KEY=your_claude_key_here
```

### 3. Update dashboard.py
```python
# Line ~427 in dashboard.py
extractor = DocumentExtractor(llm_provider="anthropic")
```

### Claude Models:
- **claude-sonnet-4** - Fast, high quality
- **claude-opus-4** - Most powerful
- **Cost**: ~$3 per 1M input tokens

## Performance Tips

### For Faster Processing:
1. Use `gemini-2.5-flash` (current default)
2. Upload smaller PDFs (< 5MB)
3. Process during off-peak hours

### For Better Quality:
1. Use `gemini-2.5-pro` (slower but more accurate)
2. Ensure PDFs are text-based (not scanned images)
3. Use well-structured documents

### For Reliability:
1. Keep retry logic enabled (default)
2. Use fallback model (default)
3. Monitor rate limits

## Troubleshooting

### Error: "Model not found"
**Solution**: Model name is incorrect. Use one from the available list above.

### Error: "Rate limit exceeded"
**Solution**: Wait 1 minute or reduce upload frequency.

### Error: "API key invalid"
**Solution**: Check GEMINI_API_KEY in .env file.

### Slow Processing
**Possible causes**:
- Large PDF files (> 10MB)
- Complex document structure
- API congestion during peak hours

**Solutions**:
- Compress PDFs before upload
- Process during off-peak hours
- Use faster model (gemini-2.5-flash)

## Current Status

✅ **Primary Model**: gemini-2.5-flash (Working)
✅ **Fallback Model**: gemini-2.0-flash (Ready)
✅ **Retry Logic**: Enabled (3 attempts)
✅ **Rate Limits**: Within free tier
✅ **Dashboard**: http://localhost:8501

## Model Update History

- **2026-05-22**: Updated to gemini-2.5-flash (latest stable)
- **Previous**: gemini-2.0-flash-exp (not available in API v1beta)
- **Previous**: gemini-1.5-flash (deprecated)

---

**Recommendation**: Keep current configuration (gemini-2.5-flash + gemini-2.0-flash). 
It provides the best balance of speed, quality, and reliability! 🎯
