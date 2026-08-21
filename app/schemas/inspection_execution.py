from datetime import datetime

from pydantic import BaseModel


class InspectionExecutionResponse(BaseModel):

    id: int

    inspection_id: int

    executor_id: int

    started_at: datetime | None

    finished_at: datetime | None

    created_at: datetime


    class Config:
        from_attributes = True
