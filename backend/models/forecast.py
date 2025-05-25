from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID, uuid4

class Forecast(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    ticker_id: UUID
    model_version: Optional[str]
    generated_at: Optional[datetime]
    file_path: Optional[str]