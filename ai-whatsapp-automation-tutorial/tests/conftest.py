"""
conftest.py
===========
Persiapan sebelum test dijalankan:
- Tambahkan folder src/ ke path agar modul bisa di-import.
- Pakai database SEMENTARA & provider "console" supaya test tidak menyentuh
  data asli atau jaringan.

Pytest otomatis memuat file ini lebih dulu, jadi pengaturan env di sini
sudah aktif sebelum modul aplikasi di-import.
"""

import os
import sys
import tempfile

# 1) Arahkan ke folder src/
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "src"))
sys.path.insert(0, SRC)

# 2) Lingkungan uji yang terisolasi (database sementara, tanpa AI/jaringan)
_tmp_db = os.path.join(tempfile.gettempdir(), "leads_test.db")
if os.path.exists(_tmp_db):
    os.remove(_tmp_db)
os.environ["DB_PATH"] = _tmp_db
os.environ["WHATSAPP_PROVIDER"] = "console"
os.environ["GEMINI_API_KEY"] = ""          # paksa mode rule-based (deterministik)
os.environ["BUSINESS_NAME"] = "Toko Maju Jaya"
