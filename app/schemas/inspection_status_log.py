from datetime import datetime

from pydantic import BaseModel


class InspectionStatusLogResponse(BaseModel):

    id: int

    inspection_id: int

    status: str

    created_at: datetime


    class Config:
        from_attributes = True
