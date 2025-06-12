import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

def utc_now_str():
    return datetime.now(timezone.utc).isoformat()

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "db" / "market_app.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create UUIDs
sector_id = str(uuid.uuid4())
ticker_id = str(uuid.uuid4())
signal_id = str(uuid.uuid4())
forecast_id = str(uuid.uuid4())

# Timestamps
now = utc_now_str()

# Add a sector
cursor.execute("""
INSERT INTO Sectors (id, name, api_endpoint, created_at)
VALUES (?, ?, ?, ?)
""", (sector_id, "technology", "/api/sectors/technology", now))

# Add a ticker
cursor.execute("""
INSERT INTO Tickers (
    id, symbol, name, type, sector_id, api_endpoint, is_owned, notes, created_at, updated_at
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (ticker_id, "AAPL", "Apple Inc", "stock", sector_id, "/api/tickers/aapl", 1, "Example note", now, now))

# Add a signal
cursor.execute("""
INSERT INTO Signals (
    id, ticker_id, signal_type, created_at, expired_at, confidence
) VALUES (?, ?, ?, ?, ?, ?)
""", (signal_id, ticker_id, "buy", now, None, 0.93))

# Add a forecast
cursor.execute("""
INSERT INTO Forecasts (
    id, ticker_id, model_version, storage_uri, created_at, updated_at
) VALUES (?, ?, ?, ?, ?, ?)
""", (forecast_id, ticker_id, "llama-3-8b-quant", "/data/extrapolations/AAPL_20250525.json", now, now))

conn.commit()
conn.close()
