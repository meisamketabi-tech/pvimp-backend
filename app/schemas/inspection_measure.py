from pydantic import BaseModel


class InspectionMeasureResponse(BaseModel):

    id: int

    title: str

    unit: str


    class Config:
        from_attributes = True
