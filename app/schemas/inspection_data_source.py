from datetime import datetime

from pydantic import BaseModel


class InspectionDataSourceResponse(BaseModel):

    id: int

    name: str

    connection_type: str

    created_at: datetime


    class Config:
        from_attributes = True
