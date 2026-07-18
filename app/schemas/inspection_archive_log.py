from datetime import datetime

from pydantic import BaseModel


class InspectionArchiveLogResponse(BaseModel):

    id: int

    archive_id: int

    action: str

    created_at: datetime


    class Config:
        from_attributes = True
