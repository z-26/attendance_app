from pydantic import BaseModel, validator
from typing import Optional

class CreateService(BaseModel):
    name: str
    description: Optional[str]
    no_of_days: int
    cost: float


class UpdateService(BaseModel):
    name: Optional[str]
    description: Optional[str]
    no_of_days: Optional[int]
    cost: Optional[float]