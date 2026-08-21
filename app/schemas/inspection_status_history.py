from pydantic import BaseModel


class InspectionStatusHistoryResponse(BaseModel):

    id: int

    inspection_id: int

    old_status: str

    new_status: str


    class Config:
        from_attributes = True
