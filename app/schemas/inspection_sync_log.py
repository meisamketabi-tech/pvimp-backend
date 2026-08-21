from pydantic import BaseModel
from datetime import datetime


class InspectionSyncLogResponse(BaseModel):

    id: int

    source: str

    status: str

    created_at: datetime


    class Config:
        from_attributes = True
