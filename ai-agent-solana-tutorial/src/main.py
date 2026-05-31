"""
main.py
=======
Titik masuk berbasis terminal (CLI) untuk menjalankan AI Agent tanpa Telegram.
Berguna untuk belajar/tes cepat sebelum deploy bot.

Contoh pakai:
    python main.py sync          # tarik transaksi dompet -> database
    python main.py ringkasan     # tampilkan statistik
    python main.py evaluasi      # minta AI evaluasi trading
    python main.py tanya "Apakah saya overtrading minggu ini?"
"""

from __future__ import annotations

import sys

from config import settings
from tracker import sync_wallet, summarize, get_recent_trades
from evaluator import evaluate_trades, run_agent


def cek_konfigurasi() -> bool:
    missing = settings.validate()
    if missing:
        print("⚠️  Pengaturan berikut masih kosong di .env:", ", ".join(missing))
        print("   Salin .env.example menjadi .env lalu isi nilainya.")
        return False
    return True


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        return

    perintah = sys.argv[1].lower()

    if perintah == "sync":
        if not cek_konfigurasi():
            return
        n = sync_wallet()
        print(f"✅ {n} trade baru tersimpan.")

    elif perintah == "ringkasan":
        s = summarize()
        print("📊 Ringkasan Trade")
        print(f"   Total trade  : {s['total_trades']}")
        print(f"   Trade pertama: {s['first_trade']}")
        print(f"   Trade terakhir: {s['last_trade']}")
        for t in get_recent_trades(10):
            print(f"   - [{t['type']}] {t['description'][:70]}")

    elif perintah == "evaluasi":
        if not cek_konfigurasi():
            return
        print(evaluate_trades())

    elif perintah == "tanya":
        if not cek_konfigurasi():
            return
        pertanyaan = " ".join(sys.argv[2:]) or "Tolong evaluasi trading saya."
        print(run_agent(pertanyaan))

    else:
        print(f"Perintah tidak dikenal: {perintah}")
        print(__doc__)


if __name__ == "__main__":
    main()
