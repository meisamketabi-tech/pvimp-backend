from pydantic import BaseModel


class InspectionDocumentTypeResponse(BaseModel):

    id: int

    title: str

    code: str | None


    class Config:
        from_attributes = True
