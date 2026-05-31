"""
app.py
======
Server webhook (Flask) yang MENERIMA pesan WhatsApp lalu membalas otomatis.
Inilah "pintu masuk" pesan dari dunia luar menuju otak bot (bot.handle_message).

Cara kerja singkat:
    WhatsApp/Gateway  --(webhook POST)-->  app.py  -->  bot.handle_message()
                                                  -->  whatsapp_client.send_message()

Jalankan lokal:
    python src/app.py
Lalu buka tunnel publik (mis. ngrok http 5000) dan daftarkan URL-nya
di dashboard Fonnte / Meta sebagai webhook.

Endpoint:
- GET  /            -> cek server hidup
- GET  /webhook     -> verifikasi webhook Meta (hub.challenge)
- POST /webhook     -> terima pesan (Fonnte ATAU Meta)
"""

from flask import Flask, request, jsonify

from config import settings
from bot import handle_message
from whatsapp_client import send_message

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify({
        "service": "AI WhatsApp Automation",
        "business": settings.BUSINESS_NAME,
        "provider": settings.WHATSAPP_PROVIDER,
        "ai_enabled": settings.ai_enabled,
        "status": "ok",
    })


@app.get("/webhook")
def verify():
    """Verifikasi webhook untuk Meta Cloud API (langkah wajib sekali saja)."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == settings.META_VERIFY_TOKEN:
        return challenge or "", 200
    return "Verifikasi gagal", 403


@app.post("/webhook")
def incoming():
    """Terima pesan masuk dari gateway, balas otomatis."""
    data = request.get_json(silent=True) or request.form.to_dict()
    parsed = _parse_incoming(data)

    if not parsed:
        # Bukan pesan teks (mis. status update) -> abaikan dengan sopan
        return jsonify({"ignored": True}), 200

    phone, text = parsed
    replies = handle_message(phone, text)
    results = [send_message(phone, r) for r in replies]
    return jsonify({"phone": phone, "replies": len(replies), "results": results}), 200


def _parse_incoming(data: dict):
    """
    Menyeragamkan format pesan dari Fonnte ATAU Meta menjadi (phone, text).
    Mengembalikan None bila bukan pesan teks yang relevan.
    """
    # --- Format Fonnte: {"sender": "628..", "message": "halo", ...} ---
    if isinstance(data, dict) and data.get("sender") and data.get("message"):
        return str(data["sender"]), str(data["message"])

    # --- Format Meta Cloud API (bertingkat) ---
    try:
        entry = data["entry"][0]["changes"][0]["value"]
        msg = entry["messages"][0]
        if msg.get("type") == "text":
            return msg["from"], msg["text"]["body"]
    except (KeyError, IndexError, TypeError):
        pass

    return None


if __name__ == "__main__":
    # host 0.0.0.0 supaya bisa diakses tunnel (ngrok/cloudflared)
    app.run(host="0.0.0.0", port=5000, debug=True)
