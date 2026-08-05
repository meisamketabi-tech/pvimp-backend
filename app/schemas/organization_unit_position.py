from pydantic import BaseModel, ConfigDict
from typing import Optional


class OrganizationUnitPositionCreate(BaseModel):
    organization_unit_id: int
    organization_position_id: int
    parent_assignment_id: Optional[int] = None


class OrganizationUnitPositionRead(BaseModel):
    id: int
    organization_unit_id: int
    organization_position_id: int
    parent_assignment_id: Optional[int] = None
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )
