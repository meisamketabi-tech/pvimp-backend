from pydantic import BaseModel
from datetime import date


class DiseaseOccurrenceBase(BaseModel):

    observation_detail_vcode: str | None = None
    observation_vcode: str | None = None

    province_id: int | None = None
    county_id: int | None = None

    province_name: str | None = None
    county_name: str | None = None

    epidemiology_unit_id: int | None = None
    epidemiology_unit_code: str | None = None
    epidemiology_unit_name: str | None = None
    epidemiology_unit_type: str | None = None

    disease_id: int | None = None
    disease_name: str | None = None

    animal_type: str | None = None

    start_date: date | None = None
    report_date: date | None = None

    animal_count: int | None = None
    exposed_count: int | None = None
    infected_count: int | None = None
    dead_count: int | None = None
    slaughtered_count: int | None = None
    total_animals: int | None = None

    sample_taken: bool | None = False

    report_number: str | None = None
    report_info: str | None = None

    latitude: float | None = None
    longitude: float | None = None

    user_name: str | None = None
    user_code: str | None = None

    expert_names: str | None = None

    status: str | None = None

    window_code: str | None = None

    operation_license_type: str | None = None

    old_system_id: str | None = None

    description: str | None = None


class DiseaseOccurrenceCreate(DiseaseOccurrenceBase):
    pass


class DiseaseOccurrenceResponse(DiseaseOccurrenceBase):
    id: int

    class Config:
        from_attributes = True
