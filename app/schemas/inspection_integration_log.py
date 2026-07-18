from datetime import datetime

from pydantic import BaseModel


class InspectionIntegrationLogResponse(BaseModel):

    id: int

    system_name: str

    action: str

    created_at: datetime


    class Config:
        from_attributes = True
