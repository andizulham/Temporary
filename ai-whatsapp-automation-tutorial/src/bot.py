"""
bot.py
======
INTI sistem: "router" autonomous yang memutuskan balasan untuk SETIAP pesan
masuk. Dibuat sengaja TERPISAH dari WhatsApp supaya bisa diuji sendiri
(lihat simulator.py & tests/).

Alur keputusan (lihat diagram 04_alur_percakapan.png):

    pesan masuk
        │
        ├─ sedang isi data lead?  ─► lanjutkan lead capture
        ├─ kontak baru?           ─► kirim sapaan (auto greeting)
        ├─ niat mendaftar?        ─► mulai lead capture (tanya nama & intent)
        ├─ cocok FAQ / pertanyaan ─► jawab via AI (grounded ke FAQ)
        └─ sapaan / lain-lain     ─► sapaan / jawaban umum

Fungsi utama: handle_message(phone, text) -> list[str]  (daftar balasan)
"""

from database import init_db, get_session, update_session, is_returning
from greeting import greeting_message
from ai_brain import detect_intent, generate_reply
import lead_capture

# Perintah khusus
CANCEL_WORDS = {"batal", "cancel", "stop", "keluar"}
MENU_WORDS = {"menu", "/start", "start", "mulai lagi"}

_initialized = False


def _ensure_db():
    global _initialized
    if not _initialized:
        init_db()
        _initialized = True


def handle_message(phone: str, text: str) -> list[str]:
    """
    Terima satu pesan dari sebuah nomor, kembalikan daftar balasan (1-2 pesan).
    Inilah satu-satunya pintu yang dipakai oleh webhook & simulator.
    """
    _ensure_db()
    text = (text or "").strip()
    session = get_session(phone)
    state = session["state"]
    returning = is_returning(phone)
    low = text.lower()

    replies: list[str] = []

    # 0) Batalkan alur pendaftaran bila diminta
    if state in ("AWAITING_NAME", "AWAITING_INTENT") and low in CANCEL_WORDS:
        update_session(phone, state="BROWSING", temp_name=None)
        replies.append("Oke, pendaftaran dibatalkan. Ada lagi yang bisa kubantu? Ketik *MENU* ya.")
        _finish(phone)
        return replies

    # 1) Sedang di tengah alur lead capture -> teruskan langkahnya
    if lead_capture.is_capturing(state):
        replies.append(lead_capture.step(phone, text, session))
        _finish(phone)
        return replies

    # 2) Permintaan menu eksplisit
    if low in MENU_WORDS:
        replies.append(greeting_message(is_returning=returning))
        update_session(phone, state="BROWSING")
        _finish(phone)
        return replies

    intent = detect_intent(text)

    # 3) Kontak BARU -> selalu sapa dulu (auto greeting)
    if not returning:
        replies.append(greeting_message(is_returning=False))
        update_session(phone, state="BROWSING")
        # Bila pesan pertama sudah berisi niat jelas, layani sekalian
        if intent == "lead":
            replies.append(lead_capture.start(phone))
        elif intent == "faq":
            replies.append(generate_reply(text))
        _finish(phone)
        return replies

    # 4) Kontak LAMA -> rutekan sesuai niat
    if intent == "lead":
        # Mulai lead capture (state -> AWAITING_NAME). JANGAN di-reset ke BROWSING.
        replies.append(lead_capture.start(phone))
    elif intent == "faq":
        replies.append(generate_reply(text))
        update_session(phone, state="BROWSING")
    elif intent == "greeting":
        replies.append(greeting_message(is_returning=True))
        update_session(phone, state="BROWSING")
    else:  # "other" -> serahkan ke AI (atau fallback bila AI nonaktif)
        replies.append(generate_reply(text))
        update_session(phone, state="BROWSING")

    _finish(phone)
    return replies


def _finish(phone: str):
    """Tandai bahwa nomor ini sudah pernah berinteraksi (hitung pesan)."""
    update_session(phone, bump_count=True)


if __name__ == "__main__":
    # Demo cepat satu percakapan
    nomor = "628111111111"
    for pesan in ["halo", "berapa harga paketnya?", "saya mau daftar", "Budi Santoso", "1"]:
        print(f"\n👤 {pesan}")
        for r in handle_message(nomor, pesan):
            print(f"🤖 {r}")
