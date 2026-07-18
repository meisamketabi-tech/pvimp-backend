from datetime import datetime

from pydantic import BaseModel


class InspectionQueueResponse(BaseModel):

    id: int

    inspection_id: int

    priority: int

    created_at: datetime


    class Config:
        from_attributes = True
