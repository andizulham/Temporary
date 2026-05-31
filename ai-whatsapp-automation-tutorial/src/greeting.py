"""
greeting.py
===========
Membuat pesan sapaan otomatis (auto greeting). Ada 3 varian:

1. Kontak BARU            -> sapaan + menu pilihan
2. Kontak yang KEMBALI    -> sapaan "selamat datang kembali"
3. Di LUAR jam kerja      -> beri tahu jam buka + tetap bantu

Logika jam kerja sederhana: Senin-Jumat 09.00-18.00, Sabtu 09.00-14.00
(zona waktu mengikuti TIMEZONE_OFFSET di .env, default WIB = +7).
"""

from datetime import datetime, timezone, timedelta

from config import settings
from knowledge_base import faq_menu


def is_business_hours(now: datetime = None) -> bool:
    """True bila saat ini termasuk jam kerja bisnis."""
    if now is None:
        tz = timezone(timedelta(hours=settings.TIMEZONE_OFFSET))
        now = datetime.now(tz)
    weekday = now.weekday()  # 0=Senin ... 6=Minggu
    hour = now.hour
    if weekday <= 4:          # Senin-Jumat
        return 9 <= hour < 18
    if weekday == 5:          # Sabtu
        return 9 <= hour < 14
    return False              # Minggu: tutup


def _menu_block() -> str:
    return (
        "Silakan tanya apa saja, atau pilih topik berikut:\n"
        "1) Harga & Paket\n"
        "2) Lokasi\n"
        "3) Jam Operasional\n"
        "4) Cara Pesan\n"
        "Ketik *DAFTAR* kalau mau langsung dibantu tim kami."
    )


def greeting_message(is_returning: bool = False, now: datetime = None) -> str:
    """Pilih sapaan yang tepat sesuai kondisi kontak & jam."""
    nama = settings.BUSINESS_NAME

    if not is_business_hours(now):
        return (
            f"Halo! 👋 Terima kasih sudah menghubungi *{nama}*.\n\n"
            f"Saat ini di luar jam kerja kami ({settings.BUSINESS_HOURS}). "
            f"Tapi tenang, asisten otomatis ini siap 24 jam untuk membantu.\n\n"
            f"{_menu_block()}"
        )

    if is_returning:
        return (
            f"Selamat datang kembali! 👋 Senang melihatmu lagi di *{nama}*.\n\n"
            f"Ada yang bisa kami bantu hari ini?\n\n{_menu_block()}"
        )

    return (
        f"Halo! 👋 Terima kasih sudah menghubungi *{nama}*.\n\n"
        f"Aku asisten otomatis yang siap membantu kamu.\n\n{_menu_block()}"
    )


if __name__ == "__main__":
    print("Jam kerja sekarang?", is_business_hours())
    print("\n--- KONTAK BARU ---\n", greeting_message(is_returning=False))
    print("\n--- KONTAK KEMBALI ---\n", greeting_message(is_returning=True))
