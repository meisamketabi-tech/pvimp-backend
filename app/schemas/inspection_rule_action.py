from pydantic import BaseModel


class InspectionRuleActionResponse(BaseModel):

    id: int

    rule_id: int

    action: str


    class Config:
        from_attributes = True
