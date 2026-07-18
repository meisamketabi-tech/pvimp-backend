from datetime import datetime

from pydantic import BaseModel


class InspectionNotificationResponse(BaseModel):

    id: int

    inspection_id: int

    message: str

    created_at: datetime


    class Config:
        from_attributes = True