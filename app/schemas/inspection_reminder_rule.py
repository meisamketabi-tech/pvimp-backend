from datetime import datetime

from pydantic import BaseModel


class InspectionReminderRuleResponse(BaseModel):

    id: int

    title: str

    days_before: int

    created_at: datetime


    class Config:
        from_attributes = True
