from pydantic import BaseModel


class InspectionSeverityResponse(BaseModel):

    id: int

    title: str

    score: int


    class Config:
        from_attributes = True
