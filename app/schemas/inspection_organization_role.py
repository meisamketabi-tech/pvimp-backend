from pydantic import BaseModel


class InspectionOrganizationRoleResponse(BaseModel):

    id: int

    name: str

    permission: str


    class Config:
        from_attributes = True
