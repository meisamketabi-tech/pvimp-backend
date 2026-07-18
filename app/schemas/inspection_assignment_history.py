from datetime import datetime

from pydantic import BaseModel


class InspectionAssignmentHistoryResponse(BaseModel):

    id: int

    inspection_id: int

    assigned_from: int

    assigned_to: int

    created_at: datetime


    class Config:
        from_attributes = True
