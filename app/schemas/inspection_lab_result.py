from datetime import datetime

from pydantic import BaseModel


class InspectionLabResultResponse(BaseModel):

    id: int

    lab_request_id: int

    result: str

    status: str

    created_at: datetime


    class Config:
        from_attributes = True
