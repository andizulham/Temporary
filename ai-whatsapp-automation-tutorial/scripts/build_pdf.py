"""
build_pdf.py
============
Membangun PDF tutorial (Bahasa Indonesia) lengkap dengan gambar/diagram,
tabel, kotak info, dan blok kode. Memakai reportlab (murni Python, andal).

Jalankan:
    python scripts/generate_diagrams.py   # buat gambar dulu
    python scripts/build_pdf.py           # lalu buat PDF

Hasil: docs/Tutorial-WhatsApp-AI-Automation.pdf
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image,
    Table, TableStyle, PageBreak, HRFlowable, ListFlowable, ListItem,
)
from reportlab.platypus.doctemplate import NextPageTemplate

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
IMG = os.path.join(ROOT, "docs", "images")
OUT = os.path.join(ROOT, "docs", "Tutorial-WhatsApp-AI-Automation.pdf")

# ---- Palet warna (tema WhatsApp hijau + biru) ----
NAVY = colors.HexColor("#0B2A3A")
GREEN = colors.HexColor("#128C7E")
LIGHTGREEN = colors.HexColor("#1EA362")
BLUE = colors.HexColor("#1565C0")
TEAL = colors.HexColor("#00897B")
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


st_subw = S("sw", fontName="Helvetica", fontSize=12, leading=18,
            textColor=colors.white, alignment=TA_CENTER)
st_h1 = S("h1", fontName="Helvetica-Bold", fontSize=18, leading=22,
          textColor=NAVY, spaceBefore=16, spaceAfter=8)
st_h2 = S("h2", fontName="Helvetica-Bold", fontSize=13.5, leading=18,
          textColor=BLUE, spaceBefore=12, spaceAfter=5)
st_h3 = S("h3", fontName="Helvetica-Bold", fontSize=11.5, leading=15,
          textColor=GREEN, spaceBefore=8, spaceAfter=3)
st_body = S("b", fontName="Helvetica", fontSize=10, leading=15,
            textColor=colors.HexColor("#222222"), alignment=TA_JUSTIFY,
            spaceAfter=5)
st_bullet = S("bl", fontName="Helvetica", fontSize=10, leading=14.5,
              textColor=colors.HexColor("#222222"), leftIndent=6)
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


def make_table(headers, rows, col_widths, header_bg=NAVY):
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
    canvas_obj.setFillColor(LIGHTGREEN)
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
                          "Belajar AI Autonomous WhatsApp dari Nol sampai Mahir")
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
        title="Belajar AI Autonomous WhatsApp dari Nol sampai Mahir",
        author="Tutorial AI Autonomous WhatsApp",
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
    e.append(NextPageTemplate("Body"))

    # ---------- COVER ----------
    e.append(Spacer(1, 0.5 * cm))
    e.append(img("00_cover.png", 15.5))
    e.append(Spacer(1, 0.8 * cm))
    e.append(Paragraph("Panduan Lengkap Berbahasa Indonesia", st_subw))
    e.append(Paragraph("Kode + Diagram + Rincian Biaya (Rupiah)", st_subw))
    e.append(Spacer(1, 0.6 * cm))
    e.append(Paragraph(
        "Proyek nyata: bot WhatsApp otomatis yang membalas pesan, menjawab FAQ, "
        "menyapa pelanggan, dan menangkap data calon pembeli (lead).", st_subw))
    e.append(PageBreak())

    # ---------- BAB 1: Pendahuluan ----------
    e += h1(1, "Pendahuluan")
    e.append(Paragraph(
        "Dokumen ini mengajarkan <b>AI Autonomous untuk WhatsApp dari nol sampai "
        "mahir</b> melalui lima proyek nyata yang berguna untuk bisnis/UMKM. Semua "
        "platform bisa diakses dan legal dari Indonesia serta punya paket gratis. "
        "Bahasa pemrograman utama adalah <b>Python</b> karena paling ramah pemula.",
        st_body))
    e.append(callout(
        "<b>Catatan:</b> Tutorial ini untuk edukasi teknologi (AI + otomatisasi bisnis). "
        "Patuhi Kebijakan WhatsApp Business: JANGAN spam, kirim hanya ke kontak yang "
        "setuju (opt-in), dan lindungi data pribadi pelanggan sesuai UU PDP. "
        "Penyalahgunaan dapat menyebabkan nomor diblokir.",
        color=RED, bg=colors.HexColor("#FDECEA")))
    e.append(Spacer(1, 0.2 * cm))
    e.append(Paragraph("Lima proyek yang akan kamu bangun", st_h2))
    e.append(make_table(
        ["#", "Proyek", "Level", "Fungsi"],
        [["1", "WhatsApp Auto-Reply", "L4", "Balas tiap pesan masuk otomatis, 24 jam"],
         ["2", "FAQ Automation Flow", "L5", "Jawab pertanyaan umum (harga, lokasi, jam)"],
         ["3", "Auto Greeting", "L6", "Sapaan: baru / kembali / di luar jam"],
         ["4", "Lead Capture", "L7", "Tangkap nama &amp; intent calon pembeli"],
         ["5", "Testing &amp; Optimasi", "L8", "Uji otomatis (pytest) + penyempurnaan"]],
        [1.0 * cm, 4.6 * cm, 1.6 * cm, 9.4 * cm]))
    e.append(Spacer(1, 0.2 * cm))
    e.append(Paragraph("Apa itu AI Autonomous?", st_h2))
    e.append(Paragraph(
        "AI Autonomous adalah program yang memakai model bahasa (LLM seperti Gemini) "
        "sebagai \"otak\" untuk memahami pesan, mengambil keputusan, dan bertindak "
        "sendiri (membalas, menyapa, menyimpan data) tanpa harus ditunggu manusia.",
        st_body))
    e.append(make_table(
        ["Chatbot tombol biasa", "AI Autonomous"],
        [["Mengikuti menu kaku (balas angka)", "Memahami bahasa natural (mis. 'brp hrga kak?')"],
         ["Tidak ingat percakapan", "Punya memory (ingat sudah sampai mana)"],
         ["Satu langkah", "Multi-langkah: sapa - jawab - tangkap lead"],
         ["Tidak menilai maksud", "Deteksi intent (niat) pelanggan"]],
        [6.0 * cm, 10.6 * cm]))

    # ---------- BAB 2: Roadmap ----------
    e.append(Spacer(1, 0.3 * cm))
    e += h1(2, "Peta Perjalanan (Roadmap Zero - Hero)")
    e.append(img("01_roadmap.png", 16.5))
    e.append(Paragraph("Gambar 1. Sebelas level dari Nol sampai Hero.", st_caption))
    e.append(make_table(
        ["Level", "Nama", "Hasil yang didapat"],
        [["L0", "Fondasi", "Paham AI Autonomous, LLM, intent, webhook"],
         ["L1", "Akun &amp; Platform", "Punya API key/token gratis"],
         ["L2", "Lingkungan", "Python siap, project bisa jalan"],
         ["L3", "Hello AI", "Otak AI menjawab pertanyaan pertama"],
         ["L4", "Auto-Reply", "Bot membalas pesan WhatsApp otomatis"],
         ["L5", "FAQ Flow", "Bot menjawab pertanyaan umum"],
         ["L6", "Auto Greeting", "Sapaan otomatis (baru/kembali/luar jam)"],
         ["L7", "Lead Capture", "Tangkap nama &amp; intent calon pembeli"],
         ["L8", "Testing", "Uji otomatis + optimasi jawaban"],
         ["L9", "Deploy 24/7", "Bot online sendiri tanpa laptop"],
         ["L10", "Hero", "Multi-channel, CRM, follow-up, no-code"]],
        [1.7 * cm, 4.0 * cm, 10.9 * cm]))

    # ---------- BAB 3: Platform ----------
    e.append(PageBreak())
    e += h1(3, "Platform yang Bisa Diakses dari Indonesia")
    e.append(Paragraph("A. Platform \"Otak\" AI (LLM)", st_h2))
    e.append(make_table(
        ["Platform", "Paket gratis", "Catatan"],
        [["Google AI Studio (Gemini)", "Sangat murah hati", "Rekomendasi utama, cukup akun Google"],
         ["OpenAI (ChatGPT API)", "Perlu top-up ($5)", "Butuh kartu internasional"],
         ["Groq", "Gratis, sangat cepat", "Alternatif gratis selain Gemini"]],
        [5.4 * cm, 4.9 * cm, 6.3 * cm]))
    e.append(callout(
        "<b>Kita pakai Gemini.</b> Per awal 2026 paket gratis berpusat pada model 2.5. "
        "Contoh batas: Gemini 2.5 Flash sekitar 10 permintaan/menit &amp; 250/hari; "
        "Flash-Lite sekitar 15/menit &amp; 1.000/hari. Batas bisa berubah - cek dokumentasi "
        "resmi. <i>Informasi dirangkum ulang untuk kepatuhan lisensi.</i>", color=BLUE))
    e.append(Spacer(1, 0.2 * cm))
    e.append(Paragraph("B. Platform Gateway WhatsApp", st_h2))
    e.append(make_table(
        ["Platform", "Jenis", "Biaya", "Cocok untuk"],
        [["Fonnte", "Gateway lokal Indonesia", "Murah, mudah", "Pemula &amp; UMKM (cepat jadi)"],
         ["Meta WhatsApp Cloud API", "Resmi dari Meta", "Pesan layanan gratis", "Resmi &amp; skala besar"],
         ["Wablas / Watzap.id", "Gateway lokal", "Berbayar (murah)", "Alternatif lokal"],
         ["console (mode belajar)", "Cetak ke layar", "Rp 0", "Belajar tanpa akun apa pun"]],
        [4.4 * cm, 4.3 * cm, 3.6 * cm, 4.3 * cm]))
    e.append(callout(
        "<b>Tutorial ini mendukung keduanya (Fonnte &amp; Meta)</b> - cukup ubah satu baris "
        "<font face='Courier'>WHATSAPP_PROVIDER</font> di file .env. Ada juga mode "
        "<font face='Courier'>console</font> untuk belajar 100% gratis tanpa akun.",
        color=GREEN, bg=colors.HexColor("#E8F5E9")))
    e.append(callout(
        "<b>Kabar baik biaya Meta:</b> sejak akhir 2024 percakapan layanan (yang dimulai "
        "pelanggan) gratis, dan sejak April 2025 template utility gratis dalam jendela 24 jam. "
        "Karena bot kita MEMBALAS pesan masuk, sebagian besar interaksi GRATIS (Meta memberi "
        "sekitar 1.000 percakapan layanan gratis/bulan). <i>Dirangkum ulang dari dokumentasi "
        "harga resmi WhatsApp Business untuk kepatuhan lisensi.</i>", color=BLUE))

    # ---------- BAB 4: Arsitektur ----------
    e.append(PageBreak())
    e += h1(4, "Arsitektur Sistem & Cara Kerja Bot")
    e.append(img("02_arsitektur.png", 16.0))
    e.append(Paragraph("Gambar 2. Arsitektur sistem bot WhatsApp AI.", st_caption))
    e.append(Paragraph(
        "Pesan pelanggan masuk lewat gateway (Fonnte/Meta) ke server webhook (Flask, "
        "<font face='Courier'>app.py</font>), diteruskan ke otak <font face='Courier'>"
        "bot.py</font> yang memutuskan balasan, lalu dikirim kembali. Data sesi &amp; lead "
        "disimpan di SQLite; jawaban FAQ disusun oleh Gemini (opsional).", st_body))
    e.append(Spacer(1, 0.2 * cm))
    e.append(img("03_agent_loop.png", 16.0))
    e.append(Paragraph(
        "Gambar 3. Siklus kerja bot (Terima - Pikir - Aksi - Ulangi) dan 4 komponen inti.",
        st_caption))
    e.append(Paragraph(
        "Empat komponen inti: <b>Otak (LLM)</b> untuk memahami &amp; menjawab, "
        "<b>Tools/Modul</b> (greeting, FAQ, lead capture), <b>Memory</b> (SQLite) untuk "
        "mengingat status, dan <b>Loop</b> sebagai siklus kerja berulang.", st_body))

    # ---------- BAB 5: Langkah membangun ----------
    e.append(PageBreak())
    e += h1(5, "Langkah Demi Langkah Membangun Proyek")

    e.append(Paragraph("Level 2 - Siapkan lingkungan", st_h3))
    e.append(code_block(
        "git clone https://github.com/andizulham/Temporary.git\n"
        "cd Temporary/ai-whatsapp-automation-tutorial\n"
        "python -m venv venv && source venv/bin/activate\n"
        "pip install -r requirements.txt\n"
        "cp .env.example .env     # untuk belajar: WHATSAPP_PROVIDER=console"))

    e.append(Paragraph("Level 3 - Hello AI (uji otak)", st_h3))
    e.append(code_block(
        "python src/ai_brain.py\n"
        "# Tanpa GEMINI_API_KEY: mode aturan (gratis, tetap jawab FAQ).\n"
        "# Dengan key: jawaban natural, tetap grounded ke data/faq.json."))

    e.append(Paragraph("Level 4 - WhatsApp Auto-Reply", st_h3))
    e.append(code_block(
        "python src/simulator.py demo   # coba tanpa WhatsApp (gratis)\n"
        "python src/app.py              # server webhook di :5000\n"
        "ngrok http 5000                # URL publik utk didaftarkan ke gateway"))
    e.append(callout(
        "<b>Inti auto-reply:</b> setiap pesan masuk memanggil "
        "<font face='Courier'>bot.handle_message(nomor, teks)</font> yang mengembalikan "
        "balasan, lalu dikirim lewat gateway. Logika yang sama dipakai di simulator "
        "maupun WhatsApp sungguhan.", color=GREEN, bg=colors.HexColor("#E8F5E9")))

    e.append(Paragraph("Level 5 - Alur FAQ", st_h3))
    e.append(Paragraph(
        "Semua FAQ ada di <font face='Courier'>data/faq.json</font> - bisa diubah TANPA "
        "menyentuh kode (ramah no-code). Bot mencocokkan kata kunci; bila AI aktif, "
        "Gemini menyusun jawaban natural namun tetap grounded.", st_body))
    e.append(code_block(
        "python src/knowledge_base.py    # tes pencarian FAQ\n"
        "# 'berapa harganya ya?' -> cocok: harga\n"
        "# 'kantornya dimana'    -> cocok: lokasi"))

    e.append(Paragraph("Level 6 - Auto Greeting", st_h3))
    e.append(make_table(
        ["Situasi", "Isi sapaan"],
        [["Kontak BARU", "Salam + perkenalan + menu pilihan"],
         ["Kontak KEMBALI", "\"Selamat datang kembali\" + menu"],
         ["Di LUAR jam kerja", "Beri tahu jam buka + tetap bantu 24 jam"]],
        [4.5 * cm, 12.1 * cm]))

    e.append(Paragraph("Level 7 - Lead Capture (nama &amp; intent)", st_h3))
    e.append(img("05_lead_flow.png", 16.2))
    e.append(Paragraph(
        "Gambar 4. Alur lead capture: pemicu - tanya nama - tanya intent - simpan - konfirmasi.",
        st_caption))
    e.append(code_block(
        "python src/simulator.py demo    # lihat alur lengkap sapaan->FAQ->lead\n"
        "python src/simulator.py leads   # tampilkan lead yang tertangkap"))

    # ---------- BAB 6: Alur keputusan + Testing ----------
    e.append(PageBreak())
    e += h1(6, "Alur Keputusan Bot & Testing")
    e.append(img("04_alur_percakapan.png", 16.2))
    e.append(Paragraph(
        "Gambar 5. Untuk setiap pesan, bot memeriksa kondisi berurutan: sedang isi lead? "
        "kontak baru? niat daftar? cocok FAQ? - lalu memilih aksi yang tepat.", st_caption))
    e.append(Paragraph("Level 8 - Testing &amp; Optimasi", st_h2))
    e.append(code_block("pytest -q\n# Hasil diharapkan: 9 passed"))
    e.append(make_table(
        ["Test", "Memastikan"],
        [["test_selalu_membalas", "Bot selalu membalas (auto-reply)"],
         ["test_kontak_baru_disapa", "Kontak baru dapat sapaan + menu"],
         ["test_greeting_after_hours", "Sapaan \"luar jam\" muncul saat tutup"],
         ["test_faq_harga / lokasi", "FAQ dijawab benar"],
         ["test_deteksi_intent", "Niat lead/faq/greeting terdeteksi"],
         ["test_lead_capture_tersimpan", "Lead (nama+intent) tersimpan"],
         ["test_lead_capture_dibatalkan", "Pelanggan bisa membatalkan"]],
        [6.4 * cm, 10.2 * cm], header_bg=TEAL))
    e.append(Paragraph("Langkah optimasi dasar", st_h3))
    e.append(bullets([
        "Perkaya <b>keyword</b> FAQ dari pertanyaan asli pelanggan.",
        "Persingkat jawaban + beri satu ajakan (CTA) yang jelas.",
        "Tambahkan FAQ baru untuk pertanyaan yang sering masuk.",
        "Aktifkan Gemini agar jawaban natural saat kata kunci tidak persis.",
        "Ukur % pesan terjawab otomatis (target awal 70%). Jalankan pytest tiap perubahan.",
    ]))

    # ---------- BAB 7: Rincian Biaya ----------
    e.append(PageBreak())
    e += h1(7, "Rincian Biaya Lengkap (Hemat & Normal)")
    e.append(callout(
        "Asumsi kurs: 1 USD sekitar Rp 16.300 (estimasi 2026 - sesuaikan saat kamu membaca). "
        "Angka di bawah adalah estimasi dan dapat berubah. Selalu cek harga resmi tiap platform.",
        color=AMBER, bg=colors.HexColor("#FFF8E1")))
    e.append(Paragraph("A. Biaya Belajar (Skenario Pelajar Hemat)", st_h2))
    e.append(make_table(
        ["Komponen", "Pilihan gratis", "Biaya"],
        [["Materi belajar", "Tutorial ini + dokumentasi resmi", "Rp 0"],
         ["Otak AI", "Mode aturan / Gemini free tier", "Rp 0"],
         ["Gateway WhatsApp", "Mode console (cetak ke layar)", "Rp 0"],
         ["Tempat ngoding", "VS Code / Google Colab", "Rp 0"],
         ["Hosting belajar", "Laptop sendiri + ngrok", "Rp 0"],
         ["TOTAL BELAJAR", "", "Rp 0"]],
        [4.6 * cm, 8.0 * cm, 4.0 * cm], header_bg=LIGHTGREEN))
    e.append(callout(
        "<b>Kamu benar-benar bisa membangun &amp; menguji kelima proyek (Level 4-8) tanpa "
        "mengeluarkan uang sama sekali (Rp 0)</b> memakai mode console + mode aturan.",
        color=GREEN, bg=colors.HexColor("#E8F5E9")))
    e.append(Spacer(1, 0.2 * cm))
    e.append(Paragraph("B. Biaya Operasional Bulanan (Hemat vs Normal vs Pro)", st_h2))
    e.append(img("06_biaya.png", 14.5))
    e.append(Paragraph("Gambar 6. Perbandingan estimasi biaya bulanan.", st_caption))
    e.append(make_table(
        ["Komponen", "Hemat (Gratis)", "Normal (UMKM)", "Pro (Skala besar)"],
        [["Otak AI (Gemini)", "Rp 0", "Rp 0", "Rp 150-500rb"],
         ["Gateway WhatsApp", "Meta API - Rp 0", "Fonnte - Rp 50-150rb", "Rp 300-500rb+"],
         ["Hosting 24/7", "Laptop/free - Rp 0", "VPS - Rp 50-100rb", "Rp 200-400rb"],
         ["Notifikasi", "Rp 0", "Rp 0", "Rp 0 / CRM"],
         ["TOTAL / BULAN", "Rp 0", "Rp 100-250rb", "Rp 650rb-1,4jt+"]],
        [4.4 * cm, 3.9 * cm, 4.0 * cm, 4.3 * cm], header_bg=NAVY))
    e.append(callout(
        "<b>Versi HEMAT (Rp 0):</b> Meta Cloud API (balasan ke pelanggan gratis + ~1.000 "
        "percakapan layanan gratis/bulan) + Gemini free tier + hosting gratis. "
        "<b>Versi NORMAL (Rp 100-250rb/bln):</b> Fonnte (paling mudah &amp; cepat jadi) + "
        "Gemini free tier + VPS murah agar online 24 jam - pilihan paling praktis untuk UMKM.",
        color=BLUE))

    # ---------- BAB 8: Keamanan & rencana ----------
    e.append(PageBreak())
    e += h1(8, "Keamanan, Etika & Rencana Belajar")
    e.append(Paragraph("Aturan penting", st_h2))
    e.append(make_table(
        ["Aturan", "Penjelasan"],
        [["Simpan token di .env", "Jangan hard-code, jangan commit ke GitHub"],
         ["Jangan spam / blast", "Kirim hanya ke kontak yang setuju (opt-in)"],
         ["Lindungi data lead (UU PDP)", "Simpan secukupnya, jangan sebar"],
         ["Beri tahu ini bot", "Sediakan jalur ke manusia bila perlu"],
         ["Uji sebelum live", "Jalankan pytest &amp; simulator dulu"]],
        [5.2 * cm, 11.4 * cm], header_bg=RED))
    e.append(Spacer(1, 0.2 * cm))
    e.append(Paragraph("Rencana belajar 4 minggu", st_h2))
    e.append(make_table(
        ["Minggu", "Fokus", "Target"],
        [["Minggu 1", "Level 0-3", "Paham konsep, akun siap, otak AI menjawab"],
         ["Minggu 2", "Level 4-5", "Auto-reply jalan + FAQ otomatis aktif"],
         ["Minggu 3", "Level 6-7", "Auto greeting + lead capture menyimpan data"],
         ["Minggu 4", "Level 8-10", "Testing hijau, deploy 24/7, +1 fitur Hero"]],
        [2.7 * cm, 3.0 * cm, 10.9 * cm], header_bg=TEAL))
    e.append(Spacer(1, 0.2 * cm))
    e.append(Paragraph("Naik kelas jadi Hero (Level 10)", st_h2))
    e.append(bullets([
        "<b>No-code/low-code:</b> n8n, Dify, Flowise (gratis/self-host).",
        "<b>Notifikasi lead real-time</b> ke grup WhatsApp/Telegram/email tim.",
        "<b>Integrasi CRM / Google Sheets</b> untuk follow-up otomatis.",
        "<b>Multi-channel:</b> pakai logika bot.py yang sama untuk Instagram/Telegram.",
        "<b>RAG:</b> beri bot katalog/brosur agar jawaban makin pintar.",
    ]))

    e.append(Spacer(1, 0.4 * cm))
    e.append(HRFlowable(width="100%", thickness=1.2, color=NAVY))
    e.append(Spacer(1, 0.2 * cm))
    e.append(Paragraph(
        "Selamat! Dari NOL, kamu kini punya bot WhatsApp AI yang bisa balas otomatis, "
        "jawab FAQ, menyapa, dan menangkap lead. Kode lengkap ada di folder src/, "
        "materi lengkap di TUTORIAL.md.",
        S("end", fontName="Helvetica-Bold", fontSize=10.5, leading=15,
          textColor=NAVY, alignment=TA_CENTER)))
    e.append(Paragraph(
        "Gunakan dengan etis &amp; patuhi aturan WhatsApp. Selamat belajar!", st_caption))

    doc.build(e)
    print("PDF berhasil dibuat:", OUT)
    print("Ukuran:", round(os.path.getsize(OUT) / 1024, 1), "KB")


if __name__ == "__main__":
    build()
