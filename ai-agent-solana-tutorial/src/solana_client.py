"""
solana_client.py
================
Lapisan "alat" (tools) untuk AI Agent: mengambil data dari blockchain Solana.

Dua sumber data utama (keduanya punya free tier):
  1. Helius  -> riwayat transaksi sebuah dompet (parsed/enhanced transactions)
  2. DexScreener -> harga & info token terkini (tanpa API key)

Catatan: semua fungsi mengembalikan dict/list Python biasa supaya mudah
diproses oleh modul tracker.py & evaluator.py.
"""

from __future__ import annotations

import time
import requests

from config import settings

HELIUS_BASE = "https://api.helius.xyz/v0"
DEXSCREENER_BASE = "https://api.dexscreener.com"

# Mint resmi untuk token referensi
SOL_MINT = "So11111111111111111111111111111111111111112"
USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"


def _get(url: str, params: dict | None = None, retries: int = 3) -> dict | list:
    """Helper HTTP GET dengan retry sederhana (menghadapi rate limit / 429)."""
    for attempt in range(retries):
        resp = requests.get(url, params=params, timeout=20)
        if resp.status_code == 429:
            # Kena rate limit -> tunggu sebentar lalu coba lagi
            time.sleep(2 * (attempt + 1))
            continue
        resp.raise_for_status()
        return resp.json()
    resp.raise_for_status()
    return {}


# --------------------------------------------------------------------------
#  DEXSCREENER: harga & metadata token (gratis, tanpa key, ~300 req/menit)
# --------------------------------------------------------------------------
def get_token_price(mint_address: str) -> dict:
    """
    Ambil harga & info pasar sebuah token Solana berdasarkan alamat mint.
    Mengembalikan dict: {symbol, name, price_usd, liquidity_usd, fdv, url}
    """
    url = f"{DEXSCREENER_BASE}/tokens/v1/solana/{mint_address}"
    data = _get(url)

    if not data:
        return {"mint": mint_address, "price_usd": None, "found": False}

    # DexScreener mengembalikan list pair; pilih pair dengan likuiditas terbesar
    pairs = data if isinstance(data, list) else data.get("pairs", [])
    if not pairs:
        return {"mint": mint_address, "price_usd": None, "found": False}

    best = max(pairs, key=lambda p: (p.get("liquidity", {}) or {}).get("usd", 0) or 0)
    base = best.get("baseToken", {})
    return {
        "mint": mint_address,
        "symbol": base.get("symbol", "?"),
        "name": base.get("name", "?"),
        "price_usd": float(best.get("priceUsd", 0) or 0),
        "liquidity_usd": (best.get("liquidity", {}) or {}).get("usd", 0),
        "fdv": best.get("fdv", 0),
        "url": best.get("url", ""),
        "found": True,
    }


# --------------------------------------------------------------------------
#  HELIUS: riwayat transaksi dompet (enhanced/parsed transactions)
# --------------------------------------------------------------------------
def get_wallet_transactions(wallet: str, limit: int = 20) -> list[dict]:
    """
    Ambil transaksi terbaru sebuah dompet dalam bentuk yang sudah diparse Helius.
    Mengembalikan list transaksi mentah (raw) dari Helius.
    """
    url = f"{HELIUS_BASE}/addresses/{wallet}/transactions"
    params = {"api-key": settings.HELIUS_API_KEY, "limit": limit}
    data = _get(url, params=params)
    return data if isinstance(data, list) else []


def parse_swaps(transactions: list[dict], wallet: str) -> list[dict]:
    """
    Saring transaksi menjadi daftar SWAP (beli/jual token) yang mudah dibaca.

    Setiap item hasil: {
        signature, timestamp, type, description,
        token_in, amount_in, token_out, amount_out
    }
    """
    swaps = []
    for tx in transactions:
        tx_type = tx.get("type", "")
        if tx_type not in ("SWAP", "UNKNOWN"):
            # Fokus pada swap; UNKNOWN kadang juga swap via aggregator
            if "swap" not in (tx.get("description", "") or "").lower():
                continue

        token_transfers = tx.get("tokenTransfers", []) or []
        masuk, keluar = [], []
        for t in token_transfers:
            if t.get("toUserAccount") == wallet:
                masuk.append(t)
            elif t.get("fromUserAccount") == wallet:
                keluar.append(t)

        swaps.append({
            "signature": tx.get("signature", "")[:16] + "...",
            "timestamp": tx.get("timestamp", 0),
            "type": tx_type,
            "description": tx.get("description", ""),
            "token_in": keluar[0].get("mint") if keluar else None,
            "amount_in": keluar[0].get("tokenAmount") if keluar else None,
            "token_out": masuk[0].get("mint") if masuk else None,
            "amount_out": masuk[0].get("tokenAmount") if masuk else None,
        })
    return swaps


def get_sol_price_usd() -> float:
    """Harga SOL dalam USD (untuk konversi nilai portfolio)."""
    info = get_token_price(SOL_MINT)
    return info.get("price_usd") or 0.0


if __name__ == "__main__":
    # Tes cepat manual: python solana_client.py
    print("Harga SOL  : $", get_sol_price_usd())
    print("Info USDC  :", get_token_price(USDC_MINT))
