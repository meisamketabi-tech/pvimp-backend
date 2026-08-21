from datetime import datetime

from pydantic import BaseModel


class InspectionPlanResponse(BaseModel):

    id: int

    title: str

    description: str | None

    start_date: datetime

    end_date: datetime

    created_at: datetime


    class Config:
        from_attributes = True
