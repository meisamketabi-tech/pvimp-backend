from pydantic import BaseModel


class InspectionChartResponse(BaseModel):

    id: int

    title: str

    chart_type: str


    class Config:
        from_attributes = True
