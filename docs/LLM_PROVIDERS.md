# LLM Provider Options

Sistem ini mendukung dua provider LLM untuk ekstraksi dokumen:

---

## 🆓 Gemini 1.5 Flash (Default - GRATIS)

**Rekomendasi:** Gunakan ini untuk penggunaan normal

### Keunggulan
- ✅ **GRATIS** - Free tier sangat generous
- ✅ **Cepat** - Response time cepat
- ✅ **Quota tinggi** - 15 requests/minute, 1500 requests/day
- ✅ **Akurat** - Kualitas ekstraksi sangat baik
- ✅ **Mudah** - Setup mudah, tidak perlu kartu kredit

### Quota & Limits
- **Free tier:**
  - 15 RPM (requests per minute)
  - 1,500 requests per day
  - 1 million tokens per minute
  - 1.5 million tokens per day

### Setup

1. **Dapatkan API Key:**
   - Kunjungi: https://makersuite.google.com/app/apikey
   - Login dengan Google account
   - Klik "Create API Key"
   - Copy API key

2. **Konfigurasi:**
   ```bash
   # Edit .env file
   GEMINI_API_KEY=AIzaSy...your_key_here
   ```

3. **Gunakan:**
   ```bash
   # Default (otomatis pakai Gemini)
   python extractor.py
   
   # Atau eksplisit
   python extractor.py --gemini
   ```

### Biaya
**GRATIS** untuk penggunaan normal (1,500 docs/day)

---

## 💰 Claude Sonnet 4 (Opsional - BERBAYAR)

**Gunakan jika:** Butuh akurasi maksimal atau quota Gemini habis

### Keunggulan
- ✅ **Akurasi tinggi** - Salah satu LLM terbaik
- ✅ **Context window besar** - Bisa handle dokumen sangat panjang
- ✅ **Reliable** - Konsisten dan stabil

### Biaya
- Input: $3 per million tokens
- Output: $15 per million tokens
- **~$0.20-0.50 per dokumen** (50-100 halaman)

### Setup

1. **Dapatkan API Key:**
   - Kunjungi: https://console.anthropic.com/
   - Sign up (perlu kartu kredit)
   - Buat API key

2. **Konfigurasi:**
   ```bash
   # Edit .env file
   ANTHROPIC_API_KEY=sk-ant-api03-...your_key_here
   ```

3. **Gunakan:**
   ```bash
   # Eksplisit gunakan Anthropic
   python extractor.py --anthropic
   
   # Atau
   python extractor.py --claude
   ```

---

## 📊 Perbandingan

| Fitur | Gemini 1.5 Flash | Claude Sonnet 4 |
|-------|------------------|-----------------|
| **Biaya** | GRATIS | $0.20-0.50/doc |
| **Kecepatan** | Sangat cepat | Cepat |
| **Akurasi** | Sangat baik | Excellent |
| **Quota** | 1,500 req/day | Unlimited (bayar) |
| **Setup** | Mudah | Perlu kartu kredit |
| **Rekomendasi** | ✅ Default | Untuk produksi besar |

---

## 🔧 Cara Penggunaan

### Default (Gemini - Gratis)
```bash
# Otomatis pakai Gemini
python extractor.py

# Test
python test_extractor.py
```

### Pilih Provider Spesifik

```bash
# Gunakan Gemini
python extractor.py --gemini
python extractor.py documents/agreement.pdf --gemini

# Gunakan Anthropic
python extractor.py --anthropic
python extractor.py documents/agreement.pdf --claude
```

### Programmatic Usage

```python
from extractor import DocumentExtractor

# Gunakan Gemini (gratis)
extractor = DocumentExtractor(llm_provider="gemini")
agreement_id = extractor.process_document('documents/agreement.pdf')

# Gunakan Anthropic (berbayar)
extractor = DocumentExtractor(llm_provider="anthropic")
agreement_id = extractor.process_document('documents/agreement.pdf')
```

---

## ⚙️ Konfigurasi .env

```bash
# Gemini (FREE - recommended)
GEMINI_API_KEY=AIzaSy...your_key_here

# Anthropic (PAID - optional)
ANTHROPIC_API_KEY=sk-ant-api03-...your_key_here
```

**Minimal:** Hanya perlu salah satu API key
**Rekomendasi:** Setup Gemini dulu (gratis)

---

## 🎯 Rekomendasi Penggunaan

### Untuk Development & Testing
✅ **Gunakan Gemini**
- Gratis
- Quota cukup untuk testing
- Akurasi bagus

### Untuk Production (Volume Kecil-Sedang)
✅ **Gunakan Gemini**
- Gratis sampai 1,500 docs/day
- Cukup untuk kebanyakan use case
- Bisa upgrade ke paid jika perlu

### Untuk Production (Volume Besar)
💰 **Pertimbangkan Anthropic**
- Jika butuh > 1,500 docs/day
- Jika butuh akurasi maksimal
- Jika budget tersedia

---

## 🔍 Validasi Setup

```bash
python validate_setup.py
```

Output akan menunjukkan provider mana yang tersedia:
```
Checking environment configuration...
  ✓ GEMINI_API_KEY configured (AIzaSy...)
  ℹ️  ANTHROPIC_API_KEY not configured (optional)
✅ Environment configured
```

---

## 🚨 Troubleshooting

### "GEMINI_API_KEY not found"
```bash
# 1. Pastikan .env file ada
ls -la .env

# 2. Pastikan key sudah diisi
cat .env | grep GEMINI

# 3. Dapatkan key dari:
# https://makersuite.google.com/app/apikey
```

### "google-generativeai not installed"
```bash
pip install google-generativeai
```

### Quota Gemini Habis
```bash
# Opsi 1: Tunggu reset (daily limit)
# Opsi 2: Gunakan Anthropic
python extractor.py --anthropic
```

---

## 💡 Tips

1. **Mulai dengan Gemini** - Gratis dan cukup untuk kebanyakan kasus
2. **Monitor quota** - Cek usage di Google AI Studio
3. **Backup plan** - Setup Anthropic key jika butuh fallback
4. **Batch processing** - Process multiple docs sekaligus untuk efisiensi

---

## 📚 Links

- **Gemini API:** https://makersuite.google.com/app/apikey
- **Gemini Docs:** https://ai.google.dev/docs
- **Anthropic Console:** https://console.anthropic.com/
- **Anthropic Docs:** https://docs.anthropic.com/

---

## ✅ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Get Gemini API key (GRATIS)
# https://makersuite.google.com/app/apikey

# 3. Configure
cp .env.example .env
# Edit .env, tambahkan GEMINI_API_KEY

# 4. Test
python test_extractor.py

# 5. Process documents
python extractor.py
```

**Selesai!** Anda siap menggunakan sistem dengan LLM gratis.
