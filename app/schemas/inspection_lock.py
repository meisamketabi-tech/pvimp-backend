from datetime import datetime

from pydantic import BaseModel


class InspectionLockResponse(BaseModel):

    id: int

    inspection_id: int

    locked_by: int

    created_at: datetime


    class Config:
        from_attributes = True
