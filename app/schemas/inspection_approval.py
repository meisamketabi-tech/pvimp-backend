from datetime import datetime

from pydantic import BaseModel


class InspectionApprovalResponse(BaseModel):

    id: int

    inspection_id: int

    approved_by: int

    status: str

    created_at: datetime


    class Config:
        from_attributes = True
