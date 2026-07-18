from datetime import datetime

from pydantic import BaseModel


class InspectionAnswerResponse(BaseModel):

    id: int

    question_id: int

    inspection_id: int

    answer: str

    created_at: datetime


    class Config:
        from_attributes = True
