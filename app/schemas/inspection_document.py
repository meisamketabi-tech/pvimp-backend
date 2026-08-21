from datetime import datetime

from pydantic import BaseModel


class InspectionDocumentResponse(BaseModel):

    id: int

    inspection_id: int

    path: str

    created_at: datetime


    class Config:
        from_attributes = True
