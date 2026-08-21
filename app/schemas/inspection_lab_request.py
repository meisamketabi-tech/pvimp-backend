from datetime import datetime

from pydantic import BaseModel


class InspectionLabRequestResponse(BaseModel):

    id: int

    sample_id: int

    status: str

    created_at: datetime


    class Config:
        from_attributes = True
