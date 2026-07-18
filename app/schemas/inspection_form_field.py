from pydantic import BaseModel


class InspectionFormFieldResponse(BaseModel):

    id: int

    form_id: int

    name: str

    field_type: str


    class Config:
        from_attributes = True
