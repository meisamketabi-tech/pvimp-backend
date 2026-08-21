from pydantic import BaseModel


class InspectionLocationCreate(BaseModel):

    inspection_id: int

    address: str

    latitude: str | None = None

    longitude: str | None = None



class InspectionLocationResponse(BaseModel):

    id: int

    inspection_id: int

    address: str

    latitude: str | None = None

    longitude: str | None = None


    class Config:
        from_attributes = True