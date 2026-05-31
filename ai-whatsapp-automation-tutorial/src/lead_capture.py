"""
lead_capture.py
===============
Alur menangkap prospek (lead) secara bertahap lewat percakapan:

    mulai  ->  tanya NAMA  ->  tanya KEBUTUHAN/INTENT  ->  simpan + konfirmasi

Status percakapan disimpan di tabel 'sessions' (lihat database.py), sehingga
bot ingat sudah sampai langkah mana untuk tiap nomor.
"""

from config import settings
from database import update_session, save_lead

# Pilihan intent yang umum (boleh dijawab dengan angka atau teks bebas)
INTENT_OPTIONS = {
    "1": "Beli Produk/Paket",
    "2": "Tanya Layanan",
    "3": "Kerja Sama / B2B",
    "4": "Konsultasi Umum",
    "5": "Lainnya",
}


def start(phone: str) -> str:
    """Mulai alur lead capture: minta nama lebih dulu."""
    update_session(phone, state="AWAITING_NAME")
    return (
        "Sip! Aku bantu daftarkan ya. 🎯\n\n"
        "Boleh tahu *nama lengkap* kamu dulu?"
    )


def step(phone: str, text: str, session: dict) -> str:
    """
    Lanjutkan alur sesuai state saat ini.
    Dipanggil oleh bot.py ketika session['state'] termasuk langkah lead capture.
    """
    state = session["state"]
    text = text.strip()

    # Langkah 1: terima NAMA -> minta intent
    if state == "AWAITING_NAME":
        name = text[:60] if text else "Calon Pelanggan"
        update_session(phone, state="AWAITING_INTENT", temp_name=name)
        opsi = "\n".join(f"{k}) {v}" for k, v in INTENT_OPTIONS.items())
        return (
            f"Terima kasih, *{name}*! 🙏\n\n"
            f"Apa yang kamu butuhkan? Balas dengan angka atau tulis langsung:\n{opsi}"
        )

    # Langkah 2: terima INTENT -> simpan lead + konfirmasi
    if state == "AWAITING_INTENT":
        intent = INTENT_OPTIONS.get(text, text[:80] if text else "Tidak disebutkan")
        name = session.get("temp_name") or "Calon Pelanggan"
        lead_id = save_lead(phone=phone, name=name, intent=intent,
                            note="Ditangkap via WhatsApp bot")
        update_session(phone, state="DONE", temp_name=None)
        return (
            f"Sudah tercatat ✅\n\n"
            f"👤 Nama   : {name}\n"
            f"📱 Nomor  : {phone}\n"
            f"🏷️ Kebutuhan: {intent}\n\n"
            f"Tim *{settings.BUSINESS_NAME}* akan menghubungi kamu dalam 1x24 jam kerja. "
            f"Ada lagi yang bisa kubantu? Ketik *MENU* untuk pilihan lain."
        )

    # Tidak seharusnya sampai sini, tapi aman-amankan:
    update_session(phone, state="BROWSING")
    return "Baik, ada lagi yang bisa kubantu?"


def is_capturing(state: str) -> bool:
    """True bila state sedang berada di tengah alur lead capture."""
    return state in ("AWAITING_NAME", "AWAITING_INTENT")
