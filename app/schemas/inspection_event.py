from datetime import datetime

from pydantic import BaseModel


class InspectionEventResponse(BaseModel):

    id: int

    inspection_id: int

    event_type: str

    description: str

    created_at: datetime


    class Config:
        from_attributes = True
