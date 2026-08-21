from datetime import datetime

from pydantic import BaseModel


class InspectionScheduleCreate(BaseModel):

    inspection_type_id: int

    organization_unit_id: int

    scheduled_date: datetime



class InspectionScheduleResponse(BaseModel):

    id: int

    inspection_type_id: int

    organization_unit_id: int

    scheduled_date: datetime


    class Config:
        from_attributes = True