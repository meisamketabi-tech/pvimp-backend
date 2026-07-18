from pydantic import BaseModel


class InspectionExportTemplateResponse(BaseModel):

    id: int

    title: str

    format: str


    class Config:
        from_attributes = True
