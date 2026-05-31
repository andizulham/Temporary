"""
config.py
=========
Membaca semua pengaturan dari file .env supaya rahasia (API key/token)
tidak ditulis langsung di dalam kode (lebih aman & mudah diganti).

Pakai:
    from config import settings
    print(settings.BUSINESS_NAME)
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Muat variabel dari file .env yang ada di folder proyek
load_dotenv()


@dataclass
class Settings:
    """Kumpulan pengaturan aplikasi (dibaca sekali saat start)."""

    # --- Otak AI ---
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # --- Gateway WhatsApp: "fonnte" | "meta" | "console" ---
    WHATSAPP_PROVIDER: str = os.getenv("WHATSAPP_PROVIDER", "console").lower()

    # Fonnte (gateway lokal Indonesia)
    FONNTE_TOKEN: str = os.getenv("FONNTE_TOKEN", "")

    # Meta WhatsApp Cloud API (resmi)
    META_WA_TOKEN: str = os.getenv("META_WA_TOKEN", "")
    META_WA_PHONE_NUMBER_ID: str = os.getenv("META_WA_PHONE_NUMBER_ID", "")
    META_VERIFY_TOKEN: str = os.getenv("META_VERIFY_TOKEN", "rahasia123")

    # --- Identitas bisnis ---
    BUSINESS_NAME: str = os.getenv("BUSINESS_NAME", "Toko Maju Jaya")
    BUSINESS_HOURS: str = os.getenv("BUSINESS_HOURS", "Senin-Jumat 09.00-18.00 WIB")
    TIMEZONE_OFFSET: int = int(os.getenv("TIMEZONE_OFFSET", "7"))

    # --- Penyimpanan ---
    DB_PATH: str = os.getenv("DB_PATH", "leads.db")

    @property
    def ai_enabled(self) -> bool:
        """True jika Gemini API key tersedia (mode AI aktif)."""
        return bool(self.GEMINI_API_KEY)


# Objek tunggal yang dipakai di seluruh proyek
settings = Settings()
