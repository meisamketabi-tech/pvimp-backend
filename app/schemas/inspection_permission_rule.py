from pydantic import BaseModel


class InspectionPermissionRuleResponse(BaseModel):

    id: int

    role: str

    permission: str


    class Config:
        from_attributes = True
