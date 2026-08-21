from pydantic import BaseModel


class InspectionQuestionResponse(BaseModel):

    id: int

    checklist_id: int

    text: str


    class Config:
        from_attributes = True
