from pydantic import BaseModel


class InspectionAssignmentCreate(BaseModel):

    inspection_id: int

    inspector_id: int


class InspectionAssignmentResponse(BaseModel):

    id: int

    inspection_id: int

    inspector_id: int


    class Config:
        from_attributes = True