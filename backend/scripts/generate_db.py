import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "db" / "market_app.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create Sectors table
cursor.execute("""
CREATE TABLE Sectors (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL CHECK(name IN (
        'technology', 'finance_service', 'communication_service', 'healthcare',
        'industrial', 'consumer_defense', 'energy', 'materials', 'real_estate', 'utilities'
    )),
    api_endpoint TEXT,
    created_at DATETIME NOT NULL
);
""")

# Create Tickers table
cursor.execute("""
CREATE TABLE Tickers (
    id TEXT PRIMARY KEY,
    symbol TEXT UNIQUE NOT NULL,
    name TEXT,
    type TEXT,
    sector_id TEXT,
    api_endpoint TEXT,
    is_owned BOOLEAN NOT NULL DEFAULT 0,
    notes TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY(sector_id) REFERENCES Sectors(id)
);
""")

# Create Signals table
cursor.execute("""
CREATE TABLE Signals (
    id TEXT PRIMARY KEY,
    ticker_id TEXT NOT NULL,
    signal_type TEXT NOT NULL CHECK(signal_type IN ('buy', 'sell', 'hold')),
    created_at DATETIME NOT NULL,
    expired_at DATETIME,
    confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 1),
    FOREIGN KEY(ticker_id) REFERENCES Tickers(id)
);
""")

# Create Forecasts table
cursor.execute("""
CREATE TABLE Forecasts (
    id TEXT PRIMARY KEY,
    ticker_id TEXT NOT NULL,
    model_version TEXT,
    storage_uri TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY(ticker_id) REFERENCES Tickers(id)
);
""")

conn.commit()
conn.close()
