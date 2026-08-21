from pydantic import BaseModel


class InspectionTemplateCreate(BaseModel):

    title: str

    description: str | None = None



class InspectionTemplateResponse(BaseModel):

    id: int

    title: str

    description: str | None = None


    class Config:
        from_attributes = True