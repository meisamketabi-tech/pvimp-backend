from datetime import datetime

from pydantic import BaseModel


class InspectionCommunicationResponse(BaseModel):

    id: int

    inspection_id: int

    receiver: str

    message: str

    created_at: datetime


    class Config:
        from_attributes = True
