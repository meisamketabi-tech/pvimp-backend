from datetime import datetime

from pydantic import BaseModel


class InspectionViolationCreate(BaseModel):

    inspection_id: int

    description: str



class InspectionViolationResponse(BaseModel):

    id: int

    inspection_id: int

    description: str

    created_at: datetime


    class Config:
        from_attributes = True