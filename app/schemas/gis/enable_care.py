from datetime import date

from pydantic import BaseModel, ConfigDict


class GISEnableCareBase(BaseModel):

    enable_care_detail_vcode: str | None = None

    enable_care_vcode: str | None = None


    # Geography
    province_code: str | None = None
    province_name: str | None = None

    county_code: str | None = None
    county_name: str | None = None


    # Epidemiology Unit
    epidemiology_unit_id: int | None = None

    epidemiology_unit_code: str | None = None

    epidemiology_unit_name: str | None = None

    epidemiology_unit_type: str | None = None


    # Care
    care_type: str | None = None

    animal_type: str | None = None

    care_date: date | None = None


    # Statistics
    total_animals: int | None = 0

    positive_count: int | None = 0

    negative_count: int | None = 0

    suspicious_count: int | None = 0


    # Legacy system
    old_system_id: str | None = None

    age_group: str | None = None

    old_unit_code: str | None = None


    window_code: str | None = None

    operation_license_type: str | None = None



class GISEnableCareCreate(
    GISEnableCareBase
):
    pass



class GISEnableCareResponse(
    GISEnableCareBase
):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )