from datetime import datetime

from pydantic import BaseModel


class InspectionViolationActionResponse(BaseModel):

    id: int

    violation_id: int

    action: str

    created_at: datetime


    class Config:
        from_attributes = True
