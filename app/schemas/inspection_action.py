from datetime import datetime

from pydantic import BaseModel


class InspectionActionResponse(BaseModel):

    id: int

    inspection_id: int

    action: str

    created_at: datetime


    class Config:
        from_attributes = True