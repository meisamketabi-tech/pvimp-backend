from pydantic import BaseModel
from datetime import date


class VaccinationPerformanceBase(BaseModel):

    control_action_vaccine_vcode: str | None = None

    epidemiology_unit_id: int | None = None

    province_name: str | None = None
    county_name: str | None = None

    vaccination_date: date | None = None
    registration_date: date | None = None

    animal_type: str | None = None
    vaccine_type: str | None = None

    vaccine_brand: str | None = None
    manufacturer: str | None = None
    batch_number: str | None = None

    total_animals: int | None = None
    vaccinated_animals: int | None = None
    eligible_animals: int | None = None

    age_group: str | None = None
    disease_name: str | None = None

    latitude: float | None = None
    longitude: float | None = None


class VaccinationPerformanceCreate(VaccinationPerformanceBase):
    pass


class VaccinationPerformanceResponse(VaccinationPerformanceBase):

    id: int

    class Config:
        from_attributes = True
