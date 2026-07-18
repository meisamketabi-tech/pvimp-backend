from datetime import datetime

from pydantic import BaseModel


class InspectionTemplateVersionResponse(BaseModel):

    id: int

    template_id: int

    version: str

    created_at: datetime


    class Config:
        from_attributes = True
