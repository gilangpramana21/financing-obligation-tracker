# Setup Gemini API (GRATIS) 🆓

Panduan lengkap setup Gemini sebagai LLM untuk ekstraksi dokumen.

---

## Kenapa Gemini?

✅ **GRATIS** - Tidak perlu kartu kredit
✅ **Generous quota** - 1,500 requests/day
✅ **Cepat** - Response time sangat cepat
✅ **Akurat** - Kualitas ekstraksi excellent
✅ **Mudah** - Setup 5 menit

---

## Langkah Setup

### 1. Dapatkan API Key (2 menit)

1. **Buka Google AI Studio:**
   https://makersuite.google.com/app/apikey

2. **Login dengan Google Account**
   - Gunakan akun Google pribadi atau workspace
   - Tidak perlu kartu kredit

3. **Create API Key:**
   - Klik tombol "Create API Key"
   - Pilih project (atau buat baru)
   - Copy API key yang muncul

4. **Simpan API Key:**
   ```
   AIzaSyC...your_key_here
   ```

### 2. Konfigurasi Project (1 menit)

```bash
# Copy template
cp .env.example .env

# Edit .env file
nano .env
# atau
code .env
```

**Tambahkan API key:**
```bash
GEMINI_API_KEY=AIzaSyC...your_key_here
```

### 3. Install Dependencies (2 menit)

```bash
pip install -r requirements.txt
```

Ini akan install:
- `google-generativeai` - Gemini SDK
- Dan dependencies lainnya

### 4. Validasi Setup

```bash
python validate_setup.py
```

**Output yang diharapkan:**
```
Checking dependencies...
  ✓ Gemini SDK (FREE) (google.generativeai)
  ✓ PDF extraction (pdfplumber)
  ✓ PDF extraction (fallback) (pymupdf)
  ✓ Word document extraction (docx)
  ✓ Database ORM (sqlalchemy)
  ✓ Environment variables (dotenv)
✅ All required dependencies installed

Checking optional dependencies...
  ℹ️  Anthropic SDK (PAID - optional) (anthropic) - not installed (optional)

Checking environment configuration...
  ✓ GEMINI_API_KEY configured (AIzaSyC...)
  ℹ️  ANTHROPIC_API_KEY not configured (optional)
✅ Environment configured

...

Result: 5/5 checks passed

🎉 All checks passed! System is ready to use.
```

---

## Test Ekstraksi

### Test dengan Sample Text (Tanpa PDF)

```bash
python test_extractor.py
```

**Output:**
```
======================================================================
TESTING DOCUMENT EXTRACTOR
======================================================================

Initializing DocumentExtractor with GEMINI...
🆓 Using Gemini 1.5 Flash (Free)
✓ Extractor initialized

Extracting obligations from sample agreement text...
Sample text length: 2847 characters

======================================================================
EXTRACTION RESULTS
======================================================================

{
  "financier": "PT Bank Central Asia Tbk",
  "agreement_name": "Term Loan Facility Agreement",
  "contract_start": "2024-01-15",
  "contract_end": "2029-01-15",
  "facility_amount": 75000000000,
  "currency": "IDR",
  ...
}

✓ Data validation: PASSED

======================================================================
SUMMARY
======================================================================
Financier: PT Bank Central Asia Tbk
Agreement: Term Loan Facility Agreement
Facility: IDR 75,000,000,000
Contract Period: 2024-01-15 to 2029-01-15

📊 Reporting Obligations: 3
   - Quarterly Financial Statements (quarterly)
   - Annual Audited Financial Statements (annual)
   - Compliance Certificate (semi-annual)

📈 Covenants: 4
   - Minimum Current Ratio (minimum: 1.2 ratio)
   - Maximum Debt Service Coverage Ratio (minimum: 1.5 ratio)
   - Maximum Total Debt to EBITDA (maximum: 3.5 ratio)
   - Minimum Tangible Net Worth (minimum: 20000000000.0 IDR)

📋 Other Obligations: 5
   - [Notification] The Borrower shall notify the Lender within 10 busines...
   - [Notification] The Borrower shall notify the Lender within 5 business...
   - [Restriction] The Borrower shall not declare or pay any dividends if ...
   - [Approval Required] The Borrower shall obtain prior written approval from th...
   - [Action Required] The Borrower shall maintain adequate insurance coverage on...

Save to database? (y/n):
```

### Test dengan PDF Asli

```bash
# Tambahkan PDF
cp /path/to/loan_agreement.pdf documents/

# Process
python extractor.py
```

---

## Quota & Limits

### Free Tier (Cukup untuk kebanyakan kasus)

