from datetime import datetime

from pydantic import BaseModel


class InspectionCalendarResponse(BaseModel):

    id: int

    title: str

    schedule_date: datetime

    created_at: datetime


    class Config:
        from_attributes = True
