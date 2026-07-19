from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrganizationUnitBase(BaseModel):
    name: str
    code: str
    unit_type: str

    parent_id: Optional[int] = None
    type_id: Optional[int] = None
    level_id: Optional[int] = None
    province_id: Optional[int] = None
    county_id: Optional[int] = None
    description: Optional[str] = None


class OrganizationUnitCreate(OrganizationUnitBase):
    pass


class OrganizationUnitUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    unit_type: Optional[str] = None

    parent_id: Optional[int] = None
    type_id: Optional[int] = None
    level_id: Optional[int] = None
    province_id: Optional[int] = None
    county_id: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class OrganizationUnitRead(OrganizationUnitBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)