from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.db.models.inspection import (
    InspectionStatusEnum,
    InspectionResultEnum,
)


# -------------------------
# Inspection Type
# -------------------------

class InspectionTypeBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_active: bool = True


class InspectionTypeCreate(InspectionTypeBase):
    pass


class InspectionTypeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class InspectionTypeResponse(InspectionTypeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------------
# Checklist Item
# -------------------------

class ChecklistItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    weight: int = 1
    is_required: bool = True


class ChecklistItemCreate(ChecklistItemBase):
    pass


class ChecklistItemResponse(ChecklistItemBase):
    id: int

    class Config:
        from_attributes = True


# -------------------------
# Checklist
# -------------------------

class ChecklistBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_active: bool = True


class ChecklistCreate(ChecklistBase):
    inspection_type_id: int
    items: List[ChecklistItemCreate] = []


class ChecklistResponse(ChecklistBase):
    id: int
    inspection_type_id: int
    items: List[ChecklistItemResponse] = []

    class Config:
        from_attributes = True


# -------------------------
# Inspection Item Result
# -------------------------

class InspectionItemResultCreate(BaseModel):
    checklist_item_id: int
    is_compliant: bool
    score: Optional[int] = None
    inspector_note: Optional[str] = None


class InspectionItemResultResponse(BaseModel):
    id: int
    checklist_item_id: int
    is_compliant: bool
    score: Optional[int] = None
    inspector_note: Optional[str] = None

    class Config:
        from_attributes = True


# -------------------------
# Inspection
# -------------------------

class InspectionBase(BaseModel):
    inspection_type_id: int
    organization_unit_id: int
    inspector_id: int
    inspection_date: datetime
    notes: Optional[str] = None


class InspectionCreate(InspectionBase):
    items_result: List[InspectionItemResultCreate] = []


class InspectionUpdate(BaseModel):
    status: Optional[InspectionStatusEnum] = None
    result: Optional[InspectionResultEnum] = None
    notes: Optional[str] = None


class InspectionResponse(InspectionBase):
    id: int
    inspection_number: str
    status: InspectionStatusEnum
    result: InspectionResultEnum
    created_at: datetime
    updated_at: datetime

    items_result: List[InspectionItemResultResponse] = []

    class Config:
        from_attributes = True