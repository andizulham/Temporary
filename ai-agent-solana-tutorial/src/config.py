"""
config.py
=========
Membaca semua pengaturan dari file .env supaya API key tidak ditulis
langsung di dalam kode (lebih aman & mudah diganti).

Pakai:
    from config import settings
    print(settings.GEMINI_API_KEY)
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Muat variabel dari file .env yang ada di root project
load_dotenv()


@dataclass
class Settings:
    """Kumpulan pengaturan aplikasi (dibaca sekali saat start)."""

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    HELIUS_API_KEY: str = os.getenv("HELIUS_API_KEY", "")
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    WALLET_ADDRESS: str = os.getenv("WALLET_ADDRESS", "")
    USD_TO_IDR: int = int(os.getenv("USD_TO_IDR", "16300"))

    # Lokasi database SQLite untuk menyimpan riwayat trade
    DB_PATH: str = os.getenv("DB_PATH", "trades.db")

    def validate(self) -> list[str]:
        """Mengembalikan daftar pengaturan penting yang masih kosong."""
        missing = []
        if not self.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
        if not self.HELIUS_API_KEY:
            missing.append("HELIUS_API_KEY")
        if not self.WALLET_ADDRESS:
            missing.append("WALLET_ADDRESS")
        return missing


# Objek tunggal yang dipakai di seluruh project
settings = Settings()
