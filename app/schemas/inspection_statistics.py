from datetime import datetime

from pydantic import BaseModel


class InspectionStatisticsResponse(BaseModel):

    id: int

    metric: str

    value: int

    created_at: datetime


    class Config:
        from_attributes = True
