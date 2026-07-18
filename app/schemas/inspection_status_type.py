from pydantic import BaseModel


class InspectionStatusTypeResponse(BaseModel):

    id: int

    title: str

    code: str | None


    class Config:
        from_attributes = True
