from pydantic import BaseModel


class InspectionMetricResponse(BaseModel):

    id: int

    name: str

    value: str


    class Config:
        from_attributes = True
