from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID, uuid4

SignalType = Literal["buy", "sell", "hold"]

class Signal(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    ticker_id: UUID
    signal_type: SignalType
    created_at: Optional[datetime]
    expired_at: Optional[datetime]
    confidence: float

    @field_validator("confidence")
    def confidence_in_range(cls, v):
        if not (0 <= v <= 1):
            raise ValueError("Confidence must be between 0 and 1")
        return v