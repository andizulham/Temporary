"""
generate_diagrams.py
====================
Membuat semua gambar/diagram pembantu untuk tutorial (disimpan di docs/images/).
Jalankan: python scripts/generate_diagrams.py

Memakai matplotlib murni (tanpa dependensi sistem) supaya andal di mana saja.
"""

import os
import math
import matplotlib
matplotlib.use("Agg")  # backend non-interaktif (tanpa layar)
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

# ---- Palet warna konsisten (tema WhatsApp hijau + biru) ----
NAVY = "#0B2A3A"
GREEN = "#128C7E"      # WhatsApp teal-green
LIGHTGREEN = "#25D366"  # WhatsApp bright green
BLUE = "#1565C0"
TEAL = "#00897B"
PURPLE = "#6A1B9A"
AMBER = "#F9A825"
RED = "#C62828"
GREY = "#455A64"
LIGHT = "#ECEFF1"
WHITE = "#FFFFFF"

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "images")
OUT_DIR = os.path.abspath(OUT_DIR)
os.makedirs(OUT_DIR, exist_ok=True)


def _save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print("OK  ", path)


def _box(ax, x, y, w, h, text, fc, tc=WHITE, fs=11, bold=True, radius=0.02):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.01,rounding_size={radius}",
        linewidth=1.2, edgecolor="white", facecolor=fc, zorder=2,
    )
    ax.add_patch(box)
    ax.text(
        x + w / 2, y + h / 2, text, ha="center", va="center",
        color=tc, fontsize=fs, fontweight="bold" if bold else "normal",
        zorder=3, wrap=True,
    )


def _arrow(ax, x1, y1, x2, y2, color=GREY, lw=2):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=18,
        linewidth=lw, color=color, zorder=1,
    ))


# =====================================================================
# 0. COVER
# =====================================================================
def cover():
    fig, ax = plt.subplots(figsize=(9, 5.2))
    fig.patch.set_facecolor(NAVY)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    ax.text(5, 5.15, "AI AUTONOMOUS", ha="center", color=WHITE,
            fontsize=33, fontweight="bold")
    ax.text(5, 4.4, "WHATSAPP AUTOMATION", ha="center", color=LIGHTGREEN,
            fontsize=22, fontweight="bold")
    ax.text(5, 3.6, "Dari Nol sampai Mahir", ha="center",
            color=AMBER, fontsize=18, fontweight="bold")
    ax.text(5, 3.05, "Auto-Reply - FAQ - Greeting - Lead Capture - Testing", ha="center",
            color=WHITE, fontsize=12)

    # chip-chip teknologi
    chips = [("Gemini AI", BLUE), ("WhatsApp", GREEN), ("Fonnte", TEAL),
             ("Flask", PURPLE), ("Python", LIGHTGREEN)]
    cx = 1.1
    for label, col in chips:
        _box(ax, cx, 1.7, 1.6, 0.55, label, col, fs=10, radius=0.25)
        cx += 1.75

    ax.text(5, 0.8, "Panduan Bahasa Indonesia  -  Kode + Gambar + Rincian Biaya (Rupiah)",
            ha="center", color=LIGHT, fontsize=11, style="italic")
    _save(fig, "00_cover.png")


# =====================================================================
# 1. ROADMAP ZERO -> HERO
# =====================================================================
def roadmap():
    levels = [
        ("L0", "Fondasi", "Konsep AI"),
        ("L1", "Akun & Platform", "API key gratis"),
        ("L2", "Lingkungan", "Python siap"),
        ("L3", "Hello AI", "AI menjawab"),
        ("L4", "Auto-Reply", "Balas otomatis"),
        ("L5", "FAQ Flow", "Jawab FAQ"),
        ("L6", "Auto Greeting", "Sapaan pintar"),
        ("L7", "Lead Capture", "Nama & intent"),
        ("L8", "Testing", "Uji & optimasi"),
        ("L9", "Deploy 24/7", "Online terus"),
        ("L10", "HERO", "Multi-channel"),
    ]
    cols = [GREY, BLUE, BLUE, TEAL, GREEN, GREEN, LIGHTGREEN, LIGHTGREEN,
            PURPLE, AMBER, RED]

    fig, ax = plt.subplots(figsize=(11, 5.4))
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.text(5.5, 5.6, "Peta Perjalanan: NOL  ->  HERO", ha="center",
            fontsize=18, fontweight="bold", color=NAVY)

    positions = []
    for i in range(len(levels)):
        row = 0 if i < 6 else 1
        col = i if i < 6 else (10 - i)
        x = 0.4 + col * 1.75
        y = 3.4 if row == 0 else 1.2
        positions.append((x, y))

    for i, ((code, title, sub), (x, y)) in enumerate(zip(levels, positions)):
        _box(ax, x, y, 1.55, 1.2, "", cols[i], radius=0.08)
        ax.text(x + 0.775, y + 0.92, code, ha="center", color=WHITE,
                fontsize=13, fontweight="bold")
        ax.text(x + 0.775, y + 0.55, title, ha="center", color=WHITE,
                fontsize=9.0, fontweight="bold")
        ax.text(x + 0.775, y + 0.22, sub, ha="center", color=LIGHT, fontsize=7.5)

    for i in range(len(levels) - 1):
        x1, y1 = positions[i]
        x2, y2 = positions[i + 1]
        if y1 == y2:
            _arrow(ax, x1 + 1.55, y1 + 0.6, x2, y2 + 0.6, color=GREY)
        else:
            _arrow(ax, x1 + 0.775, y1, x2 + 0.775, y2 + 1.2, color=AMBER, lw=2.2)

    _save(fig, "01_roadmap.png")


# =====================================================================
# 2. ARSITEKTUR SISTEM
# =====================================================================
def arsitektur():
    fig, ax = plt.subplots(figsize=(10.5, 6))
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.text(5.25, 5.7, "Arsitektur Sistem AI WhatsApp Automation", ha="center",
            fontsize=17, fontweight="bold", color=NAVY)

    # Pengguna & WhatsApp (kiri)
    _box(ax, 0.3, 4.0, 2.4, 0.9, "Pelanggan\n(chat WhatsApp)", GREEN, fs=10)
    _box(ax, 0.3, 2.5, 2.4, 0.9, "Gateway WA\nFonnte / Meta API", LIGHTGREEN, fs=9)

    # Inti agent (tengah)
    _box(ax, 3.5, 3.5, 3.4, 1.6, "WEBHOOK (Flask)\napp.py -> bot.py\nrouter autonomous", NAVY, fs=10)
    _box(ax, 3.5, 2.0, 3.4, 1.0, "SQLite (leads.db)\nsesi + data lead", GREY, fs=9)

    # Otak
    _box(ax, 7.8, 3.9, 2.4, 1.1, "Gemini LLM\n(otak: jawab FAQ\n& deteksi intent)", BLUE, fs=9)

    # Modul fitur
    _box(ax, 7.8, 2.2, 2.4, 1.0, "Modul fitur:\ngreeting - faq\nlead capture", TEAL, fs=8.5)

    # panah
    _arrow(ax, 2.7, 4.45, 3.5, 4.4, GREEN)        # pelanggan -> webhook (via gateway)
    _arrow(ax, 2.7, 2.95, 3.5, 3.8, LIGHTGREEN)   # gateway -> webhook
    _arrow(ax, 3.5, 3.6, 2.7, 2.95, LIGHTGREEN)   # webhook -> gateway (balasan)
    _arrow(ax, 5.2, 3.5, 5.2, 3.0, GREY)          # bot <-> db
    _arrow(ax, 5.2, 3.0, 5.2, 3.5, GREY)
    _arrow(ax, 6.9, 4.3, 7.8, 4.4, BLUE)          # bot -> gemini
    _arrow(ax, 7.8, 4.1, 6.9, 4.1, BLUE)          # gemini -> bot
    _arrow(ax, 6.9, 3.7, 7.8, 2.9, TEAL)          # bot -> modul
    _arrow(ax, 2.7, 4.2, 2.7, 3.4, GREEN)         # pelanggan <-> gateway

    _save(fig, "02_arsitektur.png")


