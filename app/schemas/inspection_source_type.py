from pydantic import BaseModel


class InspectionSourceTypeResponse(BaseModel):

    id: int

    name: str

    code: str | None


    class Config:
        from_attributes = True
