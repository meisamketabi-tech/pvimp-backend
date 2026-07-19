from typing import Optional

from pydantic import BaseModel


class AssignmentCreate(BaseModel):
    user_id: int
    organization_unit_id: int
    organization_unit_position_id: Optional[int] = None
    role_id: int
    is_primary: bool = False


class AssignmentRead(BaseModel):
    id: int
    user_id: int
    organization_unit_id: int
    organization_unit_position_id: Optional[int]
    role_id: int
    is_primary: bool
    is_active: bool

    model_config = {
        "from_attributes": True
    }
