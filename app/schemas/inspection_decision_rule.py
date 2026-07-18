from pydantic import BaseModel


class InspectionDecisionRuleResponse(BaseModel):

    id: int

    condition: str

    decision: str


    class Config:
        from_attributes = True
