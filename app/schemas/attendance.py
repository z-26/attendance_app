from pydantic import BaseModel, validator
from typing import Optional
from datetime import date


class CreateParticipants(BaseModel):
    service_id: int
    name: str
    date_of_birth: date
    blood_group: Optional[str]
    gender: str
    guardian_name: Optional[str]
    address: str
    start_date: date
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    pin_code: str
    mobile_number: str


class ParticipantsInDB(CreateParticipants):
    participant_code: str

class UpdateParticipants(BaseModel):
    service_id: Optional[int]
    name: Optional[str]
    date_of_birth: Optional[date]
    blood_group: Optional[str]
    gender: Optional[str]
    guardian_name: Optional[str]
    address: Optional[str]
    start_date: Optional[date]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    pin_code: Optional[str]
    mobile_number: Optional[str]