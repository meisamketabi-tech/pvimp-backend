from pydantic import BaseModel


class InspectionRuleResponse(BaseModel):

    id: int

    title: str

    expression: str


    class Config:
        from_attributes = True
