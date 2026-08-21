from datetime import datetime

from pydantic import BaseModel


class InspectionReportTemplateResponse(BaseModel):

    id: int

    title: str

    layout: str

    created_at: datetime


    class Config:
        from_attributes = True
