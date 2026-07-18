from datetime import datetime

from pydantic import BaseModel


class InspectionArchiveResponse(BaseModel):

    id: int

    inspection_id: int

    archive_path: str

    created_at: datetime


    class Config:
        from_attributes = True
