from pydantic import BaseModel
from datetime import date


class LaboratoryResultBase(BaseModel):

    send_sample_vcode: str | None = None

    answer_no: str | None = None

    answer_date: date | None = None
    sampling_date: date | None = None
    register_date: date | None = None

    epidemiology_unit_id: int | None = None

    epidemiology_unit_code: str | None = None
    epidemiology_unit_name: str | None = None
    epidemiology_unit_type: str | None = None

    province_code: str | None = None
    province_name: str | None = None

    county_code: str | None = None
    county_name: str | None = None

    laboratory_code: str | None = None

    sample_type: str | None = None
    sample_count: int | None = None

    laboratory_name: str | None = None
    laboratory_type: str | None = None
    laboratory_owner: str | None = None

    animal_type: str | None = None

    disease_id: int | None = None
    disease_name: str | None = None

    result_status: str | None = None

    latitude: float | None = None
    longitude: float | None = None

    isolate_name_1: str | None = None
    isolate_name_2: str | None = None

    serotype_a: str | None = None
    serotype_o: str | None = None
    serotype_asia1: str | None = None

    unacceptable_cases: str | None = None


class LaboratoryResultCreate(LaboratoryResultBase):
    pass


class LaboratoryResultResponse(LaboratoryResultBase):

    id: int

    class Config:
        from_attributes = True
