from datetime import datetime

from pydantic import BaseModel


class InspectionAttachmentLogResponse(BaseModel):

    id: int

    attachment_id: int

    action: str

    created_at: datetime


    class Config:
        from_attributes = True
