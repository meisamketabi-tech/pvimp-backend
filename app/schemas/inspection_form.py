from pydantic import BaseModel


class InspectionFormResponse(BaseModel):

    id: int

    title: str

    version: str


    class Config:
        from_attributes = True
