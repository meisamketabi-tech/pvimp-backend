from pydantic import BaseModel


class InspectionSourceResponse(BaseModel):

    id: int

    title: str

    type: str


    class Config:
        from_attributes = True
