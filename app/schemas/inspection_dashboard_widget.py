from pydantic import BaseModel


class InspectionDashboardWidgetResponse(BaseModel):

    id: int

    title: str

    widget_type: str


    class Config:
        from_attributes = True
