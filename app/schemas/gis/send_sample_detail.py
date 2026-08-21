from pydantic import BaseModel
from datetime import date


class SendSampleDetailBase(BaseModel):

    send_sample_detail_vcode: str | None = None

    send_sample_vcode: str | None = None


    province_code: str | None = None
    province_name: str | None = None

    county_code: str | None = None
    county_name: str | None = None


    epidemiology_unit_id: int | None = None

    epidemiology_unit_code: str | None = None

    epidemiology_unit_name: str | None = None

    epidemiology_unit_type: str | None = None


    disease_id: int | None = None

    disease_name: str | None = None


    animal_type: str | None = None

    sample_type: str | None = None

    sample_count: int | None = None


    sampling_date: date | None = None


    result_status: str | None = None



class SendSampleDetailCreate(
    SendSampleDetailBase
):
    pass



class SendSampleDetailResponse(
    SendSampleDetailBase
):

    id: int


    class Config:
        from_attributes = True