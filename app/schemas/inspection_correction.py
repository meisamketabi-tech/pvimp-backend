from datetime import datetime

from pydantic import BaseModel


class InspectionCorrectionResponse(BaseModel):

    id: int

    inspection_id: int

    description: str

    created_at: datetime


    class Config:
        from_attributes = True
