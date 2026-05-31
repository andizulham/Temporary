"""
knowledge_base.py
=================
Memuat "otak pengetahuan" bisnis dari data/faq.json dan menyediakan
fungsi pencarian FAQ sederhana berbasis kata kunci (keyword matching).

Kenapa file JSON terpisah? Supaya kamu (atau klien) bisa mengubah FAQ
TANPA menyentuh kode Python -- ramah no-code.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
FAQ_PATH = os.path.join(ROOT, "data", "faq.json")

_cache = None


def load_kb() -> dict:
    """Membaca file faq.json (di-cache supaya tidak dibaca berulang)."""
    global _cache
    if _cache is None:
        with open(FAQ_PATH, "r", encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9\s]", " ", text.lower())


def find_faq(text: str) -> dict | None:
    """
    Cari FAQ paling cocok berdasarkan jumlah kata kunci yang muncul di pesan.
    Mengembalikan dict FAQ atau None bila tidak ada yang cocok.
    """
    kb = load_kb()
    words = set(_normalize(text).split())
    best, best_score = None, 0
    for faq in kb["faqs"]:
        score = sum(1 for kw in faq["keywords"] if kw in words)
        if score > best_score:
            best, best_score = faq, score
    return best if best_score > 0 else None


def all_faqs_as_text() -> str:
    """Rangkai seluruh FAQ jadi satu teks -- dipakai sebagai konteks untuk AI."""
    kb = load_kb()
    biz = kb["business"]
    lines = [
        f"Nama bisnis: {biz['name']}",
        f"Deskripsi: {biz['deskripsi']}",
        f"Alamat: {biz['alamat']}",
        f"Jam operasional: {biz['jam_operasional']}",
        f"Kontak: {biz['kontak']}",
        "",
        "Daftar FAQ:",
    ]
    for faq in kb["faqs"]:
        lines.append(f"- T: {faq['pertanyaan']}\n  J: {faq['jawaban']}")
    return "\n".join(lines)


def faq_menu() -> str:
    """Menu singkat berisi topik FAQ -- ditampilkan di sapaan."""
    kb = load_kb()
    topik = {
        "harga": "Harga & Paket",
        "lokasi": "Lokasi",
        "jam": "Jam Operasional",
        "cara_pesan": "Cara Pesan",
        "garansi": "Garansi & Revisi",
        "pembayaran": "Pembayaran",
    }
    items = [topik.get(f["id"], f["id"]) for f in kb["faqs"]]
    return "  •  ".join(items)


if __name__ == "__main__":
    print("== Tes pencarian FAQ ==")
    for q in ["berapa harganya ya?", "kantornya dimana", "halo kak"]:
        hit = find_faq(q)
        print(f"\nPertanyaan: {q}")
        print("Cocok:", hit["id"] if hit else "(tidak ada -> fallback)")
