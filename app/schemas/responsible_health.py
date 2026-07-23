
from pydantic import BaseModel
from typing import Optional
from datetime import date


class OfficerCreate(BaseModel):
    full_name:str
    national_code:Optional[str]=None
    veterinary_system_code:Optional[str]=None
    license_number:Optional[str]=None
    unit_name:Optional[str]=None
    unit_type:Optional[str]=None
    status:Optional[str]="فعال"



class InspectionCreate(BaseModel):
    officer_id:int
    inspection_date:date
    employee_status:Optional[str]=None
    building_status:Optional[str]=None
    description:Optional[str]=None



class NonConformityCreate(BaseModel):
    officer_id:int
    title:str
    level:str
    description:Optional[str]=None
    corrective_action:Optional[str]=None



class CorrectiveActionCreate(BaseModel):
    nonconformity_id:int
    root_cause:Optional[str]=None
    action:Optional[str]=None
    executor:Optional[str]=None



class SamplingCreate(BaseModel):
    product_name:str
    sample_type:str
    batch_number:Optional[str]=None
    laboratory:Optional[str]=None
    result:Optional[str]=None



class ColdChainCreate(BaseModel):
    location:str
    temperature:str
    status:str



class DocumentControlCreate(BaseModel):
    document_type:str
    status:str
    description:Optional[str]=None
