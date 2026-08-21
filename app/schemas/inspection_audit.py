from datetime import datetime

from pydantic import BaseModel


class InspectionAuditResponse(BaseModel):

    id: int

    user_id: int

    action: str

    details: str

    created_at: datetime


    class Config:
        from_attributes = True
