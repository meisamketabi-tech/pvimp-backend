from datetime import datetime

from pydantic import BaseModel


class InspectionEscalationResponse(BaseModel):

    id: int

    inspection_id: int

    level: int

    reason: str

    created_at: datetime


    class Config:
        from_attributes = True
