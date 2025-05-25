from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class Ticker(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    symbol: str = Field(..., max_length=10, description="Unique ticker symbol")
    name: Optional[str]
    type: Optional[str]
    sector_id: Optional[UUID]
    added_at: Optional[datetime]
    api_endpoint: Optional[str]

    @field_validator("symbol")
    def symbol_must_be_upper(cls, v):
        if not v.isupper():
            raise ValueError("Ticker symbol must be uppercase")
        return v