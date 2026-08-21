from pydantic import BaseModel


class InspectionPriorityRuleResponse(BaseModel):

    id: int

    name: str

    weight: int


    class Config:
        from_attributes = True
