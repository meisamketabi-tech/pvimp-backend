from datetime import datetime

from pydantic import BaseModel


class InspectionVisitResponse(BaseModel):

    id: int

    inspection_id: int

    visitor: str

    visit_time: datetime

    created_at: datetime


    class Config:
        from_attributes = True
