from datetime import date
from pydantic import BaseModel
from typing import Optional


class EpidemiologyUnitBase(BaseModel):

    unit_name: str
    unit_code: str

    old_code: Optional[str] = None
    window_code: Optional[str] = None

    unit_type_id: int

    province_id: Optional[int] = None
    county_id: Optional[int] = None

    parent_unit_id: Optional[int] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None


    user_name: Optional[str] = None
    user_code: Optional[str] = None


    sheep_count: Optional[int] = 0
    cattle_count: Optional[int] = 0
    goat_count: Optional[int] = 0
    horse_count: Optional[int] = 0
    dog_count: Optional[int] = 0
    camel_count: Optional[int] = 0
    buffalo_count: Optional[int] = 0


    postal_code: Optional[str] = None
    address: Optional[str] = None


    sanitary_license_number: Optional[str] = None
    sanitary_license_date: Optional[date] = None


    operation_license_number: Optional[str] = None
    operation_license_date: Optional[date] = None


    license_type: Optional[str] = None

    has_sub_unit: Optional[bool] = False
    is_active: Optional[bool] = True



class EpidemiologyUnitCreate(
    EpidemiologyUnitBase
):
    pass



class EpidemiologyUnitUpdate(
    BaseModel
):

    unit_name: Optional[str] = None
    unit_code: Optional[str] = None

    old_code: Optional[str] = None
    window_code: Optional[str] = None

    unit_type_id: Optional[int] = None

    province_id: Optional[int] = None
    county_id: Optional[int] = None

    parent_unit_id: Optional[int] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None


    user_name: Optional[str] = None
    user_code: Optional[str] = None


    sheep_count: Optional[int] = None
    cattle_count: Optional[int] = None
    goat_count: Optional[int] = None
    horse_count: Optional[int] = None
    dog_count: Optional[int] = None
    camel_count: Optional[int] = None
    buffalo_count: Optional[int] = None


    postal_code: Optional[str] = None
    address: Optional[str] = None


    sanitary_license_number: Optional[str] = None
    sanitary_license_date: Optional[date] = None

    operation_license_number: Optional[str] = None
    operation_license_date: Optional[date] = None


    license_type: Optional[str] = None

    has_sub_unit: Optional[bool] = None
    is_active: Optional[bool] = None



class EpidemiologyUnitResponse(
    EpidemiologyUnitBase
):

    id: int


    class Config:
        from_attributes = True