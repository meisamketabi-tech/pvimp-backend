from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProvinceBase(BaseModel):
    name: str
    code: str
    is_active: bool = True


class ProvinceCreate(ProvinceBase):
    pass


class ProvinceUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    is_active: Optional[bool] = None


class ProvinceRead(ProvinceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CountyBase(BaseModel):
    province_id: int
    name: str
    code: str
    is_active: bool = True


class CountyCreate(CountyBase):
    pass


class CountyUpdate(BaseModel):
    province_id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    is_active: Optional[bool] = None


class CountyRead(CountyBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class VeterinaryUnitBase(BaseModel):
    county_id: int
    name: str
    code: str
    unit_type: str
    is_active: bool = True


class VeterinaryUnitCreate(VeterinaryUnitBase):
    pass


class VeterinaryUnitUpdate(BaseModel):
    county_id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    unit_type: Optional[str] = None
    is_active: Optional[bool] = None


class VeterinaryUnitRead(VeterinaryUnitBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
