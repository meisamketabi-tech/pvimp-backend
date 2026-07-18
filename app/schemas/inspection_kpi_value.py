from datetime import datetime

from pydantic import BaseModel


class InspectionKPIValueResponse(BaseModel):

    id: int

    kpi_id: int

    value: int

    created_at: datetime


    class Config:
        from_attributes = True
