from datetime import datetime

from pydantic import BaseModel


class InspectionHistoryNoteResponse(BaseModel):

    id: int

    inspection_id: int

    note: str

    created_at: datetime


    class Config:
        from_attributes = True
