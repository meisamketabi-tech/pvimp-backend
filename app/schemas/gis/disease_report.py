from pydantic import BaseModel, ConfigDict
from datetime import date


class DiseaseReportBase(BaseModel):

    observation_detail_vcode: str | None = None
    observation_vcode: str | None = None

    epidemiology_unit_id: int | None = None
    disease_id: int | None = None

    province_code: str | None = None
    province_name: str | None = None

    county_code: str | None = None
    county_name: str | None = None

    epidemiology_unit_code: str | None = None
    epidemiology_unit_name: str | None = None
    epidemiology_unit_type: str | None = None

    disease_name: str | None = None

    animal_type: str | None = None

    disease_start_date: date | None = None

    total_animals: int | None = None

    infected_count: int | None = None

    death_count: int | None = None

    slaughtered_count: int | None = None

    destroyed_count: int | None = None

    sampling: str | None = None

    old_system_id: str | None = None

    old_unit_code: str | None = None

    age_group: str | None = None

    biting_animal: str | None = None

    operation_license_type: str | None = None

    creator_user_code: str | None = None

    creator_user_name: str | None = None

    source_unit_code: str | None = None

    source_unit_name: str | None = None

    source_unit_type: str | None = None


class DiseaseReportCreate(DiseaseReportBase):
    pass


class DiseaseReportResponse(
    DiseaseReportBase
):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )