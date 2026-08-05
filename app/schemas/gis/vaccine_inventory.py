from pydantic import BaseModel
from datetime import date


class VaccineInventoryBase(BaseModel):

    distribution_vaccine_center_vcode: str | None = None

    epidemiology_unit_id: int | None = None

    province_name: str | None = None

    county_name: str | None = None


    epidemiology_unit_type: str | None = None

    epidemiology_unit_code: str | None = None

    epidemiology_unit_name: str | None = None


    user_code: str | None = None

    user_name: str | None = None


    distribution_no: str | None = None

    distribution_date: date | None = None


    vaccine_type: str | None = None

    vaccine_brand: str | None = None

    manufacturer: str | None = None

    batch_number: str | None = None


    vaccine_shape: str | None = None


    package_count: int | None = None

    dose_volume: float | None = None


    unit_name: str | None = None


    registration_date: date | None = None


    production_import_date: date | None = None

    expiration_date: date | None = None



class VaccineInventoryCreate(
    VaccineInventoryBase
):
    pass



class VaccineInventoryResponse(
    VaccineInventoryBase
):

    id: int


    class Config:
        from_attributes = True