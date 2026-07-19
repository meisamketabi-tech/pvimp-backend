from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InspectionAssignmentCreate(BaseModel):

    inspection_id: int

    inspector_id: int

    note: Optional[str] = None


class InspectionAssignmentResponse(BaseModel):

    id: int

    inspection_id: int

    inspector_id: int

    assigned_at: datetime

    is_active: bool

    class Config:
        from_attributes = True
