# backend/routes/signals.py
from fastapi import APIRouter, HTTPException
from backend.models.signal import Signal
from uuid import UUID
import sqlite3
import boto3
from datetime import datetime, timezone
from pathlib import Path

signal_router = APIRouter()
BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "db" / "market_app.db"

sns = boto3.client("sns")
SNS_TOPIC_ARN = "your-sns-topic-arn"  # Set your SNS topic ARN here


def get_db():
    return sqlite3.connect(DB_PATH)


@signal_router.get("/signals", response_model=list[Signal])
def get_all_signals():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Signals")
    rows = cursor.fetchall()
    conn.close()
    return [Signal(**dict(zip([c[0] for c in cursor.description], row))) for row in rows]


@signal_router.get("/signals/{signal_id}", response_model=Signal)
def get_signal(signal_id: UUID):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Signals WHERE id = ?", (str(signal_id),))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Signal not found")
    return Signal(**dict(zip([c[0] for c in cursor.description], row)))


@signal_router.post("/signals", response_model=Signal)
def create_signal(signal: Signal):
    signal.created_at = signal.created_at or datetime.now(timezone.utc)
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Signals (id, ticker_id, signal_type, created_at, expired_at, confidence)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            str(signal.id), str(signal.ticker_id), signal.signal_type,
            signal.created_at.isoformat(),
            signal.expired_at.isoformat() if signal.expired_at else None,
            signal.confidence
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Signal already exists or invalid foreign key")
    finally:
        conn.close()
    return signal


@signal_router.put("/signals/{signal_id}", response_model=Signal)
def update_signal(signal_id: UUID, updated: Signal):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Signals WHERE id = ?", (str(signal_id),))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Signal not found")

    cursor.execute("""
        UPDATE Signals SET ticker_id = ?, signal_type = ?, created_at = ?, expired_at = ?, confidence = ?
        WHERE id = ?
    """, (
        str(updated.ticker_id), updated.signal_type,
        updated.created_at.isoformat() if updated.created_at else None,
        updated.expired_at.isoformat() if updated.expired_at else None,
        updated.confidence, str(signal_id)
    ))
    conn.commit()
    conn.close()
    return updated


@signal_router.delete("/signals/{signal_id}")
def delete_signal(signal_id: UUID):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Signals WHERE id = ?", (str(signal_id),))
    conn.commit()
    conn.close()
    return {"message": f"Signal {signal_id} deleted"}


@signal_router.post("/signals/{signal_id}/send")
def send_signal_alert(signal_id: UUID):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Signals WHERE id = ?", (str(signal_id),))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Signal not found")

    signal_data = dict(zip([c[0] for c in cursor.description], row))
    message = (
        f"Signal Alert!\n"
        f"Ticker ID: {signal_data['ticker_id']}\n"
        f"Signal Type: {signal_data['signal_type']}\n"
        f"Confidence: {signal_data['confidence']:.2f}\n"
        f"Created At: {signal_data['created_at']}"
    )

    try:
        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject=f"Stock Signal: {signal_data['signal_type'].upper()}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send SNS message: {str(e)}")

    return {"message": "Signal alert sent", "sns_message_id": response.get("MessageId")}
