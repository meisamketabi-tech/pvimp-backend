from pydantic import BaseModel
from typing import Optional


class OrganizationResponsibilityCreate(BaseModel):

    organization_unit_id: int

    inspection_type_id: int

    title: str

    description: Optional[str] = None

    priority: int = 1



class OrganizationResponsibilityResponse(BaseModel):

    id: int

    organization_unit_id: int

    inspection_type_id: int

    title: str

    description: Optional[str] = None

    priority: int

    is_active: bool


    class Config:
        from_attributes = True
