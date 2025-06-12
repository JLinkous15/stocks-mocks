from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from helpers import utc_now

class SignalType(str, Enum):
    buy = "buy"
    sell = "sell"
    hold = "hold"


class Signal(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    ticker_id: UUID
    signal_type: SignalType
    created_at: datetime = Field(default_factory=utc_now)
    expired_at: Optional[datetime]
    confidence: float

    @field_validator("confidence")
    def confidence_in_range(cls, v):
        if not (0 <= v <= 1):
            raise ValueError("Confidence must be between 0 and 1")
        return v