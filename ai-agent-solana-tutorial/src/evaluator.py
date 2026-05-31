"""
evaluator.py
============
Inti "kecerdasan" AI Agent. Memakai Google Gemini untuk:
  1. Menganalisa daftar trade (swap) dari dompet.
  2. Memberi penilaian (skor disiplin, pola, risiko) dalam Bahasa Indonesia.
  3. Memberi saran perbaikan yang konkret.

Ada DUA mode:
  - evaluate_trades(): analisa langsung (1 panggilan, paling sederhana).
  - run_agent(): mode AGENT dengan "tools" -> Gemini bisa memanggil fungsi
    get_token_price() sendiri saat butuh data harga terbaru (function calling).
"""

from __future__ import annotations

import json
import google.generativeai as genai

from config import settings
from solana_client import get_token_price, get_sol_price_usd
from tracker import get_recent_trades, summarize

# Konfigurasi Gemini sekali di awal
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)


SYSTEM_PROMPT = """\
Kamu adalah "SolanaTradeCoach", asisten AI yang ahli mengevaluasi aktivitas
trading token di blockchain Solana. Tugasmu:
- Menganalisa riwayat trade pengguna secara objektif.
- Menilai disiplin, manajemen risiko, dan pola perilaku (FOMO, overtrading, dll).
- Memberi skor 1-10 untuk "Disiplin" dan "Manajemen Risiko".
- Memberi 3 saran perbaikan yang konkret dan mudah dipraktikkan.
Jawab SELALU dalam Bahasa Indonesia yang ringkas, jujur, dan membangun.
PENTING: Ini bukan nasihat keuangan. Selalu ingatkan pengguna untuk riset mandiri (DYOR).
"""


def _format_trades_for_prompt(trades: list[dict]) -> str:
    """Ubah list trade menjadi teks rapi untuk dimasukkan ke prompt."""
    if not trades:
        return "(Belum ada data trade.)"
    baris = []
    for t in trades:
        baris.append(
            f"- [{t.get('type')}] {t.get('description', '')[:80]} "
            f"(in={t.get('amount_in')} {(_short(t.get('token_in')))}, "
            f"out={t.get('amount_out')} {(_short(t.get('token_out')))})"
        )
    return "\n".join(baris)


def _short(mint: str | None) -> str:
    if not mint:
        return "-"
    return mint[:4] + ".." + mint[-4:]


def evaluate_trades(limit: int = 15) -> str:
    """Mode sederhana: kirim ringkasan + daftar trade ke Gemini, minta evaluasi."""
    if not settings.GEMINI_API_KEY:
        return "GEMINI_API_KEY belum diisi. Lengkapi file .env terlebih dahulu."

    trades = get_recent_trades(limit)
    ringkasan = summarize()
    sol_price = get_sol_price_usd()

    konteks = (
        f"Harga SOL saat ini: ${sol_price:.2f}\n"
        f"Total trade tersimpan: {ringkasan['total_trades']}\n"
        f"Trade pertama: {ringkasan['first_trade']} | terakhir: {ringkasan['last_trade']}\n\n"
        f"Daftar trade terbaru:\n{_format_trades_for_prompt(trades)}\n"
    )

    model = genai.GenerativeModel(
        settings.GEMINI_MODEL, system_instruction=SYSTEM_PROMPT
    )
    prompt = (
        "Berikut data trading saya di Solana. Tolong evaluasi dan beri skor "
        "serta saran perbaikan:\n\n" + konteks
    )
    resp = model.generate_content(prompt)
    return resp.text


# --------------------------------------------------------------------------
#  MODE AGENT: function calling (Gemini memutuskan kapan memanggil tool)
# --------------------------------------------------------------------------
def _tool_get_token_price(mint_address: str) -> dict:
    """Tool yang diekspos ke Gemini: ambil harga token berdasarkan mint."""
    return get_token_price(mint_address)


def run_agent(user_question: str) -> str:
    """
    Mode AGENT sesungguhnya: Gemini menerima pertanyaan bebas dari user,
    dan boleh memanggil tool get_token_price() bila perlu data harga.
    Ini contoh pola 'agentic loop' paling dasar.
    """
    if not settings.GEMINI_API_KEY:
        return "GEMINI_API_KEY belum diisi. Lengkapi file .env terlebih dahulu."

    trades = get_recent_trades(15)
    konteks_trade = _format_trades_for_prompt(trades)

    model = genai.GenerativeModel(
        settings.GEMINI_MODEL,
        system_instruction=SYSTEM_PROMPT,
        tools=[_tool_get_token_price],  # daftarkan fungsi sebagai tool
    )
    chat = model.start_chat(enable_automatic_function_calling=True)

    prompt = (
        f"Data trade terakhir saya:\n{konteks_trade}\n\n"
        f"Pertanyaan saya: {user_question}\n\n"
        "Jika perlu harga token terkini, gunakan tool yang tersedia."
    )
    resp = chat.send_message(prompt)
    return resp.text


if __name__ == "__main__":
    # Tes cepat: python evaluator.py
    print(evaluate_trades())
