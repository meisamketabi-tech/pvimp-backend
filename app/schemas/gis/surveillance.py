from datetime import date
from pydantic import BaseModel


class SurveillanceBase(BaseModel):

    enable_care_detail_vcode: str | None = None
    enable_care_vcode: str | None = None

    province_code: str | None = None
    province_name: str | None = None

    county_code: str | None = None
    county_name: str | None = None

    epidemiology_unit_id: int | None = None
    epidemiology_unit_code: str | None = None
    epidemiology_unit_name: str | None = None
    epidemiology_unit_type: str | None = None

    surveillance_type: str | None = None

    animal_type: str | None = None

    surveillance_date: date | None = None

    total_animals: int | None = None
    positive: int | None = None
    negative: int | None = None
    suspected: int | None = None

    old_system_id: str | None = None

    age_group: str | None = None

    old_unit_code: str | None = None

    window_code: str | None = None

    operation_license_type: str | None = None


class SurveillanceCreate(SurveillanceBase):
    pass


class SurveillanceResponse(SurveillanceBase):

    id: int

    class Config:
        from_attributes = True
