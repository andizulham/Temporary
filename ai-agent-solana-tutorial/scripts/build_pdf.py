"""
build_pdf.py
============
Membangun PDF tutorial (Bahasa Indonesia) lengkap dengan gambar/diagram,
tabel, kotak info, dan blok kode. Memakai reportlab (murni Python, andal).

Jalankan:
    python scripts/generate_diagrams.py   # buat gambar dulu
    python scripts/build_pdf.py           # lalu buat PDF

Hasil: docs/Tutorial-AI-Agent-Solana-Trading.pdf
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image,
    Table, TableStyle, PageBreak, KeepTogether, HRFlowable, ListFlowable,
    ListItem,
)
from reportlab.platypus.doctemplate import NextPageTemplate
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
IMG = os.path.join(ROOT, "docs", "images")
OUT = os.path.join(ROOT, "docs", "Tutorial-AI-Agent-Solana-Trading.pdf")

# ---- Palet warna ----
NAVY = colors.HexColor("#0B1F3A")
BLUE = colors.HexColor("#1565C0")
TEAL = colors.HexColor("#00897B")
GREEN = colors.HexColor("#2E7D32")
AMBER = colors.HexColor("#F9A825")
RED = colors.HexColor("#C62828")
GREY = colors.HexColor("#455A64")
LIGHTBG = colors.HexColor("#ECEFF1")
CODEBG = colors.HexColor("#1E2733")
CODEFG = colors.HexColor("#E0E6ED")

PAGE_W, PAGE_H = A4

# =========================================================================
#  STYLES
# =========================================================================
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

st_title = S("t", fontName="Helvetica-Bold", fontSize=30, leading=35,
             textColor=colors.white, alignment=TA_CENTER)
st_sub = S("s", fontName="Helvetica-Bold", fontSize=15, leading=20,
           textColor=AMBER, alignment=TA_CENTER)
st_subw = S("sw", fontName="Helvetica", fontSize=12, leading=18,
            textColor=colors.white, alignment=TA_CENTER)
st_h1 = S("h1", fontName="Helvetica-Bold", fontSize=18, leading=22,
          textColor=NAVY, spaceBefore=16, spaceAfter=8)
st_h2 = S("h2", fontName="Helvetica-Bold", fontSize=13.5, leading=18,
          textColor=BLUE, spaceBefore=12, spaceAfter=5)
st_h3 = S("h3", fontName="Helvetica-Bold", fontSize=11.5, leading=15,
          textColor=TEAL, spaceBefore=8, spaceAfter=3)
st_body = S("b", fontName="Helvetica", fontSize=10, leading=15,
            textColor=colors.HexColor("#222222"), alignment=TA_JUSTIFY,
            spaceAfter=5)
st_bullet = S("bl", fontName="Helvetica", fontSize=10, leading=14.5,
              textColor=colors.HexColor("#222222"), leftIndent=6)
st_small = S("sm", fontName="Helvetica", fontSize=8.5, leading=12,
             textColor=GREY, alignment=TA_CENTER, spaceBefore=3)
st_code = S("c", fontName="Courier", fontSize=8.3, leading=11.5,
            textColor=CODEFG)
st_caption = S("cap", fontName="Helvetica-Oblique", fontSize=8.5, leading=11,
               textColor=GREY, alignment=TA_CENTER, spaceBefore=3, spaceAfter=8)
st_th = S("th", fontName="Helvetica-Bold", fontSize=9, leading=12,
          textColor=colors.white)
st_td = S("td", fontName="Helvetica", fontSize=8.8, leading=11.5,
          textColor=colors.HexColor("#222222"))
st_tdb = S("tdb", fontName="Helvetica-Bold", fontSize=8.8, leading=11.5,
           textColor=NAVY)


# =========================================================================
#  HELPER FLOWABLES
# =========================================================================
def img(path, width_cm):
    """Gambar dengan menjaga rasio aspek."""
    from PIL import Image as PILImage
    full = os.path.join(IMG, path)
    iw, ih = PILImage.open(full).size
    w = width_cm * cm
    h = w * ih / iw
    return Image(full, width=w, height=h)


def code_block(text):
    """Blok kode dengan latar gelap."""
    lines = text.strip("\n").split("\n")
    safe = []
    for ln in lines:
        ln = ln.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        ln = ln.replace(" ", "&nbsp;") or "&nbsp;"
        safe.append(Paragraph(ln, st_code))
    tbl = Table([[safe]], colWidths=[16.6 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODEBG),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
    ]))
    return tbl


def callout(text, color=BLUE, bg=LIGHTBG):
    """Kotak info berwarna dengan garis kiri."""
    p = Paragraph(text, S("co", fontName="Helvetica", fontSize=9.3, leading=13.5,
                          textColor=colors.HexColor("#222222")))
    tbl = Table([[p]], colWidths=[16.4 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 4, color),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return tbl


def make_table(headers, rows, col_widths, header_bg=NAVY, font=8.8):
    data = [[Paragraph(h, st_th) for h in headers]]
    for r in rows:
        row = []
        for i, cell in enumerate(r):
            stl = st_tdb if i == 0 else st_td
            row.append(Paragraph(str(cell), stl))
        data.append(row)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CFD8DC")),
        ("LINEBELOW", (0, 0), (-1, 0), 1.2, header_bg),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#F7F9FA")))
    t.setStyle(TableStyle(style))
    return t


def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(it, st_bullet), leftIndent=10, value="•")
         for it in items],
        bulletType="bullet", start="•", leftIndent=12,
    )


def h1(num, text):
    return [HRFlowable(width="100%", thickness=1.4, color=NAVY,
                       spaceBefore=6, spaceAfter=4),
            Paragraph(f"{num}. {text}", st_h1)]


# =========================================================================
#  PAGE DECOR (cover & footer)
# =========================================================================
def on_cover(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas_obj.setFillColor(AMBER)
    canvas_obj.rect(0, 0, PAGE_W, 1.2 * cm, fill=1, stroke=0)
    canvas_obj.rect(0, PAGE_H - 1.2 * cm, PAGE_W, 1.2 * cm, fill=1, stroke=0)
    canvas_obj.restoreState()


def on_page(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setStrokeColor(colors.HexColor("#CFD8DC"))
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(2 * cm, 1.5 * cm, PAGE_W - 2 * cm, 1.5 * cm)
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(GREY)
    canvas_obj.drawString(2 * cm, 1.0 * cm,
                          "Belajar AI Agent dari Nol sampai Mahir - Proyek Solana Trading")
    canvas_obj.drawRightString(PAGE_W - 2 * cm, 1.0 * cm, f"Halaman {doc.page}")
    canvas_obj.restoreState()


# =========================================================================
#  BUILD CONTENT
# =========================================================================
def build():
    doc = BaseDocTemplate(
        OUT, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title="Belajar AI Agent dari Nol sampai Mahir - Proyek Solana Trading",
        author="Tutorial AI Agent",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height, id="main")
    cover_frame = Frame(0, 0, PAGE_W, PAGE_H, id="cover",
                        leftPadding=2 * cm, rightPadding=2 * cm,
                        topPadding=3 * cm, bottomPadding=3 * cm)
    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[cover_frame], onPage=on_cover),
        PageTemplate(id="Body", frames=[frame], onPage=on_page),
    ])

    e = []  # daftar elemen (flowables)

    # Halaman pertama (cover) pakai template "Cover", sisanya pakai "Body"
    e.append(NextPageTemplate("Body"))

    # ---------- COVER ----------
    e.append(Spacer(1, 0.5 * cm))
    e.append(img("00_cover.png", 15.5))
    e.append(Spacer(1, 0.8 * cm))
    e.append(Paragraph("Panduan Lengkap Berbahasa Indonesia", st_subw))
    e.append(Paragraph("Kode + Diagram + Rincian Biaya (Rupiah)", st_subw))
    e.append(Spacer(1, 0.6 * cm))
    e.append(Paragraph(
        "Proyek nyata: AI Agent yang melacak (tracking) dan mengevaluasi "
        "transaksi trading crypto di jaringan Solana.", st_subw))
    e.append(PageBreak())

    # ---------- BAB 1: Pendahuluan ----------
    e += h1(1, "Pendahuluan")
    e.append(Paragraph(
        "Dokumen ini mengajarkan <b>AI Agent dari nol sampai mahir</b> melalui "
        "proyek nyata yang berguna untuk trading crypto di chain Solana. Semua "
        "platform yang dipakai bisa diakses dari Indonesia dan punya paket gratis. "
        "Bahasa pemrograman utama adalah <b>Python</b> karena paling ramah pemula.",
        st_body))
    e.append(callout(
        "<b>Disclaimer:</b> Tutorial ini untuk edukasi teknologi (AI + pemrograman), "
        "BUKAN nasihat keuangan. Trading crypto sangat berisiko. AI Agent membantu "
        "mencatat &amp; menganalisa keputusanmu, bukan menjamin profit. Selalu DYOR "
        "(Do Your Own Research) dan JANGAN pernah membagikan private key / seed phrase.",
        color=RED, bg=colors.HexColor("#FDECEA")))
    e.append(Spacer(1, 0.2 * cm))
    e.append(Paragraph("Apa itu AI Agent?", st_h2))
    e.append(Paragraph(
        "AI Agent adalah program yang memakai model bahasa (LLM seperti Gemini) "
        "sebagai \"otak\" untuk mengambil keputusan dan <b>bertindak</b> memakai "
        "<i>tools</i> (alat), bukan sekadar menjawab teks seperti chatbot biasa.",
        st_body))
    e.append(make_table(
        ["Chatbot biasa", "AI Agent"],
        [["Hanya membalas teks", "Bisa bertindak: panggil API, baca database, kirim notifikasi"],
         ["Tidak ingat konteks", "Punya memory (ingatan)"],
         ["Satu langkah", "Multi-langkah: rencana - aksi - cek - ulangi"],
         ["Tanpa alat", "Punya tools (fungsi yang bisa dipanggil)"]],
        [5.5 * cm, 11.1 * cm]))

    # ---------- BAB 2: Roadmap ----------
    e.append(Spacer(1, 0.3 * cm))
    e += h1(2, "Peta Perjalanan (Roadmap Zero - Hero)")
    e.append(img("01_roadmap.png", 16.5))
    e.append(Paragraph("Gambar 1. Sepuluh level dari Nol sampai Hero.", st_caption))
    e.append(make_table(
        ["Level", "Nama", "Hasil yang didapat"],
        [["L0", "Fondasi", "Paham konsep AI Agent, LLM, tools, memory"],
         ["L1", "Akun &amp; Platform", "Punya semua API key gratis"],
         ["L2", "Lingkungan", "Python siap, project bisa jalan"],
         ["L3", "Hello Agent", "AI menjawab pertanyaan pertama"],
         ["L4", "Data Solana", "Ambil harga token &amp; riwayat dompet"],
         ["L5", "Tracker", "Otomatis mencatat trade ke database"],
         ["L6", "Evaluator", "AI memberi skor &amp; saran"],
         ["L7", "Mode Agent", "AI memanggil tools sendiri (function calling)"],
         ["L8", "Telegram Bot", "Kontrol agent dari HP via chat"],
         ["L9", "Deploy 24/7", "Agent jalan sendiri tanpa laptop"],
         ["L10", "Hero", "Multi-agent, RAG, backtest, no-code"]],
        [1.7 * cm, 4.0 * cm, 10.9 * cm]))

    # ---------- BAB 3: Platform Indonesia ----------
    e.append(PageBreak())
    e += h1(3, "Platform yang Bisa Diakses dari Indonesia")
    e.append(Paragraph("A. Platform \"Otak\" AI (LLM)", st_h2))
    e.append(make_table(
        ["Platform", "Paket gratis", "Catatan"],
        [["Google AI Studio (Gemini)", "Sangat murah hati", "Rekomendasi utama, cukup akun Google"],
         ["OpenAI (ChatGPT API)", "Perlu top-up (mulai $5)", "Butuh kartu internasional"],
         ["Anthropic (Claude)", "Kredit awal terbatas", "Bagus untuk teks panjang"],
         ["Groq", "Gratis, sangat cepat", "Alternatif gratis selain Gemini"]],
        [5.0 * cm, 5.3 * cm, 6.3 * cm]))
    e.append(callout(
        "<b>Kita pakai Gemini.</b> Per awal 2026 paket gratis berpusat pada model 2.5. "
        "Contoh batas: Gemini 2.5 Flash sekitar 10 permintaan/menit &amp; 250/hari; "
        "Flash-Lite sekitar 15/menit &amp; 1.000/hari. Batas bisa berubah - cek dokumentasi "
        "resmi. <i>Informasi dirangkum ulang untuk kepatuhan lisensi.</i>", color=BLUE))
    e.append(Spacer(1, 0.2 * cm))
    e.append(Paragraph("B. Platform Data Solana", st_h2))
    e.append(make_table(
        ["Platform", "Fungsi", "Paket gratis", "API key?"],
        [["DexScreener", "Harga token DEX", "~300 req/menit", "Tidak"],
         ["Helius", "Riwayat tx dompet", "1jt kredit/bln, ~100rb DAS/bln", "Perlu (gratis)"],
         ["Jupiter API", "Agregator harga", "Gratis", "Tidak"],
         ["Solana RPC publik", "Baca chain mentah", "Gratis (terbatas)", "Tidak"]],
        [3.7 * cm, 4.3 * cm, 5.6 * cm, 3.0 * cm]))
    e.append(Spacer(1, 0.15 * cm))
    e.append(Paragraph("C. Dompet &amp; Bursa Solana (legal, terdaftar Bappebti)", st_h2))
    e.append(bullets([
        "<b>Dompet Solana:</b> Phantom, Solflare (gratis, non-custodial).",
        "<b>Beli SOL di Indonesia:</b> Indodax, Tokocrypto, Pintu, Reku.",
        "<b>DEX di Solana:</b> Jupiter, Raydium (untuk swap token).",
    ]))
    e.append(callout(
        "<b>Tidak wajib punya modal.</b> Untuk belajar, kamu bisa memantau alamat "
        "dompet publik mana pun (alamat saja, bukan private key).", color=GREEN,
        bg=colors.HexColor("#E8F5E9")))

    # ---------- BAB 4: Arsitektur ----------
    e.append(PageBreak())
    e += h1(4, "Arsitektur Sistem & Cara Kerja Agent")
    e.append(img("02_arsitektur.png", 16.0))
    e.append(Paragraph("Gambar 2. Arsitektur sistem AI Agent Solana.", st_caption))
    e.append(Paragraph(
        "Sistem mengambil data dari Solana (via Helius &amp; DexScreener), "
        "menyimpannya ke database SQLite, lalu Gemini menganalisanya. Pengguna "
        "berinteraksi lewat bot Telegram.", st_body))
    e.append(Spacer(1, 0.2 * cm))
    e.append(img("03_agent_loop.png", 16.0))
    e.append(Paragraph(
        "Gambar 3. Siklus kerja agent (Perceive - Think - Act - Repeat) dan 4 komponen inti.",
        st_caption))
    e.append(Paragraph(
        "Empat komponen inti AI Agent: <b>Otak (LLM)</b> untuk berpikir, "
        "<b>Tools</b> untuk bertindak, <b>Memory</b> untuk mengingat, dan "
        "<b>Loop</b> sebagai siklus kerja berulang.", st_body))

    # ---------- BAB 5: Langkah membangun (ringkas) ----------
    e.append(PageBreak())
    e += h1(5, "Langkah Demi Langkah Membangun Proyek")

    e.append(Paragraph("Level 2 - Siapkan lingkungan", st_h3))
    e.append(code_block(
        "git clone https://github.com/andizulham/Temporary.git\n"
        "cd Temporary/ai-agent-solana-tutorial\n"
        "python -m venv venv && source venv/bin/activate\n"
        "pip install -r requirements.txt\n"
        "cp .env.example .env     # lalu isi semua API key kamu"))

    e.append(Paragraph("Level 3 - Hello Agent (uji otak AI)", st_h3))
    e.append(code_block(
        "import google.generativeai as genai\n"
        "from config import settings\n"
        "genai.configure(api_key=settings.GEMINI_API_KEY)\n"
        "model = genai.GenerativeModel(settings.GEMINI_MODEL)\n"
        "print(model.generate_content('Apa itu slippage saat swap?').text)"))

    e.append(Paragraph("Level 4-5 - Ambil data Solana & rekam trade", st_h3))
    e.append(code_block(
        "python src/solana_client.py     # tes harga token\n"
        "python src/main.py sync         # tarik & simpan transaksi dompet\n"
        "python src/main.py ringkasan    # lihat statistik trade"))
    e.append(img("04_data_flow.png", 16.2))
    e.append(Paragraph(
        "Gambar 4. Alur data: dompet - Helius - parse - SQLite - Gemini - Telegram.",
        st_caption))

    e.append(Paragraph("Level 6-7 - Evaluasi AI & mode agent", st_h3))
    e.append(code_block(
        "python src/main.py evaluasi                       # AI menilai trading\n"
        "python src/main.py tanya \"Apakah saya overtrading?\"  # mode agent"))
    e.append(callout(
        "<b>Inti AI Agent (Level 7):</b> di mode ini, Gemini sendiri yang memutuskan "
        "kapan memanggil fungsi get_token_price() untuk mengambil harga terbaru "
        "(function calling), lalu menjawab berdasarkan data nyata.", color=TEAL))

    e.append(Paragraph("Level 8 - Antarmuka Telegram", st_h3))
    e.append(code_block("python src/telegram_bot.py    # lalu buka bot di Telegram, ketik /start"))
    e.append(make_table(
        ["Perintah", "Fungsi"],
        [["/sync", "Tarik transaksi terbaru dompet"],
         ["/ringkasan", "Tampilkan statistik trade"],
         ["/evaluasi", "AI menilai trading kamu"],
         ["(teks bebas)", "Tanya apa saja - mode agent"]],
        [4.5 * cm, 12.1 * cm]))

    # ---------- BAB 6: Rincian Biaya ----------
    e.append(PageBreak())
    e += h1(6, "Rincian Biaya Lengkap (Rupiah)")
    e.append(callout(
        "Asumsi kurs: 1 USD sekitar Rp 16.300 (estimasi 2026 - sesuaikan dengan kurs "
        "saat kamu membaca). Angka di bawah adalah estimasi dan dapat berubah.",
        color=AMBER, bg=colors.HexColor("#FFF8E1")))
    e.append(Paragraph("A. Biaya Belajar (Skenario Pelajar Hemat)", st_h2))
    e.append(make_table(
        ["Komponen", "Pilihan gratis", "Biaya"],
        [["Materi belajar", "Tutorial ini + dokumentasi resmi", "Rp 0"],
         ["LLM (otak AI)", "Gemini free tier", "Rp 0"],
         ["Data Solana", "DexScreener + Helius free", "Rp 0"],
         ["Antarmuka", "Telegram Bot", "Rp 0"],
         ["Tempat ngoding", "Google Colab / VS Code", "Rp 0"],
         ["Hosting belajar", "Laptop sendiri", "Rp 0"],
         ["TOTAL BELAJAR", "", "Rp 0"]],
        [4.6 * cm, 8.0 * cm, 4.0 * cm], header_bg=GREEN))
    e.append(callout(
        "<b>Kamu benar-benar bisa belajar dari nol sampai Level 8 tanpa "
        "mengeluarkan uang sama sekali (Rp 0).</b>", color=GREEN,
        bg=colors.HexColor("#E8F5E9")))
    e.append(Spacer(1, 0.2 * cm))
    e.append(Paragraph("B. Biaya Operasional Bulanan (3 Skenario)", st_h2))
    e.append(img("05_biaya.png", 14.5))
    e.append(Paragraph("Gambar 5. Perbandingan estimasi biaya bulanan.", st_caption))
    e.append(make_table(
        ["Komponen", "Hemat (Gratis)", "Serius", "Pro"],
        [["LLM (Gemini)", "Rp 0", "Rp 0-80rb", "Rp 150-500rb"],
         ["Data on-chain (Helius)", "Rp 0", "~Rp 800rb", "~Rp 8jt"],
         ["Data harga (DexScreener)", "Rp 0", "Rp 0", "opsional"],
         ["Hosting 24/7", "Rp 0 (laptop)", "~Rp 80rb (VPS)", "Rp 150-500rb"],
         ["Notifikasi (Telegram)", "Rp 0", "Rp 0", "Rp 0"],
         ["TOTAL / BULAN", "Rp 0", "~Rp 80-900rb", "~Rp 8jt+"]],
        [4.8 * cm, 3.9 * cm, 3.9 * cm, 4.0 * cm], header_bg=NAVY))
    e.append(callout(
        "Untuk pemakaian pribadi, skenario <b>Hemat (Rp 0)</b> atau <b>Serius "
        "(sekitar Rp 80rb/bulan untuk VPS saja, sisanya gratis)</b> sudah lebih dari "
        "cukup. Paket Pro hanya perlu bila memantau banyak dompet / volume sangat tinggi.",
        color=BLUE))

    # ---------- BAB 7: Keamanan & rencana ----------
    e.append(PageBreak())
    e += h1(7, "Keamanan, Etika & Rencana Belajar")
    e.append(Paragraph("Aturan keamanan penting", st_h2))
    e.append(make_table(
        ["Aturan", "Penjelasan"],
        [["Jangan share private key", "Cukup pakai alamat publik untuk memantau"],
         ["Simpan API key di .env", "Jangan hard-code, jangan commit ke GitHub"],
         ["Patuhi aturan Bappebti", "Gunakan bursa terdaftar (Indodax, Pintu, dll)"],
         ["Catat untuk pajak", "Transaksi crypto di Indonesia dikenakan pajak"],
         ["AI = alat bantu", "Output bisa salah, selalu verifikasi &amp; DYOR"]],
        [5.0 * cm, 11.6 * cm], header_bg=RED))
    e.append(Spacer(1, 0.2 * cm))
    e.append(Paragraph("Rencana belajar 4 minggu", st_h2))
    e.append(make_table(
        ["Minggu", "Fokus", "Target"],
        [["Minggu 1", "Level 0-2", "Paham konsep, akun &amp; lingkungan siap"],
         ["Minggu 2", "Level 3-5", "Hello Agent, data masuk, tracker menyimpan"],
         ["Minggu 3", "Level 6-8", "Evaluator + mode agent + bot Telegram aktif"],
         ["Minggu 4", "Level 9-10", "Deploy 24/7 + 1 fitur Hero (notifikasi/RAG)"]],
        [2.7 * cm, 3.0 * cm, 10.9 * cm], header_bg=TEAL))
    e.append(Spacer(1, 0.2 * cm))
    e.append(Paragraph("Naik kelas jadi Hero (Level 10)", st_h2))
    e.append(bullets([
        "<b>No-code/low-code:</b> n8n, Dify, Flowise, Langflow (gratis/self-host).",
        "<b>RAG:</b> beri agent catatan strategimu agar saran sesuai gayamu.",
        "<b>Multi-agent:</b> pisahkan peran (pelacak, analis risiko, pelapor).",
        "<b>Backtesting:</b> uji strategi dengan data historis.",
        "<b>Notifikasi pintar:</b> alert transaksi besar / deteksi rug pull.",
    ]))

    e.append(Spacer(1, 0.4 * cm))
    e.append(HRFlowable(width="100%", thickness=1.2, color=NAVY))
    e.append(Spacer(1, 0.2 * cm))
    e.append(Paragraph(
        "Selamat! Dari NOL, kamu kini punya peta lengkap menjadi HERO AI Agent. "
        "Kerjakan satu per satu dan rayakan tiap \"Lulus Level\". Kode lengkap "
        "ada di folder src/, materi lengkap di TUTORIAL.md.",
        S("end", fontName="Helvetica-Bold", fontSize=10.5, leading=15,
          textColor=NAVY, alignment=TA_CENTER)))
    e.append(Paragraph(
        "AI Agent ini teman analisamu, keputusan tetap di tanganmu. DYOR &amp; "
        "trading dengan bijak.", st_caption))

    doc.build(e)
    print("PDF berhasil dibuat:", OUT)
    print("Ukuran:", round(os.path.getsize(OUT) / 1024, 1), "KB")


if __name__ == "__main__":
    build()