- **15 requests per minute**
- **1,500 requests per day**
- **1 million tokens per minute**
- **1.5 million tokens per day**

### Estimasi Penggunaan

**1 dokumen financing agreement (50-100 halaman):**
- Input: ~50,000-100,000 tokens
- Output: ~2,000-5,000 tokens
- **Total: ~1 request**

**Dengan free tier:**
- Bisa process **1,500 dokumen per hari**
- Atau **~45,000 dokumen per bulan**
- **GRATIS**

---

## Monitoring Quota

### Cek Usage

1. Buka Google AI Studio: https://makersuite.google.com/
2. Lihat dashboard usage
3. Monitor requests per day

### Jika Quota Habis

**Opsi 1: Tunggu Reset**
- Quota reset setiap hari (midnight UTC)

**Opsi 2: Upgrade ke Paid**
- Bisa upgrade jika butuh lebih
- Tetap murah dibanding alternatif

**Opsi 3: Gunakan Anthropic**
```bash
# Setup Anthropic key di .env
ANTHROPIC_API_KEY=sk-ant-...

# Gunakan Anthropic
python extractor.py --anthropic
```

---

## Troubleshooting

### Error: "GEMINI_API_KEY not found"

**Solusi:**
```bash
# 1. Cek .env file ada
ls -la .env

# 2. Cek isi .env
cat .env | grep GEMINI

# 3. Pastikan format benar
GEMINI_API_KEY=AIzaSyC...your_key_here
# (tidak ada spasi, tidak ada quotes)

# 4. Restart terminal
```

### Error: "google-generativeai not installed"

**Solusi:**
```bash
pip install google-generativeai
```

### Error: "API key not valid"

**Solusi:**
1. Cek API key di Google AI Studio
2. Generate API key baru jika perlu
3. Copy paste dengan hati-hati (no extra spaces)

### Error: "Quota exceeded"

**Solusi:**
```bash
# Cek quota di: https://makersuite.google.com/
# Tunggu reset atau gunakan Anthropic:
python extractor.py --anthropic
```

---

## Perbandingan dengan Anthropic

| Aspek | Gemini 1.5 Flash | Claude Sonnet 4 |
|-------|------------------|-----------------|
| **Biaya** | GRATIS | $0.20-0.50/doc |
| **Setup** | 5 menit | 10 menit + CC |
| **Quota** | 1,500/day | Unlimited |
| **Kecepatan** | Sangat cepat | Cepat |
| **Akurasi** | Excellent | Excellent |
| **Rekomendasi** | ✅ Default | Produksi besar |

---

## Best Practices

### 1. Batch Processing
```bash
# Process multiple docs sekaligus
cp *.pdf documents/
python extractor.py
```

### 2. Monitor Quota
- Cek usage secara berkala
- Jangan process ribuan docs sekaligus

### 3. Error Handling
- Sistem otomatis retry jika gagal
- Cek error log untuk debugging

### 4. Backup Plan
- Setup Anthropic key sebagai backup
- Gunakan jika Gemini quota habis

---

## FAQ

**Q: Apakah benar-benar gratis?**
A: Ya, 100% gratis untuk 1,500 requests/day. Tidak perlu kartu kredit.

**Q: Apakah akurat?**
A: Ya, Gemini 1.5 Flash sangat akurat untuk ekstraksi dokumen.

**Q: Bagaimana jika quota habis?**
A: Tunggu reset (daily) atau gunakan Anthropic sebagai backup.

**Q: Apakah data saya aman?**
A: Ya, Google tidak menggunakan data Anda untuk training model.

**Q: Bisa untuk production?**
A: Ya, sangat cocok untuk production dengan volume normal (<1,500 docs/day).

**Q: Bagaimana upgrade ke paid?**
A: Bisa upgrade di Google AI Studio jika butuh quota lebih.

---

## Links

- **Get API Key:** https://makersuite.google.com/app/apikey
- **Documentation:** https://ai.google.dev/docs
- **Pricing:** https://ai.google.dev/pricing
- **Support:** https://ai.google.dev/support

---

## Quick Commands

```bash
# Setup
cp .env.example .env
# Edit .env, add GEMINI_API_KEY

# Install
pip install -r requirements.txt

# Validate
python validate_setup.py

# Test
python test_extractor.py

# Process
python extractor.py
```

---

## ✅ Checklist

- [ ] Dapatkan Gemini API key
- [ ] Copy .env.example ke .env
- [ ] Tambahkan GEMINI_API_KEY ke .env
- [ ] Install dependencies
- [ ] Run validate_setup.py
- [ ] Test dengan test_extractor.py
- [ ] Process dokumen pertama

**Selesai!** Anda siap menggunakan sistem dengan LLM gratis.
