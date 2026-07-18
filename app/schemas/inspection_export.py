from datetime import datetime

from pydantic import BaseModel


class InspectionExportResponse(BaseModel):

    id: int

    format: str

    file_path: str

    created_at: datetime


    class Config:
        from_attributes = True
