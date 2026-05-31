"""
test_bot.py
===========
Uji otomatis untuk memastikan lima fitur inti bekerja:
1. Auto-reply (bot selalu membalas)
2. Auto greeting (kontak baru disapa)
3. FAQ automation (pertanyaan harga/lokasi dijawab)
4. Lead capture (nama & intent tersimpan)
5. Deteksi intent (klasifikasi pesan)

Jalankan: pytest -q   (dari folder ai-whatsapp-automation-tutorial)
"""

import uuid

import bot
import ai_brain
import greeting
from database import count_leads, get_leads
from datetime import datetime


def _new_phone() -> str:
    """Nomor unik per test supaya state tidak bocor antar test."""
    return "62" + uuid.uuid4().hex[:11]


# ---------------------------------------------------------------- auto reply
def test_selalu_membalas():
    phone = _new_phone()
    replies = bot.handle_message(phone, "halo")
    assert isinstance(replies, list) and len(replies) >= 1
    assert all(isinstance(r, str) and r for r in replies)


# ------------------------------------------------------------- auto greeting
def test_kontak_baru_disapa():
    phone = _new_phone()
    replies = bot.handle_message(phone, "hai")
    gabung = " ".join(replies).lower()
    assert "toko maju jaya" in gabung
    # Kontak baru harus mendapat menu pilihan
    assert "harga" in gabung


def test_greeting_after_hours():
    minggu = datetime(2026, 5, 31, 10, 0)  # 31 Mei 2026 = Minggu (tutup)
    pesan = greeting.greeting_message(is_returning=False, now=minggu)
    assert "luar jam kerja" in pesan.lower()


def test_business_hours_true():
    senin_siang = datetime(2026, 6, 1, 11, 0)  # Senin 11.00
    assert greeting.is_business_hours(senin_siang) is True


# ------------------------------------------------------------- FAQ automation
def test_faq_harga_dijawab():
    phone = _new_phone()
    bot.handle_message(phone, "halo")              # sapaan dulu (kontak baru)
    replies = bot.handle_message(phone, "berapa harganya?")
    gabung = " ".join(replies).lower()
    assert "paket" in gabung and "rp" in gabung


def test_faq_lokasi_dijawab():
    phone = _new_phone()
    bot.handle_message(phone, "halo")
    replies = bot.handle_message(phone, "alamat kantornya dimana ya")
    assert "sudirman" in " ".join(replies).lower()


# ---------------------------------------------------------------- intent
def test_deteksi_intent():
    assert ai_brain.detect_intent("saya mau daftar") == "lead"
    assert ai_brain.detect_intent("berapa harga paket") == "faq"
    assert ai_brain.detect_intent("halo kak") == "greeting"


# ------------------------------------------------------------- lead capture
def test_lead_capture_tersimpan():
    sebelum = count_leads()
    phone = _new_phone()
    bot.handle_message(phone, "halo")              # sapaan
    bot.handle_message(phone, "saya mau daftar")   # mulai capture -> tanya nama
    bot.handle_message(phone, "Andi Zulham")       # nama -> tanya intent
    konfirmasi = bot.handle_message(phone, "1")    # intent -> simpan

    assert count_leads() == sebelum + 1
    lead = get_leads(1)[0]
    assert lead["name"] == "Andi Zulham"
    assert lead["intent"] == "Beli Produk/Paket"
    assert "tercatat" in " ".join(konfirmasi).lower()


def test_lead_capture_bisa_dibatalkan():
    phone = _new_phone()
    bot.handle_message(phone, "halo")
    bot.handle_message(phone, "mau daftar")
    replies = bot.handle_message(phone, "batal")
    assert "dibatalkan" in " ".join(replies).lower()
