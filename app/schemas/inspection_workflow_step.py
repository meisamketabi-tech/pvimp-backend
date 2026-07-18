from pydantic import BaseModel


class InspectionWorkflowStepResponse(BaseModel):

    id: int

    workflow_id: int

    title: str

    status: str


    class Config:
        from_attributes = True
