from datetime import datetime

from pydantic import BaseModel


class InspectionCommentCreate(BaseModel):

    inspection_id: int

    comment: str



class InspectionCommentResponse(BaseModel):

    id: int

    inspection_id: int

    comment: str

    created_at: datetime


    class Config:
        from_attributes = True