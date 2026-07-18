from datetime import datetime

from pydantic import BaseModel


class InspectionEvidenceCreate(BaseModel):

    inspection_id: int

    evidence_type: str

    file_path: str



class InspectionEvidenceResponse(BaseModel):

    id: int

    inspection_id: int

    evidence_type: str

    file_path: str

    created_at: datetime


    class Config:
        from_attributes = True