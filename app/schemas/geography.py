from typing import Optional, List
from pydantic import BaseModel


class GeographicAreaBase(BaseModel):
    parent_id: Optional[int] = None
    code: str
    name: str
    area_type: str
    is_active: bool = True


class GeographicAreaCreate(GeographicAreaBase):
    pass


class GeographicAreaUpdate(BaseModel):
    parent_id: Optional[int] = None
    code: Optional[str] = None
    name: Optional[str] = None
    area_type: Optional[str] = None
    is_active: Optional[bool] = None


class GeographicAreaResponse(GeographicAreaBase):
    id: int

    class Config:
        from_attributes = True


class GeographicTreeResponse(GeographicAreaResponse):
    children: List["GeographicTreeResponse"] = []


GeographicTreeResponse.model_rebuild()