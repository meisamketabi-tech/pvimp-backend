from pydantic import BaseModel


class InspectionOutcomeResponse(BaseModel):

    id: int

    title: str

    code: str | None


    class Config:
        from_attributes = True
