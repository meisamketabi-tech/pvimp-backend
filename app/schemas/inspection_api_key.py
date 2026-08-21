from pydantic import BaseModel


class InspectionApiKeyResponse(BaseModel):

    id: int

    name: str

    key_hash: str


    class Config:
        from_attributes = True
