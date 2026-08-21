from datetime import date

from pydantic import BaseModel, ConfigDict


class DiseaseOccurrenceBase(BaseModel):

    # =========================
    # شناسه‌های فرم
    # =========================

    observation_detail_vcode: str | None = None
    observation_vcode: str | None = None

    # =========================
    # Geography
    # =========================

    province_id: int | None = None
    county_id: int | None = None

    province_code: str | None = None
    province_name: str | None = None

    county_code: str | None = None
    county_name: str | None = None

    # =========================
    # Epidemiology Unit
    # =========================

    epidemiology_unit_id: int | None = None
    epidemiology_unit_code: str | None = None
    epidemiology_unit_name: str | None = None
    epidemiology_unit_type: str | None = None

    # =========================
    # Disease
    # =========================

    disease_id: int | None = None
    disease_name: str | None = None

    # =========================
    # Animal
    # =========================

    animal_type: str | None = None

    # =========================
    # Dates
    # =========================

    start_date: date | None = None
    report_date: date | None = None
    registration_date: date | None = None

    # =========================
    # Animal Statistics
    # =========================

    animal_count: int | None = None
    exposed_count: int | None = None
    infected_count: int | None = None
    dead_count: int | None = None
    slaughtered_count: int | None = None
    total_animals: int | None = None

    # =========================
    # Sampling
    # =========================

    sample_taken: bool | None = False

    # =========================
    # Report
    # =========================

    report_number: str | None = None
    report_info: str | None = None

    # =========================
    # Coordinates
    # =========================

    latitude: float | None = None
    longitude: float | None = None

    # =========================
    # User
    # =========================

    user_name: str | None = None
    user_code: str | None = None

    expert_names: str | None = None

    # =========================
    # System
    # =========================

    status: str | None = None

    window_code: str | None = None

    operation_license_type: str | None = None

    old_system_id: str | None = None

    description: str | None = None


class DiseaseOccurrenceCreate(DiseaseOccurrenceBase):
    pass


class DiseaseOccurrenceResponse(DiseaseOccurrenceBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
