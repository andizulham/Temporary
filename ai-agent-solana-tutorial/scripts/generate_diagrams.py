"""
generate_diagrams.py
====================
Membuat semua gambar/diagram pembantu untuk tutorial (disimpan di docs/images/).
Jalankan: python scripts/generate_diagrams.py

Memakai matplotlib murni (tanpa dependensi sistem) supaya andal di mana saja.
"""

import os
import matplotlib
matplotlib.use("Agg")  # backend non-interaktif (tanpa layar)
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.lines import Line2D

# ---- Palet warna konsisten ----
NAVY = "#0B1F3A"
BLUE = "#1565C0"
TEAL = "#00897B"
PURPLE = "#6A1B9A"
GREEN = "#2E7D32"
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
    print("✓ ", path)


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

    ax.text(5, 5.1, "BELAJAR AI AGENT", ha="center", color=WHITE,
            fontsize=32, fontweight="bold")
    ax.text(5, 4.35, "DARI NOL SAMPAI MAHIR", ha="center", color=AMBER,
            fontsize=20, fontweight="bold")
    ax.text(5, 3.5, "Proyek Nyata: Pelacak & Evaluator", ha="center",
            color=WHITE, fontsize=15)
    ax.text(5, 3.0, "Trading Crypto di Jaringan Solana", ha="center",
            color=WHITE, fontsize=15)

    # chip-chip teknologi
    chips = [("Gemini AI", BLUE), ("Solana", PURPLE), ("Helius", TEAL),
             ("Telegram", BLUE), ("Python", GREEN)]
    cx = 1.1
    for label, col in chips:
        _box(ax, cx, 1.7, 1.6, 0.55, label, col, fs=10, radius=0.25)
        cx += 1.75

    ax.text(5, 0.8, "Panduan Bahasa Indonesia • Kode + Gambar + Rincian Biaya",
            ha="center", color=LIGHT, fontsize=11, style="italic")
    _save(fig, "00_cover.png")


# =====================================================================
# 1. ROADMAP ZERO -> HERO
# =====================================================================
def roadmap():
    levels = [
        ("L0", "Fondasi", "Konsep AI Agent"),
        ("L1", "Akun & Platform", "API key gratis"),
        ("L2", "Lingkungan", "Python siap"),
        ("L3", "Hello Agent", "AI menjawab"),
        ("L4", "Data Solana", "Harga & dompet"),
        ("L5", "Tracker", "Rekam trade"),
        ("L6", "Evaluator", "AI menilai"),
        ("L7", "Mode Agent", "Tools/function"),
        ("L8", "Telegram Bot", "Kontrol dari HP"),
        ("L9", "Deploy 24/7", "Otomatis"),
        ("L10", "HERO", "Multi-agent/RAG"),
    ]
    colors = [GREY, BLUE, BLUE, TEAL, TEAL, GREEN, GREEN, PURPLE, PURPLE, AMBER, RED]

    fig, ax = plt.subplots(figsize=(11, 5.4))
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.text(5.5, 5.6, "Peta Perjalanan: NOL  →  HERO", ha="center",
            fontsize=18, fontweight="bold", color=NAVY)

    # tata letak zig-zag 2 baris
    positions = []
    for i in range(len(levels)):
        row = 0 if i < 6 else 1
        col = i if i < 6 else (10 - i)
        x = 0.4 + col * 1.75
        y = 3.4 if row == 0 else 1.2
        positions.append((x, y))

    for i, ((code, title, sub), (x, y)) in enumerate(zip(levels, positions)):
        _box(ax, x, y, 1.55, 1.2, "", colors[i], radius=0.08)
        ax.text(x + 0.775, y + 0.92, code, ha="center", color=WHITE,
                fontsize=13, fontweight="bold")
        ax.text(x + 0.775, y + 0.55, title, ha="center", color=WHITE,
                fontsize=9.5, fontweight="bold")
        ax.text(x + 0.775, y + 0.22, sub, ha="center", color=LIGHT, fontsize=7.5)

    # panah antar level
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
    ax.text(5.25, 5.7, "Arsitektur Sistem AI Agent", ha="center",
            fontsize=17, fontweight="bold", color=NAVY)

    # Sumber data (kiri)
    _box(ax, 0.3, 4.2, 2.4, 0.8, "Blockchain Solana", PURPLE, fs=11)
    _box(ax, 0.3, 3.1, 2.4, 0.8, "Helius API\n(riwayat dompet)", TEAL, fs=9)
    _box(ax, 0.3, 2.0, 2.4, 0.8, "DexScreener API\n(harga token)", TEAL, fs=9)

    # Inti agent (tengah)
    _box(ax, 3.6, 3.7, 3.3, 1.5, "AI AGENT (Python)\nsolana_client • tracker\nevaluator", NAVY, fs=10)
    _box(ax, 3.6, 2.3, 3.3, 0.9, "Database SQLite\n(trades.db) — memory", GREY, fs=9)

    # Otak
    _box(ax, 7.8, 3.9, 2.4, 1.0, "Gemini LLM\n(otak/analisa)", BLUE, fs=10)

    # Interface
    _box(ax, 7.8, 2.3, 2.4, 0.9, "Telegram Bot\n(antarmuka)", BLUE, fs=9)
    _box(ax, 3.6, 0.9, 3.3, 0.9, "Pengguna (kamu)\nchat dari HP/laptop", GREEN, fs=9)

    # panah
    _arrow(ax, 2.7, 4.6, 3.6, 4.6, PURPLE)
    _arrow(ax, 2.7, 3.5, 3.6, 4.2, TEAL)
    _arrow(ax, 2.7, 2.4, 3.6, 4.0, TEAL)
    _arrow(ax, 5.25, 3.7, 5.25, 3.2, GREY)          # agent <-> db
    _arrow(ax, 5.25, 3.2, 5.25, 3.7, GREY)
    _arrow(ax, 6.9, 4.4, 7.8, 4.4, BLUE)            # agent -> gemini
    _arrow(ax, 7.8, 4.2, 6.9, 4.2, BLUE)            # gemini -> agent
    _arrow(ax, 7.8, 2.7, 6.9, 3.7, BLUE)            # telegram -> agent
    _arrow(ax, 6.9, 3.6, 7.8, 2.75, BLUE)           # agent -> telegram
    _arrow(ax, 5.25, 1.8, 5.25, 2.3, GREEN)         # user -> agent
    _arrow(ax, 7.9, 2.3, 5.6, 1.4, GREEN)           # telegram -> user

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
    ax.text(2.6, 5.0, "Siklus Kerja AI Agent", ha="center",
            fontsize=15, fontweight="bold", color=NAVY)
    ax.text(8.0, 5.0, "4 Komponen Inti", ha="center",
            fontsize=15, fontweight="bold", color=NAVY)

    # Loop melingkar (kiri)
    cx, cy, r = 2.6, 2.4, 1.5
    steps = [("1. PERCEIVE\n(lihat data)", TEAL, 90),
             ("2. THINK\n(analisa)", BLUE, 0),
             ("3. ACT\n(bertindak)", GREEN, 270),
             ("4. REPEAT\n(ulangi)", AMBER, 180)]
    import math
    coords = []
    for label, col, ang in steps:
        a = math.radians(ang)
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        coords.append((x, y))
        c = Circle((x, y), 0.62, facecolor=col, edgecolor="white", lw=1.5, zorder=2)
        ax.add_patch(c)
        ax.text(x, y, label, ha="center", va="center", color=WHITE,
                fontsize=8.2, fontweight="bold", zorder=3)
    # panah melingkar
    order = [0, 1, 2, 3, 0]
    for i in range(4):
        x1, y1 = coords[order[i]]
        x2, y2 = coords[order[i + 1]]
        ax.add_patch(FancyArrowPatch(
            (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=16,
            connectionstyle="arc3,rad=0.3", color=GREY, lw=1.8, zorder=1))

    # 4 komponen (kanan)
    comps = [("Otak (LLM)", "Gemini - berpikir & memutuskan", BLUE),
             ("Tools (Alat)", "Fungsi: ambil harga, baca dompet", TEAL),
             ("Memory", "SQLite - menyimpan riwayat", GREY),
             ("Loop (Siklus)", "Perceive - Think - Act", GREEN)]
    y = 3.8
    for title, sub, col in comps:
        _box(ax, 5.6, y, 4.6, 0.78, "", col, radius=0.06)
        ax.text(5.8, y + 0.5, title, ha="left", color=WHITE, fontsize=10.5,
                fontweight="bold")
        ax.text(5.8, y + 0.2, sub, ha="left", color=LIGHT, fontsize=8.5)
        y -= 0.95

    _save(fig, "03_agent_loop.png")


# =====================================================================
# 4. ALUR DATA (DATA FLOW)
# =====================================================================
def data_flow():
    fig, ax = plt.subplots(figsize=(11, 3.2))
    fig.patch.set_facecolor(WHITE)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 3.2)
    ax.axis("off")
    ax.text(5.5, 2.95, "Alur Data: dari Dompet sampai Saran AI", ha="center",
            fontsize=15, fontweight="bold", color=NAVY)

    stages = [
        ("Dompet\nSolana", PURPLE),
        ("Helius\n(tarik tx)", TEAL),
        ("parse_swaps\n(saring swap)", GREY),
        ("SQLite\n(simpan)", BLUE),
        ("Gemini\n(evaluasi)", BLUE),
        ("Telegram\n(laporan)", GREEN),
    ]
    x = 0.3
    w = 1.6
    centers = []
    for label, col in stages:
        _box(ax, x, 1.1, w, 1.0, label, col, fs=9.5, radius=0.06)
        centers.append(x + w)
        x += w + 0.28
    for i in range(len(stages) - 1):
        _arrow(ax, centers[i], 1.6, centers[i] + 0.28, 1.6, GREY)

    _save(fig, "04_data_flow.png")


