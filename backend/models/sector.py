from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from helpers import utc_now

class SectorType(str, Enum):
    technology = "technology"
    finance_service = "finance_service"
    communication_service = "communication_service"
    healthcare = "healthcare"
    industrial = "industrial"
    consumer_defense = "consumer_defense"
    energy = "energy"
    materials = "materials"
    real_estate = "real_estate"
    utilities = "utilities"

class Sector(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: SectorType
    api_endpoint: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)
