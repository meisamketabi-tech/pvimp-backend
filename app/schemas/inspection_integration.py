from datetime import datetime

from pydantic import BaseModel


class InspectionIntegrationResponse(BaseModel):

    id: int

    name: str

    endpoint: str

    created_at: datetime


    class Config:
        from_attributes = True
