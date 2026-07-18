from datetime import datetime

from pydantic import BaseModel


class InspectionReviewResponse(BaseModel):

    id: int

    inspection_id: int

    reviewer_id: int | None

    comment: str

    created_at: datetime


    class Config:
        from_attributes = True
