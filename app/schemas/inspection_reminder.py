from datetime import datetime

from pydantic import BaseModel


class InspectionReminderResponse(BaseModel):

    id: int

    inspection_id: int

    message: str

    remind_at: datetime

    created_at: datetime


    class Config:
        from_attributes = True
