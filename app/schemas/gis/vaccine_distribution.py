from pydantic import BaseModel
from datetime import date


class VaccineDistributionBase(BaseModel):

    distribution_vaccine_center_vcode: str | None = None

    epidemiology_unit_id: int | None = None

    province_name: str | None = None
    county_name: str | None = None

    distribution_date: date | None = None

    distribution_status_id: int | None = None

    destination_province: str | None = None
    destination_county: str | None = None

    destination_unit_code: str | None = None
    destination_unit_name: str | None = None
    destination_unit_type: str | None = None

    vaccine_type: str | None = None
    vaccine_brand: str | None = None
    manufacturer: str | None = None

    batch_number: str | None = None

    vaccine_shape: str | None = None

    package_count: int | None = None
    dose_volume: float | None = None

    unit_name: str | None = None

    user_code: str | None = None
    user_name: str | None = None

    registration_date: date | None = None


class VaccineDistributionCreate(
    VaccineDistributionBase
):
    pass


class VaccineDistributionResponse(
    VaccineDistributionBase
):

    id: int

    class Config:
        from_attributes = True