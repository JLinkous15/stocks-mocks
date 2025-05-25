from pydantic import BaseModel, Field
from typing import Optional, Literal
from uuid import UUID, uuid4

SectorType = Literal[
    "technology",
    "finance_service",
    "communication_service",
    "healthcare",
    "industrual",
    "consumer_defense",
    "energy",
    "materials",
    "real_estate",
    "utilities",
]

class Sector(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: SectorType
    api_endpoint: Optional[str] = None