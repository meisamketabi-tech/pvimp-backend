from datetime import datetime

from pydantic import BaseModel


class InspectionAttachmentCreate(BaseModel):

    inspection_id: int

    file_name: str

    file_path: str

    description: str | None = None



class InspectionAttachmentResponse(BaseModel):

    id: int

    inspection_id: int

    file_name: str

    file_path: str

    description: str | None = None

    uploaded_at: datetime


    class Config:
        from_attributes = True