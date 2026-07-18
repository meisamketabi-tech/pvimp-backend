from datetime import datetime

from pydantic import BaseModel


class InspectionAIAlertResponse(BaseModel):

    id: int

    title: str

    confidence: int

    created_at: datetime


    class Config:
        from_attributes = True
