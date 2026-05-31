"""
database.py
===========
Penyimpanan ringan memakai SQLite (bawaan Python, tanpa server).
Menyimpan dua hal:

1. sessions  -> status percakapan tiap nomor (state machine lead capture)
2. leads     -> data prospek yang berhasil ditangkap (nama & intent)

Semua fungsi sengaja kecil & jelas supaya mudah dipahami pemula.
"""

import sqlite3
from datetime import datetime, timezone, timedelta

from config import settings


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Membuat tabel jika belum ada. Aman dipanggil berkali-kali."""
    with _conn() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                phone        TEXT PRIMARY KEY,
                state        TEXT NOT NULL DEFAULT 'NEW',
                temp_name    TEXT,
                last_seen    TEXT,
                message_count INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                phone     TEXT NOT NULL,
                name      TEXT,
                intent    TEXT,
                note      TEXT,
                created_at TEXT NOT NULL
            )
            """
        )


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ----------------------- SESSION (status percakapan) -----------------------
def get_session(phone: str) -> dict:
    """Ambil sesi sebuah nomor. Buat baru (state=NEW) bila belum ada."""
    with _conn() as c:
        row = c.execute("SELECT * FROM sessions WHERE phone=?", (phone,)).fetchone()
        if row is None:
            c.execute(
                "INSERT INTO sessions (phone, state, last_seen, message_count) "
                "VALUES (?, 'NEW', ?, 0)",
                (phone, _now()),
            )
            return {"phone": phone, "state": "NEW", "temp_name": None,
                    "last_seen": None, "message_count": 0}
        return dict(row)


def update_session(phone: str, *, state: str = None, temp_name: str = None,
                   bump_count: bool = False) -> None:
    """Perbarui state / nama sementara / hitung pesan untuk sebuah nomor."""
    s = get_session(phone)
    new_state = state if state is not None else s["state"]
    new_name = temp_name if temp_name is not None else s["temp_name"]
    new_count = s["message_count"] + (1 if bump_count else 0)
    with _conn() as c:
        c.execute(
            "UPDATE sessions SET state=?, temp_name=?, last_seen=?, message_count=? "
            "WHERE phone=?",
            (new_state, new_name, _now(), new_count, phone),
        )


def is_returning(phone: str) -> bool:
    """True jika nomor ini pernah chat sebelumnya (bukan kontak baru)."""
    s = get_session(phone)
    return s["message_count"] > 0


# ----------------------- LEAD (prospek tertangkap) -------------------------
def save_lead(phone: str, name: str, intent: str, note: str = "") -> int:
    """Simpan satu lead. Mengembalikan id lead."""
    with _conn() as c:
        cur = c.execute(
            "INSERT INTO leads (phone, name, intent, note, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (phone, name, intent, note, _now()),
        )
        return cur.lastrowid


def get_leads(limit: int = 50) -> list[dict]:
    with _conn() as c:
        rows = c.execute(
            "SELECT * FROM leads ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]


def count_leads() -> int:
    with _conn() as c:
        return c.execute("SELECT COUNT(*) FROM leads").fetchone()[0]


if __name__ == "__main__":
    # Uji cepat: buat tabel & tampilkan jumlah lead
    init_db()
    print("Database siap di:", settings.DB_PATH)
    print("Jumlah lead tersimpan:", count_leads())
