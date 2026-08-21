from pydantic import BaseModel


class InspectionWorkflowResponse(BaseModel):

    id: int

    name: str

    description: str | None


    class Config:
        from_attributes = True
