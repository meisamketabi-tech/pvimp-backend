from pydantic import BaseModel


class InspectionResultTypeResponse(BaseModel):

    id: int

    title: str

    code: str | None


    class Config:
        from_attributes = True