# =====================================================================
# 5. PERBANDINGAN BIAYA
# =====================================================================
def biaya():
    fig, ax = plt.subplots(figsize=(9.5, 5))
    fig.patch.set_facecolor(WHITE)

    skenario = ["Hemat\n(Gratis)", "Serius\n(VPS)", "Pro\n(Skala besar)"]
    # estimasi biaya bulanan (ribuan rupiah) per komponen
    llm =     [0,   40,   325]
    data_ =   [0,   0,    8000]
    hosting = [0,   80,   400]

    import numpy as np
    x = np.arange(len(skenario))
    width = 0.55
    p1 = ax.bar(x, llm, width, label="LLM (Gemini)", color=BLUE)
    p2 = ax.bar(x, data_, width, bottom=llm, label="Data on-chain (Helius)", color=TEAL)
    bottom2 = [llm[i] + data_[i] for i in range(3)]
    p3 = ax.bar(x, hosting, width, bottom=bottom2, label="Hosting 24/7", color=AMBER)

    ax.set_title("Estimasi Biaya Operasional per Bulan (ribu Rupiah)",
                 fontsize=14, fontweight="bold", color=NAVY)
    ax.set_xticks(x)
    ax.set_xticklabels(skenario, fontsize=11)
    ax.set_ylabel("Ribu Rupiah / bulan")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    totals = [llm[i] + data_[i] + hosting[i] for i in range(3)]
    labels = ["Rp 0", "± Rp 120 rb", "± Rp 8,7 jt"]
    for i, (t, lab) in enumerate(zip(totals, labels)):
        ax.text(i, t + 200, lab, ha="center", fontweight="bold",
                color=NAVY, fontsize=11)

    ax.text(0, 1500, "Cukup untuk\nbelajar &\npakai pribadi", ha="center",
            fontsize=8.5, color=GREEN, fontweight="bold")
    ax.set_ylim(0, max(totals) * 1.18)
    _save(fig, "05_biaya.png")


if __name__ == "__main__":
    cover()
    roadmap()
    arsitektur()
    agent_loop()
    data_flow()
    biaya()
    print("\nSemua diagram berhasil dibuat di:", OUT_DIR)
