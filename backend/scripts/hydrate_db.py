import sqlite3

conn = sqlite3.connect("market_app.db")
cursor = conn.cursor()

# Add sectors
cursor.execute("INSERT INTO Sectors (name, api_endpoint) VALUES (?, ?)", 
               ("technology", "technology"))

# Add a ticker
cursor.execute("""INSERT INTO Tickers 
    (symbol, name, type, sectors, added_at, api_endpoint) 
    VALUES (?, ?, ?, ?, datetime('now'), ?)""",
    ("AAPL", "Apple Inc", "stock", "technology", "/api/aapl"))

# Add a signal
cursor.execute("INSERT INTO Signals (ticker_symbol, signal_type, confidence) VALUES (?, ?, ?)", 
               ("AAPL", "buy", 0.93))

# Add a forecast
cursor.execute("""INSERT INTO Forecasts 
    (symbol, model_version, generated_at, file_path) 
    VALUES (?, ?, datetime('now'), ?)""",
    ("AAPL", "llama-3-8b-quant", "/data/extrapolations/AAPL_20250525.json"))

conn.commit()

conn.commit()
conn.close()