from datetime import datetime

from pydantic import BaseModel


class InspectionIndicatorResponse(BaseModel):

    id: int

    title: str

    target: str

    created_at: datetime


    class Config:
        from_attributes = True
