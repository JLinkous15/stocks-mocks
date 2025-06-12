# backend/routes/tickers.py
from fastapi import APIRouter, HTTPException
from backend.models.ticker import Ticker
import sqlite3
from uuid import UUID
from pathlib import Path

ticker_router = APIRouter()
BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "db" / "market_app.db"


# --- Helper: DB connection ---
def get_db():
    return sqlite3.connect(DB_PATH)


# --- GET all tickers ---
@ticker_router.get("/tickers", response_model=list[Ticker])
def get_all_tickers():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Tickers")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return []
    return [Ticker(**dict(zip([column[0] for column in cursor.description], row))) for row in rows]


# --- GET ticker by ID ---
@ticker_router.get("/tickers/{ticker_id}", response_model=Ticker)
def get_ticker(ticker_id: UUID):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Tickers WHERE id = ?", (str(ticker_id),))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Ticker not found")
    return Ticker(**dict(zip([column[0] for column in cursor.description], row)))


# --- POST new ticker ---
@ticker_router.post("/tickers", response_model=Ticker)
def create_ticker(ticker: Ticker):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Tickers (
                id, symbol, name, type, sector_id, api_endpoint,
                is_owned, notes, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(ticker.id), ticker.symbol, ticker.name, ticker.type, str(ticker.sector_id) if ticker.sector_id else None,
            ticker.api_endpoint, ticker.is_owned, ticker.notes, ticker.created_at.isoformat(), ticker.updated_at.isoformat()
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Ticker with this symbol or ID already exists")
    finally:
        conn.close()
    return ticker


# --- PUT update ticker ---
@ticker_router.put("/tickers/{ticker_id}", response_model=Ticker)
def update_ticker(ticker_id: UUID, updated: Ticker):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Tickers WHERE id = ?", (str(ticker_id),))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Ticker not found")

    cursor.execute("""
        UPDATE Tickers SET
            symbol = ?, name = ?, type = ?, sector_id = ?, api_endpoint = ?,
            is_owned = ?, notes = ?, created_at = ?, updated_at = ?
        WHERE id = ?
    """, (
        updated.symbol, updated.name, updated.type,
        str(updated.sector_id) if updated.sector_id else None,
        updated.api_endpoint, updated.is_owned, updated.notes,
        updated.created_at.isoformat(), updated.updated_at.isoformat(),
        str(ticker_id)
    ))
    conn.commit()
    conn.close()
    return updated


# --- DELETE ticker ---
@ticker_router.delete("/tickers/{ticker_id}")
def delete_ticker(ticker_id: UUID):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Tickers WHERE id = ?", (str(ticker_id),))
    conn.commit()
    conn.close()
    return {"message": f"Ticker {ticker_id} deleted"}
