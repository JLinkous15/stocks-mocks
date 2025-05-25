from fastapi import FastAPI
from routes import tickers, signals, forecasts

app = FastAPI()

app.include_router(tickers.router, prefix="/tickers")
app.include_router(signals.router, prefix="/signals")
app.include_router(forecasts.router, prefix="/forecasts")
