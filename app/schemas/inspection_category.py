from pydantic import BaseModel


class InspectionCategoryResponse(BaseModel):

    id: int

    name: str

    code: str | None


    class Config:
        from_attributes = True
