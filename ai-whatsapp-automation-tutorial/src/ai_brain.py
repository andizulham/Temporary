"""
ai_brain.py
===========
"Otak" AI autonomous memakai Gemini. Tugasnya dua:

1. detect_intent()  -> menebak maksud pesan (greeting / faq / lead / other)
2. generate_reply() -> membuat balasan natural yang BERDASAR pada FAQ bisnis
                       (grounded), jadi AI tidak mengarang di luar data kita.

PENTING: modul ini dirancang tetap jalan TANPA API key (mode rule-based),
supaya simulator & testing bisa dijalankan offline / gratis.
"""

from config import settings
from knowledge_base import find_faq, all_faqs_as_text

# Kata kunci untuk deteksi cepat (dipakai sebagai fallback & pemandu)
LEAD_WORDS = [
    "daftar", "mau beli", "beli", "pesan", "order", "konsultasi",
    "tertarik", "minat", "langganan", "mulai", "ambil paket", "deal",
]
GREETING_WORDS = [
    "halo", "hallo", "hai", "hi", "assalamualaikum", "permisi",
    "selamat pagi", "selamat siang", "selamat sore", "selamat malam",
    "pagi", "siang", "sore", "malam", "min", "kak", "bang",
]

_model = None


def _get_model():
    """Memuat model Gemini sekali saja (lazy). None bila AI tidak aktif."""
    global _model
    if not settings.ai_enabled:
        return None
    if _model is None:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        system = (
            f"Kamu adalah CS (customer service) otomatis untuk bisnis "
            f"'{settings.BUSINESS_NAME}'. Jawab dalam Bahasa Indonesia yang ramah, "
            f"singkat (maksimal 4 kalimat), dan sopan. Gunakan HANYA informasi dari "
            f"'DATA BISNIS' di bawah. Jika informasi tidak ada, katakan dengan jujur "
            f"bahwa kamu akan menghubungkan ke tim, jangan mengarang.\n\n"
            f"=== DATA BISNIS ===\n{all_faqs_as_text()}"
        )
        _model = genai.GenerativeModel(
            settings.GEMINI_MODEL, system_instruction=system
        )
    return _model


def detect_intent(text: str) -> str:
    """
    Mengembalikan salah satu: 'lead', 'faq', 'greeting', 'other'.
    Pakai aturan kata kunci -> cepat, gratis, dan mudah diuji.
    """
    t = text.lower().strip()

    # 1. Niat jadi prospek (paling prioritas)
    if any(w in t for w in LEAD_WORDS):
        return "lead"

    # 2. Cocok dengan salah satu FAQ?
    if find_faq(t) is not None:
        return "faq"

    # 3. Sekadar menyapa?
    if any(t == w or t.startswith(w + " ") or w in t.split() for w in GREETING_WORDS):
        return "greeting"

    return "other"


def generate_reply(user_text: str) -> str:
    """
    Membuat balasan untuk pertanyaan umum/FAQ.
    - Jika AI aktif: Gemini menyusun jawaban natural berdasar DATA BISNIS.
    - Jika AI nonaktif: ambil jawaban FAQ apa adanya (rule-based fallback).
    """
    model = _get_model()

    if model is None:
        # Mode hemat / offline: pakai jawaban FAQ langsung
        faq = find_faq(user_text)
        if faq:
            return faq["jawaban"]
        return (
            "Maaf, aku belum punya jawaban pasti untuk itu. "
            "Kamu bisa tanya soal harga, lokasi, jam buka, cara pesan, "
            "garansi, atau pembayaran. Atau ketik *DAFTAR* untuk dibantu tim kami."
        )

    # Mode AI: biarkan Gemini menyusun jawaban yang grounded
    try:
        resp = model.generate_content(user_text)
        return (resp.text or "").strip() or _fallback(user_text)
    except Exception:
        # Bila API error/limit, jangan sampai bot mati -> pakai fallback
        return _fallback(user_text)


def _fallback(user_text: str) -> str:
    faq = find_faq(user_text)
    if faq:
        return faq["jawaban"]
    return (
        "Maaf, koneksi ke asisten AI sedang sibuk. "
        "Coba tanyakan lagi sebentar lagi ya, atau ketik *DAFTAR* "
        "agar tim kami menghubungi kamu."
    )


if __name__ == "__main__":
    print("AI aktif?", settings.ai_enabled)
    for q in ["halo kak", "berapa harganya?", "saya mau daftar", "bisa kirim ke luar negeri?"]:
        print(f"\n[{detect_intent(q):8}] {q}")
        print("->", generate_reply(q))
