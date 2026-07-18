from pydantic import BaseModel


class InspectionKPIResponse(BaseModel):

    id: int

    name: str

    formula: str


    class Config:
        from_attributes = True
