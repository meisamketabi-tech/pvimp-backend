from datetime import datetime

from pydantic import BaseModel


class InspectionSampleCreate(BaseModel):

    inspection_id: int

    sample_code: str

    sample_type: str


class InspectionSampleResponse(BaseModel):

    id: int

    inspection_id: int

    sample_code: str

    sample_type: str

    created_at: datetime


    class Config:
        from_attributes = True
