"""
whatsapp_client.py
==================
Mengirim pesan balasan ke WhatsApp. Mendukung 3 mode (diatur lewat
WHATSAPP_PROVIDER di .env):

- "console" : hanya cetak ke layar (default, untuk belajar/testing, GRATIS)
- "fonnte"  : gateway WhatsApp lokal Indonesia (paling mudah & murah)
- "meta"    : WhatsApp Cloud API resmi dari Meta

Dengan pola ini, logika bot tidak perlu tahu detail provider -- tinggal
panggil send_message(nomor, teks).
"""

import requests

from config import settings


def send_message(phone: str, text: str) -> dict:
    """Kirim satu pesan teks ke nomor tujuan, sesuai provider terpilih."""
    provider = settings.WHATSAPP_PROVIDER
    if provider == "fonnte":
        return _send_fonnte(phone, text)
    if provider == "meta":
        return _send_meta(phone, text)
    return _send_console(phone, text)


# ----------------------------- CONSOLE -------------------------------------
def _send_console(phone: str, text: str) -> dict:
    print(f"\n[KIRIM -> {phone}]\n{text}\n" + "-" * 40)
    return {"provider": "console", "ok": True}


# ----------------------------- FONNTE --------------------------------------
def _send_fonnte(phone: str, text: str) -> dict:
    """
    Fonnte: kirim POST ke https://api.fonnte.com/send dengan header Authorization.
    Dok: https://docs.fonnte.com
    """
    if not settings.FONNTE_TOKEN:
        return {"provider": "fonnte", "ok": False, "error": "FONNTE_TOKEN kosong"}
    try:
        resp = requests.post(
            "https://api.fonnte.com/send",
            headers={"Authorization": settings.FONNTE_TOKEN},
            data={"target": phone, "message": text},
            timeout=20,
        )
        return {"provider": "fonnte", "ok": resp.ok, "status": resp.status_code,
                "body": resp.text}
    except Exception as e:  # jangan sampai bot mati gara-gara jaringan
        return {"provider": "fonnte", "ok": False, "error": str(e)}


# ----------------------------- META CLOUD API ------------------------------
def _send_meta(phone: str, text: str) -> dict:
    """
    Meta WhatsApp Cloud API: POST ke /{phone_number_id}/messages.
    Dok: https://developers.facebook.com/docs/whatsapp/cloud-api
    """
    if not (settings.META_WA_TOKEN and settings.META_WA_PHONE_NUMBER_ID):
        return {"provider": "meta", "ok": False, "error": "Kredensial Meta belum lengkap"}
    url = f"https://graph.facebook.com/v21.0/{settings.META_WA_PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": text},
    }
    try:
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {settings.META_WA_TOKEN}",
                     "Content-Type": "application/json"},
            json=payload,
            timeout=20,
        )
        return {"provider": "meta", "ok": resp.ok, "status": resp.status_code,
                "body": resp.text}
    except Exception as e:
        return {"provider": "meta", "ok": False, "error": str(e)}


if __name__ == "__main__":
    print("Provider aktif:", settings.WHATSAPP_PROVIDER)
    print(send_message("628123456789", "Tes kirim pesan dari bot 👋"))
