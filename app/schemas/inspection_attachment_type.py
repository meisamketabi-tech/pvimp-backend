from datetime import datetime

from pydantic import BaseModel


class InspectionAttachmentTypeResponse(BaseModel):

    id: int

    title: str

    extension: str

    created_at: datetime


    class Config:
        from_attributes = True
