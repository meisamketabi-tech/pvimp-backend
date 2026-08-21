from pydantic import BaseModel


class InspectionDepartmentResponse(BaseModel):

    id: int

    name: str

    code: str | None


    class Config:
        from_attributes = True
