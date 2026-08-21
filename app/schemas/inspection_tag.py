from pydantic import BaseModel


class InspectionTagResponse(BaseModel):

    id: int

    name: str

    color: str


    class Config:
        from_attributes = True