# =====================================================================
# 3. SIKLUS AGENT + 4 KOMPONEN
# =====================================================================
def agent_loop():
    fig, ax = plt.subplots(figsize=(10.5, 5.4))
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 5.4)
    ax.axis("off")
    ax.text(2.6, 5.0, "Siklus Kerja Agent", ha="center",
            fontsize=15, fontweight="bold", color=NAVY)
    ax.text(8.0, 5.0, "4 Komponen Inti", ha="center",
            fontsize=15, fontweight="bold", color=NAVY)

    cx, cy, r = 2.6, 2.4, 1.5
    steps = [("1. TERIMA\n(pesan masuk)", TEAL, 90),
             ("2. PIKIR\n(deteksi niat)", BLUE, 0),
             ("3. AKSI\n(balas/simpan)", GREEN, 270),
             ("4. ULANGI\n(tunggu lagi)", AMBER, 180)]
    coords = []
    for label, col, ang in steps:
        a = math.radians(ang)
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        coords.append((x, y))
        c = Circle((x, y), 0.66, facecolor=col, edgecolor="white", lw=1.5, zorder=2)
        ax.add_patch(c)
        ax.text(x, y, label, ha="center", va="center", color=WHITE,
                fontsize=8.0, fontweight="bold", zorder=3)
    order = [0, 1, 2, 3, 0]
    for i in range(4):
        x1, y1 = coords[order[i]]
        x2, y2 = coords[order[i + 1]]
        ax.add_patch(FancyArrowPatch(
            (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=16,
            connectionstyle="arc3,rad=0.3", color=GREY, lw=1.8, zorder=1))

    comps = [("Otak (LLM)", "Gemini - menjawab & menilai niat", BLUE),
             ("Tools/Modul", "greeting, FAQ, lead capture", TEAL),
             ("Memory", "SQLite - sesi & data lead", GREY),
             ("Loop", "Terima - Pikir - Aksi - Ulangi", GREEN)]
    y = 3.8
    for title, sub, col in comps:
        _box(ax, 5.6, y, 4.6, 0.78, "", col, radius=0.06)
        ax.text(5.8, y + 0.5, title, ha="left", color=WHITE, fontsize=10.5,
                fontweight="bold")
        ax.text(5.8, y + 0.2, sub, ha="left", color=LIGHT, fontsize=8.5)
        y -= 0.95

    _save(fig, "03_agent_loop.png")


# =====================================================================
# 4. ALUR PERCAKAPAN (DECISION FLOW)
# =====================================================================
def alur_percakapan():
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6.4)
    ax.axis("off")
    ax.text(5.25, 6.05, "Alur Keputusan Bot untuk Setiap Pesan Masuk",
            ha="center", fontsize=15, fontweight="bold", color=NAVY)

    _box(ax, 4.1, 5.2, 2.3, 0.7, "Pesan masuk", GREEN, fs=10, radius=0.1)

    # baris pertanyaan keputusan
    _box(ax, 0.4, 3.9, 2.3, 0.85, "Sedang isi\ndata lead?", AMBER, tc=NAVY, fs=9, radius=0.06)
    _box(ax, 3.0, 3.9, 2.3, 0.85, "Kontak baru?", BLUE, fs=9, radius=0.06)
    _box(ax, 5.6, 3.9, 2.3, 0.85, "Niat\nmendaftar?", PURPLE, fs=9, radius=0.06)
    _box(ax, 8.0, 3.9, 2.1, 0.85, "Cocok FAQ /\npertanyaan?", TEAL, fs=9, radius=0.06)

    # aksi
    _box(ax, 0.4, 2.2, 2.3, 0.95, "Lanjutkan\nlead capture\n(nama->intent)", GREY, fs=8.5, radius=0.06)
    _box(ax, 3.0, 2.2, 2.3, 0.95, "Kirim SAPAAN\n(auto greeting)\n+ menu", BLUE, fs=8.5, radius=0.06)
    _box(ax, 5.6, 2.2, 2.3, 0.95, "Mulai lead\ncapture: tanya\nnama & intent", PURPLE, fs=8.5, radius=0.06)
    _box(ax, 8.0, 2.2, 2.1, 0.95, "Jawab via AI\n(grounded ke\nFAQ bisnis)", TEAL, fs=8.5, radius=0.06)

    # default
    _box(ax, 3.4, 0.6, 3.7, 0.9, "Lainnya -> jawaban umum AI\n(atau fallback + tawarkan menu)",
         NAVY, fs=9, radius=0.06)

    _arrow(ax, 5.25, 5.2, 5.25, 4.78, GREEN)
    for x in (1.55, 4.15, 6.75, 9.05):
        _arrow(ax, x, 3.9, x, 3.18, GREY)
    _arrow(ax, 5.25, 2.2, 5.25, 1.5, NAVY)

    ax.text(5.25, 4.95, "diperiksa berurutan dari kiri ke kanan",
            ha="center", fontsize=8.5, style="italic", color=GREY)
    _save(fig, "04_alur_percakapan.png")


