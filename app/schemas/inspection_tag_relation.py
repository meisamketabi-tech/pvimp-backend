from pydantic import BaseModel


class InspectionTagRelationResponse(BaseModel):

    id: int

    inspection_id: int

    tag_id: int


    class Config:
        from_attributes = True
