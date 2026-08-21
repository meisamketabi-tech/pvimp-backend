from datetime import datetime

from pydantic import BaseModel


class InspectionFollowUpCreate(BaseModel):

    inspection_id: int

    description: str

    followup_date: datetime | None = None


class InspectionFollowUpResponse(BaseModel):

    id: int

    inspection_id: int

    description: str

    followup_date: datetime | None

    created_at: datetime


    class Config:
        from_attributes = True