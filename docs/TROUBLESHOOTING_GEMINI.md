# Troubleshooting Gemini API

## Masalah: Model Not Found (404)

Jika Anda mendapat error:
```
404 NOT_FOUND. models/gemini-1.5-flash is not found
```

### Kemungkinan Penyebab:

1. **API Key belum aktif**
   - API key baru butuh waktu beberapa menit untuk aktif
   - Tunggu 5-10 menit setelah membuat API key

2. **Region tidak didukung**
   - Gemini API mungkin belum tersedia di region Anda
   - Cek di: https://ai.google.dev/gemini-api/docs/available-regions

3. **Quota belum diaktifkan**
   - Pastikan Anda sudah enable Gemini API di project
   - Kunjungi: https://makersuite.google.com/

### Solusi:

#### Opsi 1: Tunggu dan Coba Lagi
```bash
# Tunggu 10 menit, lalu test lagi
source venv/bin/activate
python test_extractor.py
```

#### Opsi 2: Gunakan Anthropic Claude (Berbayar)

Jika Gemini tidak bisa digunakan, Anda bisa pakai Anthropic Claude:

1. **Dapatkan Anthropic API Key:**
   - Kunjungi: https://console.anthropic.com/
   - Sign up (perlu kartu kredit)
   - Buat API key

2. **Tambahkan ke .env:**
   ```bash
   # Edit .env file
   ANTHROPIC_API_KEY=sk-ant-api03-your_key_here
   ```

3. **Test dengan Anthropic:**
   ```bash
   source venv/bin/activate
   python test_extractor.py --anthropic
   ```

4. **Gunakan Anthropic sebagai default:**
   ```bash
   # Process documents dengan Anthropic
   python extractor.py --anthropic
   ```

#### Opsi 3: Cek API Key

```bash
# Pastikan API key benar
cat .env | grep GEMINI

# Format harus:
GEMINI_API_KEY=AIzaSy...
# (tidak ada spasi, tidak ada quotes)
```

#### Opsi 4: Generate API Key Baru

1. Kunjungi: https://makersuite.google.com/app/apikey
2. Delete API key lama
3. Create API key baru
4. Update di .env file
5. Tunggu 10 menit
6. Test lagi

---

## Biaya

### Gemini (Jika Berhasil)
- **GRATIS** - 1,500 requests/day
- Tidak perlu kartu kredit

### Anthropic Claude (Alternatif)
- **$0.20-0.50 per dokumen** (50-100 halaman)
- Perlu kartu kredit
- Unlimited requests

---

## Rekomendasi

**Untuk sekarang:**
1. Coba tunggu 10 menit dan test Gemini lagi
2. Jika masih error, gunakan Anthropic sebagai alternatif
3. Anthropic lebih reliable dan akurat (tapi berbayar)

**Untuk production:**
- Jika budget ada: Gunakan Anthropic (lebih reliable)
- Jika budget terbatas: Coba Gemini lagi nanti atau gunakan Anthropic untuk volume kecil

---

## Status Saat Ini

✅ Setup sudah benar
✅ Dependencies terinstall
✅ API key terkonfigurasi
⚠️  Gemini API belum bisa digunakan (404 error)
✅ Anthropic tersedia sebagai alternatif

---

## Next Steps

```bash
# Opsi 1: Tunggu dan coba Gemini lagi
sleep 600  # tunggu 10 menit
source venv/bin/activate
python test_extractor.py

# Opsi 2: Gunakan Anthropic sekarang
# 1. Dapatkan API key dari https://console.anthropic.com/
# 2. Tambahkan ke .env:
#    ANTHROPIC_API_KEY=sk-ant-api03-...
# 3. Test:
source venv/bin/activate
python test_extractor.py --anthropic
```

---

## Support

Jika masih ada masalah:
1. Cek region support: https://ai.google.dev/gemini-api/docs/available-regions
2. Cek API key valid: https://makersuite.google.com/app/apikey
3. Gunakan Anthropic sebagai alternatif
