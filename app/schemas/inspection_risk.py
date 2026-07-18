from pydantic import BaseModel


class InspectionRiskResponse(BaseModel):

    id: int

    title: str

    level: int


    class Config:
        from_attributes = True
