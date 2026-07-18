from pydantic import BaseModel


class InspectionTypeRuleResponse(BaseModel):

    id: int

    inspection_type: str

    rule_text: str


    class Config:
        from_attributes = True
