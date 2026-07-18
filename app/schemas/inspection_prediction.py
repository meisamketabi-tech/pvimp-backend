from datetime import datetime

from pydantic import BaseModel


class InspectionPredictionResponse(BaseModel):

    id: int

    subject: str

    prediction: str

    created_at: datetime


    class Config:
        from_attributes = True
