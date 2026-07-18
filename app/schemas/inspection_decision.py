from datetime import datetime

from pydantic import BaseModel


class InspectionDecisionResponse(BaseModel):

    id: int

    inspection_id: int

    decision: str

    reason: str

    created_at: datetime


    class Config:
        from_attributes = True
