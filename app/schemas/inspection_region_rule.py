from pydantic import BaseModel


class InspectionRegionRuleResponse(BaseModel):

    id: int

    region: str

    rule: str


    class Config:
        from_attributes = True
