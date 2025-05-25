import sqlite3

conn = sqlite3.connect("db/market_app.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE Sectors (
    name TEXT PRIMARY KEY,
    api_endpoint TEXT CHECK(api_endpoint IN (
        'technology', 'finance_service', 'communication_service', 'healthcare',
        'industrual', 'consumer_defense', 'energy', 'materials', 'real_estate', 'utilities'
    ))
);
""")

cursor.execute("""
CREATE TABLE Tickers (
    symbol TEXT PRIMARY KEY,
    name TEXT,
    type TEXT,
    sectors TEXT,
    added_at DATETIME,
    api_endpoint TEXT,
    FOREIGN KEY(sectors) REFERENCES Sectors(name)
);
""")

cursor.execute("""
CREATE TABLE Signals (
    ticker_symbol TEXT PRIMARY KEY,
    signal_type TEXT CHECK(signal_type IN ('buy', 'sell', 'hold')),
    confidence REAL,
    FOREIGN KEY(ticker_symbol) REFERENCES Tickers(symbol)
);
""")

cursor.execute("""
CREATE TABLE Forecasts (
    symbol TEXT PRIMARY KEY,
    model_version TEXT,
    generated_at DATETIME,
    file_path TEXT,
    FOREIGN KEY(symbol) REFERENCES Tickers(symbol)
);
""")

conn.commit()
conn.close()