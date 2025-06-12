from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from helpers import utc_now

class Forecast(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    ticker_id: UUID
    model_version: Optional[str]
    storage_uri: Optional[str]
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)