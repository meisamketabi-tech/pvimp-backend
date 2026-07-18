from pydantic import BaseModel


class InspectionScoreResponse(BaseModel):

    id: int

    inspection_id: int

    total_score: int

    max_score: int


    class Config:
        from_attributes = True