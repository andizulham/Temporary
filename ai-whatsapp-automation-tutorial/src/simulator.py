"""
simulator.py
============
Alat untuk MENGUJI bot tanpa WhatsApp asli (Level 8: Testing & Optimasi).
Kamu bisa mengetik seperti pelanggan, lalu melihat balasan bot langsung di
terminal. Gratis, cepat, dan tidak butuh API key.

Cara pakai:
    python src/simulator.py            # mode chat interaktif
    python src/simulator.py demo       # jalankan skenario contoh otomatis
    python src/simulator.py leads      # lihat lead yang sudah tertangkap
"""

import sys

from bot import handle_message
from database import init_db, get_leads, count_leads


NOMOR_UJI = "628999000111"


def _print_replies(replies):
    for r in replies:
        print(f"🤖 {r}\n")


def chat():
    init_db()
    print("=" * 56)
    print("  SIMULATOR WHATSAPP BOT  (ketik 'exit' untuk keluar)")
    print("  Berperanlah sebagai pelanggan. Balasan bot muncul di bawah.")
    print("=" * 56)
    while True:
        try:
            msg = input("\n👤 Kamu: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSampai jumpa!")
            break
        if msg.lower() in ("exit", "quit", "keluar"):
            print("Sampai jumpa!")
            break
        if not msg:
            continue
        _print_replies(handle_message(NOMOR_UJI, msg))


def demo():
    """Skenario contoh: dari sapaan sampai lead tertangkap."""
    init_db()
    skenario = [
        "halo kak",
        "berapa harga paketnya?",
        "lokasi kantornya di mana?",
        "oke saya mau daftar",
        "Andi Zulham",
        "1",
        "menu",
    ]
    nomor = "628777000222"
    print("=" * 56)
    print("  DEMO PERCAKAPAN OTOMATIS")
    print("=" * 56)
    for pesan in skenario:
        print(f"\n👤 {pesan}")
        _print_replies(handle_message(nomor, pesan))
    print(f"Total lead tersimpan sekarang: {count_leads()}")


def show_leads():
    init_db()
    leads = get_leads()
    if not leads:
        print("Belum ada lead tertangkap. Jalankan 'demo' atau 'chat' dulu.")
        return
    print(f"== {len(leads)} LEAD TERAKHIR ==")
    for l in leads:
        print(f"#{l['id']:<3} {l['name']:<20} | {l['intent']:<22} | {l['phone']} | {l['created_at'][:19]}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "chat"
    if cmd == "demo":
        demo()
    elif cmd == "leads":
        show_leads()
    else:
        chat()
