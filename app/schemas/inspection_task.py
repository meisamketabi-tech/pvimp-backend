from datetime import datetime

from pydantic import BaseModel


class InspectionTaskResponse(BaseModel):

    id: int

    inspection_id: int

    title: str

    assigned_to: int

    status: str

    created_at: datetime


    class Config:
        from_attributes = True
