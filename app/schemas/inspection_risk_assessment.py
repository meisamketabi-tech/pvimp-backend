from datetime import datetime

from pydantic import BaseModel


class InspectionRiskAssessmentResponse(BaseModel):

    id: int

    inspection_id: int

    risk_level: str

    description: str

    created_at: datetime


    class Config:
        from_attributes = True
