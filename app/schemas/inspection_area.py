from pydantic import BaseModel


class InspectionAreaResponse(BaseModel):

    id: int

    name: str

    description: str | None


    class Config:
        from_attributes = True
