<div align="center">

# 🤖 Belajar AI Agent dari Nol sampai Mahir
### Proyek Nyata: AI Agent Pelacak & Evaluator Trading Crypto di Jaringan Solana

Panduan lengkap berbahasa Indonesia + kode siap pakai + diagram + rincian biaya (Rupiah).

</div>

---

## 📦 Isi Repo Ini

| File / Folder | Keterangan |
|---|---|
| **[`TUTORIAL.md`](TUTORIAL.md)** | Tutorial lengkap zero-to-hero (10 level) dalam Bahasa Indonesia |
| **[`docs/Tutorial-AI-Agent-Solana-Trading.pdf`](docs/Tutorial-AI-Agent-Solana-Trading.pdf)** | Versi PDF tutorial (dengan gambar & rincian biaya) |
| `docs/images/` | Diagram pembantu (roadmap, arsitektur, alur data, biaya) |
| `src/` | Kode proyek nyata (Python) — siap dijalankan |
| `scripts/` | Skrip pembuat diagram & PDF |
| `requirements.txt` | Daftar dependensi Python |
| `.env.example` | Contoh konfigurasi (salin jadi `.env`) |

---

## 🎯 Apa yang Kamu Pelajari

Dari **nol** sampai **mahir**, melalui 10 level bertahap:

`Fondasi → Akun & Platform → Lingkungan → Hello Agent → Data Solana → Tracker → Evaluator → Mode Agent (function calling) → Telegram Bot → Deploy 24/7 → Hero (multi-agent, RAG, backtest, no-code)`

Semua platform **bisa diakses dari Indonesia** dan punya **paket gratis**:
- **Gemini** (Google AI Studio) — otak AI
- **Helius** + **DexScreener** — data on-chain Solana
- **Telegram Bot** — antarmuka

> 💡 Belajar dari nol sampai Level 8 **bisa Rp 0** (semua pakai paket gratis). Lihat rincian biaya lengkap di tutorial.

---

## 🚀 Cara Cepat Menjalankan

```bash
# 1. Masuk ke folder proyek
cd ai-agent-solana-tutorial

# 2. Buat virtual environment & install dependensi
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Siapkan konfigurasi (isi API key kamu)
cp .env.example .env            # Windows: copy .env.example .env

# 4. Jalankan
python src/main.py sync         # tarik & simpan transaksi dompet
python src/main.py ringkasan    # statistik trade
python src/main.py evaluasi     # AI menilai trading kamu
python src/main.py tanya "Apakah saya overtrading minggu ini?"

# 5. (Opsional) jalankan bot Telegram
python src/telegram_bot.py
```

### Membuat ulang diagram & PDF
```bash
python scripts/generate_diagrams.py   # buat gambar di docs/images/
python scripts/build_pdf.py           # buat docs/Tutorial-...pdf
```

---

## 🔑 API Key yang Dibutuhkan (semua gratis)

| Variabel `.env` | Dapatkan di |
|---|---|
| `GEMINI_API_KEY` | https://aistudio.google.com/app/apikey |
| `HELIUS_API_KEY` | https://dashboard.helius.dev |
| `TELEGRAM_BOT_TOKEN` | Chat `@BotFather` di Telegram → `/newbot` |
| `WALLET_ADDRESS` | Alamat publik dompet Solana yang ingin dipantau |

---

## 🧩 Arsitektur Singkat

```
Solana (Helius + DexScreener)  →  AI Agent (Python)  →  Gemini (analisa)
                                        │
                                    SQLite (memory)
                                        │
                                   Telegram Bot  ←→  Kamu
```

Modul utama di `src/`:
- `solana_client.py` — ambil harga token (DexScreener) & riwayat dompet (Helius)
- `tracker.py` — simpan trade ke SQLite + ringkasan
- `evaluator.py` — Gemini menilai trade + mode agent (function calling)
- `telegram_bot.py` — antarmuka chat
- `main.py` — antarmuka terminal (CLI)

---

## ⚠️ Disclaimer

Repo ini untuk **edukasi teknologi (AI + pemrograman)**, **BUKAN nasihat keuangan/investasi**.
Trading crypto sangat berisiko. AI Agent di sini membantu **mencatat & menganalisa** keputusanmu, bukan menjamin profit.
**Jangan pernah** membagikan *private key* / *seed phrase* — cukup pakai **alamat publik** untuk memantau. Selalu **DYOR**.

---

<div align="center">
Dibuat untuk membantu kamu belajar AI Agent sambil punya alat bantu trading Solana. Selamat belajar! 🎓
</div>
