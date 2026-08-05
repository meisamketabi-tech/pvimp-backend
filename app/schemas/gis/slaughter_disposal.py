from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class GISSlaughterDisposalBase(BaseModel):

    # VCode
    control_action_emha_detail_vcode: str

    control_action_emha_vcode: Optional[str] = None

    # Epidemiology Unit
    epidemiology_unit_id: Optional[int] = None

    epidemiology_unit_code: Optional[str] = None
    epidemiology_unit_name: Optional[str] = None
    epidemiology_unit_type: Optional[str] = None

    old_unit_code: Optional[str] = None

    # Location
    province_code: Optional[str] = None
    province_name: Optional[str] = None

    county_code: Optional[str] = None
    county_name: Optional[str] = None

    # Disease
    disease_id: Optional[int] = None

    disease_name: Optional[str] = None

    # Animal
    animal_type: Optional[str] = None

    # Action Date
    action_date: Optional[date] = None

    # Counts
    total_animals: Optional[int] = 0

    positive_count: Optional[int] = 0

    slaughtered_count: Optional[int] = 0

    destroyed_count: Optional[int] = 0

    dead_count: Optional[int] = 0

    # Compensation
    estimated_compensation: Optional[float] = 0

    # Other
    window_code: Optional[str] = None

    operation_license_type: Optional[str] = None


class GISSlaughterDisposalCreate(
    GISSlaughterDisposalBase
):
    pass


class GISSlaughterDisposalResponse(
    GISSlaughterDisposalBase
):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )