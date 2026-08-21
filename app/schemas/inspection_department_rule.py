from pydantic import BaseModel


class InspectionDepartmentRuleResponse(BaseModel):

    id: int

    department: str

    rule: str


    class Config:
        from_attributes = True
