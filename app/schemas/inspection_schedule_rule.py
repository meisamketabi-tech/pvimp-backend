from datetime import datetime

from pydantic import BaseModel


class InspectionScheduleRuleResponse(BaseModel):

    id: int

    title: str

    interval_days: int

    created_at: datetime


    class Config:
        from_attributes = True
