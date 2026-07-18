from pydantic import BaseModel


class InspectionChecklistCategoryResponse(BaseModel):

    id: int

    title: str

    code: str | None


    class Config:
        from_attributes = True
