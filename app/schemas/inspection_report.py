from pydantic import BaseModel


class InspectionStatisticsResponse(BaseModel):

    total: int
    completed: int