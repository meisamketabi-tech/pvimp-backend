from datetime import datetime

from pydantic import BaseModel


class InspectionAlertResponse(BaseModel):

    id: int

    title: str

    severity: str

    created_at: datetime


    class Config:
        from_attributes = True
