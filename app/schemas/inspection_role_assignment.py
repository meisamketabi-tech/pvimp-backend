from pydantic import BaseModel


class InspectionRoleAssignmentResponse(BaseModel):

    id: int

    role: str

    description: str


    class Config:
        from_attributes = True