# =====================================================================
# 5. ALUR LEAD CAPTURE
# =====================================================================
def lead_flow():
    fig, ax = plt.subplots(figsize=(11, 3.2))
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 3.2)
    ax.axis("off")
    ax.text(5.5, 2.95, "Alur Lead Capture: Tangkap Nama & Intent",
            ha="center", fontsize=15, fontweight="bold", color=NAVY)

    stages = [
        ("Pemicu\n(niat daftar)", PURPLE),
        ("Tanya\nNAMA", BLUE),
        ("Tanya\nKEBUTUHAN\n(intent)", TEAL),
        ("Simpan ke\nSQLite", GREEN),
        ("Konfirmasi\n+ notifikasi\ntim", LIGHTGREEN),
    ]
    x = 0.4
    w = 1.85
    centers = []
    for label, col in stages:
        _box(ax, x, 1.0, w, 1.1, label, col, fs=9.0, radius=0.06)
        centers.append(x + w)
        x += w + 0.27
    for i in range(len(stages) - 1):
        _arrow(ax, centers[i], 1.55, centers[i] + 0.27, 1.55, GREY)

    _save(fig, "05_lead_flow.png")


# =====================================================================
# 6. PERBANDINGAN BIAYA
# =====================================================================
def biaya():
    fig, ax = plt.subplots(figsize=(9.5, 5))
    fig.patch.set_facecolor(WHITE)

    skenario = ["Hemat\n(Gratis)", "Normal\n(UMKM)", "Pro\n(Skala besar)"]
    # estimasi biaya bulanan (ribuan rupiah) per komponen
    llm =     [0,   0,    300]
    gateway = [0,   100,  500]
    hosting = [0,   50,   400]

    x = np.arange(len(skenario))
    width = 0.55
    ax.bar(x, llm, width, label="AI (Gemini)", color=BLUE)
    ax.bar(x, gateway, width, bottom=llm, label="Gateway WhatsApp", color=GREEN)
    bottom2 = [llm[i] + gateway[i] for i in range(3)]
    ax.bar(x, hosting, width, bottom=bottom2, label="Hosting 24/7", color=AMBER)

    ax.set_title("Estimasi Biaya Operasional per Bulan (ribu Rupiah)",
                 fontsize=14, fontweight="bold", color=NAVY)
    ax.set_xticks(x)
    ax.set_xticklabels(skenario, fontsize=11)
    ax.set_ylabel("Ribu Rupiah / bulan")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    totals = [llm[i] + gateway[i] + hosting[i] for i in range(3)]
    labels = ["Rp 0", "± Rp 150 rb", "± Rp 1,2 jt"]
    for i, (t, lab) in enumerate(zip(totals, labels)):
        ax.text(i, t + 25, lab, ha="center", fontweight="bold",
                color=NAVY, fontsize=11)

    ax.text(0, 200, "Cukup untuk\nbelajar &\nuji coba", ha="center",
            fontsize=8.5, color=GREEN, fontweight="bold")
    ax.set_ylim(0, max(totals) * 1.25)
    _save(fig, "06_biaya.png")


if __name__ == "__main__":
    cover()
    roadmap()
    arsitektur()
    agent_loop()
    alur_percakapan()
    lead_flow()
    biaya()
    print("\nSemua diagram berhasil dibuat di:", OUT_DIR)
