from datetime import datetime

from pydantic import BaseModel


class InspectionDeadlineCreate(BaseModel):

    inspection_id: int

    deadline: datetime


class InspectionDeadlineResponse(BaseModel):

    id: int

    inspection_id: int

    deadline: datetime


    class Config:
        from_attributes = True