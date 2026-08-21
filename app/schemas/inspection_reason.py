from pydantic import BaseModel


class InspectionReasonResponse(BaseModel):

    id: int

    title: str

    category: str


    class Config:
        from_attributes = True
