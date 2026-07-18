from datetime import datetime

from pydantic import BaseModel


class InspectionAIModelResponse(BaseModel):

    id: int

    name: str

    version: str

    created_at: datetime


    class Config:
        from_attributes = True
