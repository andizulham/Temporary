"""
tracker.py
==========
Modul pelacak (tracker) trade: menyimpan riwayat swap ke database SQLite
dan menghitung ringkasan sederhana (jumlah trade, volume, dsb).

SQLite dipilih karena: gratis, bawaan Python, dan tidak perlu server terpisah.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

from config import settings
from solana_client import get_wallet_transactions, parse_swaps


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Buat tabel jika belum ada."""
    with _conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS trades (
                signature   TEXT PRIMARY KEY,
                timestamp   INTEGER,
                type        TEXT,
                description TEXT,
                token_in    TEXT,
                amount_in   REAL,
                token_out   TEXT,
                amount_out  REAL,
                created_at  TEXT
            )
            """
        )


def sync_wallet(wallet: str | None = None, limit: int = 30) -> int:
    """
    Tarik transaksi terbaru dari dompet, simpan swap baru ke database.
    Mengembalikan jumlah trade baru yang tersimpan.
    """
    wallet = wallet or settings.WALLET_ADDRESS
    init_db()

    txs = get_wallet_transactions(wallet, limit=limit)
    swaps = parse_swaps(txs, wallet)

    baru = 0
    now = datetime.now(timezone.utc).isoformat()
    with _conn() as conn:
        for s in swaps:
            try:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO trades
                    (signature, timestamp, type, description, token_in,
                     amount_in, token_out, amount_out, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        s["signature"], s["timestamp"], s["type"], s["description"],
                        s["token_in"], s["amount_in"], s["token_out"],
                        s["amount_out"], now,
                    ),
                )
                if conn.total_changes:
                    baru += 1
            except sqlite3.Error:
                continue
    return baru


def get_recent_trades(limit: int = 20) -> list[dict]:
    """Ambil trade terakhir dari database."""
    init_db()
    with _conn() as conn:
        rows = conn.execute(
            "SELECT * FROM trades ORDER BY timestamp DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def summarize() -> dict:
    """Ringkasan statistik sederhana dari semua trade tersimpan."""
    init_db()
    with _conn() as conn:
        total = conn.execute("SELECT COUNT(*) AS n FROM trades").fetchone()["n"]
        first = conn.execute(
            "SELECT MIN(timestamp) AS t FROM trades"
        ).fetchone()["t"]
        last = conn.execute(
            "SELECT MAX(timestamp) AS t FROM trades"
        ).fetchone()["t"]

    def _fmt(ts):
        if not ts:
            return "-"
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")

    return {
        "total_trades": total,
        "first_trade": _fmt(first),
        "last_trade": _fmt(last),
    }


if __name__ == "__main__":
    n = sync_wallet()
    print(f"Trade baru tersimpan: {n}")
    print("Ringkasan:", summarize())
    for t in get_recent_trades(5):
        print(t["timestamp"], t["type"], t["description"][:60])
