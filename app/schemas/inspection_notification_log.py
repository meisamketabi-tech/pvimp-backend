from datetime import datetime

from pydantic import BaseModel


class InspectionNotificationLogResponse(BaseModel):

    id: int

    recipient: str

    message: str

    created_at: datetime


    class Config:
        from_attributes = True
