from pydantic import BaseModel


class InspectionChecklistVersionResponse(BaseModel):

    id: int

    checklist_id: int

    version: str


    class Config:
        from_attributes = True
