<div align="center">

# 🤖 Belajar AI Autonomous WhatsApp dari Nol sampai Mahir
### Proyek Nyata: Bot WhatsApp Otomatis (Auto-Reply, FAQ, Greeting, Lead Capture, Testing)

Panduan lengkap berbahasa Indonesia + kode siap pakai + diagram + rincian biaya (Rupiah).

</div>

---

## 📦 Isi Repo Ini

| File / Folder | Keterangan |
|---|---|
| **[`TUTORIAL.md`](TUTORIAL.md)** | Tutorial lengkap zero-to-hero (11 level) dalam Bahasa Indonesia |
| **[`docs/Tutorial-WhatsApp-AI-Automation.pdf`](docs/Tutorial-WhatsApp-AI-Automation.pdf)** | Versi PDF tutorial (dengan gambar & rincian biaya) |
| `docs/images/` | Diagram pembantu (roadmap, arsitektur, alur, biaya) |
| `src/` | Kode proyek nyata (Python) — siap dijalankan |
| `data/faq.json` | "Buku pengetahuan" FAQ — ubah tanpa menyentuh kode |
| `tests/` | Uji otomatis (pytest) untuk kelima fitur |
| `scripts/` | Skrip pembuat diagram & PDF |
| `requirements.txt` | Daftar dependensi Python |
| `.env.example` | Contoh konfigurasi (salin jadi `.env`) |

---

## 🎯 5 Proyek Nyata yang Kamu Bangun

| # | Proyek | Level | Fungsi |
|---|---|---|---|
| 1 | **WhatsApp Auto-Reply** | L4 | Balas setiap pesan masuk otomatis, 24 jam |
| 2 | **FAQ Automation Flow** | L5 | Jawab pertanyaan umum (harga, lokasi, jam, dll) |
| 3 | **Auto Greeting** | L6 | Sapaan otomatis: baru / kembali / di luar jam |
| 4 | **Lead Capture** | L7 | Tangkap nama & intent calon pembeli → simpan |
| 5 | **Testing & Optimasi** | L8 | Uji otomatis (pytest) + penyempurnaan |

Semua platform **bisa diakses & legal dari Indonesia** dan punya **paket gratis**:
- **Gemini** (Google AI Studio) — otak AI
- **Fonnte** (gateway lokal Indonesia) atau **Meta WhatsApp Cloud API** (resmi)
- **Flask** + **SQLite** — webhook & penyimpanan

> 💡 Bot ini **tetap jalan tanpa API key** (mode aturan) dan punya mode **`console`**, jadi kamu bisa belajar & menguji **100% gratis** sebelum menyambung ke WhatsApp sungguhan.

---

## 🚀 Cara Cepat Menjalankan

```bash
# 1. Masuk ke folder proyek
cd ai-whatsapp-automation-tutorial

# 2. Buat virtual environment & install dependensi
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Siapkan konfigurasi (untuk belajar, biarkan WHATSAPP_PROVIDER=console)
cp .env.example .env            # Windows: copy .env.example .env

# 4. Coba bot TANPA WhatsApp (gratis, tanpa API key)
python src/simulator.py demo    # skenario otomatis: sapaan -> FAQ -> lead
python src/simulator.py         # mode chat interaktif
python src/simulator.py leads   # lihat lead yang tertangkap

# 5. Jalankan uji otomatis
pytest -q

# 6. (Saat siap) jalankan server webhook untuk WhatsApp sungguhan
python src/app.py               # lalu buka tunnel: ngrok http 5000
```

### Membuat ulang diagram & PDF
```bash
python scripts/generate_diagrams.py   # buat gambar di docs/images/
python scripts/build_pdf.py           # buat docs/Tutorial-WhatsApp-AI-Automation.pdf
```

---

## 🔑 Konfigurasi `.env`

| Variabel | Wajib? | Keterangan |
|---|---|---|
| `WHATSAPP_PROVIDER` | ya | `console` (belajar) / `fonnte` / `meta` |
| `GEMINI_API_KEY` | opsional | Kosongkan untuk mode aturan (gratis). Isi untuk jawaban AI natural. Dapatkan di https://aistudio.google.com/app/apikey |
| `FONNTE_TOKEN` | jika `fonnte` | Token device dari dashboard Fonnte |
| `META_WA_TOKEN`, `META_WA_PHONE_NUMBER_ID`, `META_VERIFY_TOKEN` | jika `meta` | Kredensial WhatsApp Cloud API |
| `BUSINESS_NAME`, `BUSINESS_HOURS`, `TIMEZONE_OFFSET` | ya | Identitas bisnis untuk sapaan & jawaban |

---

## 🧩 Arsitektur Singkat

```
Pelanggan (WhatsApp)
      │
Gateway WA (Fonnte / Meta Cloud API)
      │  webhook
   app.py (Flask)
      │
   bot.py  ── deteksi intent ──►  ai_brain.py  ──►  Gemini (opsional)
      │                                │
      ├── greeting.py (sapaan)         └── knowledge_base.py + data/faq.json
      ├── lead_capture.py (nama&intent)
      └── database.py (SQLite: sesi + lead)
```

Modul utama di `src/`:
- `app.py` — server webhook (terima pesan, kirim balasan)
- `bot.py` — router autonomous (inti pengambilan keputusan)
- `ai_brain.py` — deteksi intent + jawaban AI (grounded ke FAQ)
- `knowledge_base.py` — memuat & mencari FAQ dari `data/faq.json`
- `greeting.py` — sapaan otomatis (baru/kembali/di luar jam)
- `lead_capture.py` — alur tangkap nama & intent
- `whatsapp_client.py` — kirim pesan (console/Fonnte/Meta)
- `database.py` — penyimpanan SQLite (sesi & lead)
- `simulator.py` — alat uji percakapan tanpa WhatsApp

---

## 💰 Rincian Biaya (Hemat & Normal)

| Komponen | 🟢 HEMAT (Gratis) | 🟡 NORMAL (UMKM) |
|---|---|---|
| Otak AI (Gemini) | Free tier — Rp 0 | Free tier — Rp 0 |
| Gateway WhatsApp | Meta Cloud API (balasan gratis) — Rp 0 | Fonnte — ±Rp 50rb–150rb |
| Hosting 24/7 | Laptop / free tier — Rp 0 | VPS murah — ±Rp 50rb–100rb |
| **TOTAL / BULAN** | **Rp 0** | **±Rp 100rb–250rb** |

> Belajar & uji kelima proyek: **Rp 0**. Detail lengkap + skenario Pro ada di [`TUTORIAL.md`](TUTORIAL.md#14-rincian-biaya-lengkap-hemat--normal).

---

## ⚠️ Disclaimer

Repo ini untuk **edukasi teknologi (AI + otomatisasi bisnis)**. Gunakan WhatsApp sesuai *Business Messaging Policy*: **jangan spam**, kirim hanya ke kontak yang setuju (opt-in), dan lindungi data pribadi pelanggan sesuai **UU PDP**. Penyalahgunaan dapat menyebabkan nomor/akun diblokir.

---

<div align="center">
Dibuat untuk membantu kamu belajar AI Autonomous sambil punya bot WhatsApp yang berguna untuk bisnis. Selamat belajar! 🎓
</div>
