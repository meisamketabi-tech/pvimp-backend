from fastapi import APIRouter

from app.services.complaint_workflow import engine


router=APIRouter(
prefix="/complaint-workflow",
tags=["Complaint Workflow"]
)



@router.post("/process")
def process(data:dict):

    return engine.process(data)
