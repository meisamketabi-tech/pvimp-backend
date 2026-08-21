from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class GISSprayingBase(BaseModel):

    spraying_vcode: Optional[str] = None

    province_code: Optional[str] = None
    province_name: Optional[str] = None

    county_code: Optional[str] = None
    county_name: Optional[str] = None

    epidemiology_unit_id: Optional[int] = None

    epidemiology_unit_code: Optional[str] = None
    epidemiology_unit_name: Optional[str] = None
    epidemiology_unit_type: Optional[str] = None

    spraying_date: Optional[date] = None

    plan_type: Optional[str] = None

    operation_type: Optional[str] = None

    poison_type: Optional[str] = None

    sprayed_area: Optional[float] = None

    sprayed_animal_count: Optional[int] = 0

    animal_type: Optional[str] = None

    total_animals: Optional[int] = 0


class GISSprayingCreate(
    GISSprayingBase
):
    pass


class GISSprayingResponse(
    GISSprayingBase
):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )