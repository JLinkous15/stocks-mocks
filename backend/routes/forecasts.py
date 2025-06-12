# backend/routes/forecasts.py
from fastapi import APIRouter, HTTPException, UploadFile, File
from backend.models.forecast import Forecast
from uuid import UUID
from pathlib import Path
import sqlite3
import boto3
import json
from datetime import datetime, timezone

forecast_router = APIRouter()
BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "db" / "market_app.db"

s3 = boto3.client("s3")
BUCKET_NAME = "your-s3-bucket-name"  # <-- set your bucket here


def get_db():
    return sqlite3.connect(DB_PATH)


def upload_forecast_to_s3(forecast_id: str, data: dict) -> str:
    key = f"forecasts/{forecast_id}.json"
    s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=json.dumps(data))
    return f"s3://{BUCKET_NAME}/{key}"


def download_forecast_from_s3(storage_uri: str) -> dict:
    parts = storage_uri.replace("s3://", "").split("/", 1)
    bucket, key = parts[0], parts[1]
    obj = s3.get_object(Bucket=bucket, Key=key)
    return json.loads(obj["Body"].read().decode("utf-8"))


def delete_forecast_from_s3(storage_uri: str):
    parts = storage_uri.replace("s3://", "").split("/", 1)
    bucket, key = parts[0], parts[1]
    s3.delete_object(Bucket=bucket, Key=key)


@forecast_router.get("/forecasts", response_model=list[Forecast])
def get_all_forecasts():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Forecasts")
    rows = cursor.fetchall()
    conn.close()
    return [Forecast(**dict(zip([c[0] for c in cursor.description], row))) for row in rows]


@forecast_router.get("/forecasts/{forecast_id}", response_model=Forecast)
def get_forecast(forecast_id: UUID):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Forecasts WHERE id = ?", (str(forecast_id),))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Forecast not found")
    return Forecast(**dict(zip([c[0] for c in cursor.description], row)))


@forecast_router.post("/forecasts", response_model=Forecast)
async def create_forecast(forecast: Forecast, forecast_file: UploadFile = File(...)):
    # Load JSON data from uploaded file
    data = await forecast_file.read()
    json_data = json.loads(data)

    # Upload JSON to S3
    storage_uri = upload_forecast_to_s3(str(forecast.id), json_data)

    # Update metadata fields
    now = datetime.now(timezone.utc)
    forecast.storage_uri = storage_uri
    forecast.created_at = now
    forecast.updated_at = now

    # Insert metadata into DB
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Forecasts (id, ticker_id, model_version, storage_uri, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            str(forecast.id), str(forecast.ticker_id), forecast.model_version,
            forecast.storage_uri, forecast.created_at.isoformat(), forecast.updated_at.isoformat()
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Forecast already exists or invalid foreign key")
    finally:
        conn.close()

    return forecast


@forecast_router.put("/forecasts/{forecast_id}", response_model=Forecast)
async def update_forecast(forecast_id: UUID, updated: Forecast, forecast_file: UploadFile = File(None)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Forecasts WHERE id = ?", (str(forecast_id),))
    existing = cursor.fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Forecast not found")

    # If new file uploaded, update S3 object
    if forecast_file:
        data = await forecast_file.read()
        json_data = json.loads(data)
        # Delete old S3 object
        old_storage_uri = existing[cursor.description.index(("storage_uri", None, None, None, None, None, None))]
        delete_forecast_from_s3(old_storage_uri)
        # Upload new object
        storage_uri = upload_forecast_to_s3(str(forecast_id), json_data)
    else:
        # Keep existing URI
        storage_uri = existing[cursor.description.index(("storage_uri", None, None, None, None, None, None))]

    updated.updated_at = datetime.now(timezone.utc)
    updated.created_at = updated.created_at or datetime.now(timezone.utc)
    updated.storage_uri = storage_uri

    cursor.execute("""
        UPDATE Forecasts SET
            ticker_id = ?, model_version = ?, storage_uri = ?, created_at = ?, updated_at = ?
        WHERE id = ?
    """, (
        str(updated.ticker_id), updated.model_version, updated.storage_uri,
        updated.created_at.isoformat(), updated.updated_at.isoformat(),
        str(forecast_id)
    ))
    conn.commit()
    conn.close()

    return updated


@forecast_router.delete("/forecasts/{forecast_id}")
def delete_forecast(forecast_id: UUID):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT storage_uri FROM Forecasts WHERE id = ?", (str(forecast_id),))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Forecast not found")

    storage_uri = row[0]
    delete_forecast_from_s3(storage_uri)

    cursor.execute("DELETE FROM Forecasts WHERE id = ?", (str(forecast_id),))
    conn.commit()
    conn.close()
    return {"message": f"Forecast {forecast_id} deleted"}
