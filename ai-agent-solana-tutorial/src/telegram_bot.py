"""
telegram_bot.py
===============
Antarmuka (interface) AI Agent berupa bot Telegram. Pengguna cukup chat
dengan bot untuk: sinkron dompet, lihat ringkasan, minta evaluasi AI,
atau bertanya bebas (mode agent).

Perintah:
  /start    -> sapaan & bantuan
  /sync     -> tarik transaksi terbaru dari dompet ke database
  /ringkasan-> tampilkan statistik trade
  /evaluasi -> minta AI mengevaluasi trading kamu
  (teks bebas) -> ditanyakan ke AI Agent (mode function calling)

Jalankan: python telegram_bot.py
"""

from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import settings
from tracker import sync_wallet, summarize
from evaluator import evaluate_trades, run_agent

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Halo! Saya *SolanaTradeCoach*, AI Agent pelacak & evaluator trading "
        "Solana kamu.\n\n"
        "Perintah:\n"
        "/sync - tarik transaksi terbaru dari dompet\n"
        "/ringkasan - statistik trade\n"
        "/evaluasi - minta AI menilai trading kamu\n\n"
        "Atau ketik pertanyaan bebas, misal: _\"Apakah saya terlalu sering FOMO?\"_\n\n"
        "⚠️ Ini bukan nasihat keuangan. DYOR.",
        parse_mode="Markdown",
    )


async def sync_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("⏳ Menarik transaksi terbaru dari dompet...")
    try:
        n = sync_wallet()
        await update.message.reply_text(f"✅ Selesai. {n} trade baru tersimpan.")
    except Exception as e:  # noqa: BLE001
        await update.message.reply_text(f"❌ Gagal sync: {e}")


async def ringkasan_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    s = summarize()
    await update.message.reply_text(
        f"📊 *Ringkasan Trade*\n"
        f"Total trade: {s['total_trades']}\n"
        f"Trade pertama: {s['first_trade']}\n"
        f"Trade terakhir: {s['last_trade']}",
        parse_mode="Markdown",
    )


async def evaluasi_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🤖 AI sedang menganalisa trading kamu...")
    hasil = evaluate_trades()
    await update.message.reply_text(hasil)


async def free_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🤖 Sebentar, saya pikirkan dulu...")
    jawaban = run_agent(update.message.text)
    await update.message.reply_text(jawaban)


def main() -> None:
    if not settings.TELEGRAM_BOT_TOKEN:
        raise SystemExit("TELEGRAM_BOT_TOKEN belum diisi di file .env")

    app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sync", sync_cmd))
    app.add_handler(CommandHandler("ringkasan", ringkasan_cmd))
    app.add_handler(CommandHandler("evaluasi", evaluasi_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, free_text))

    print("Bot berjalan. Tekan Ctrl+C untuk berhenti.")
    app.run_polling()


if __name__ == "__main__":
    main()
