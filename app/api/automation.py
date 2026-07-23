from fastapi import APIRouter

from app.services.automation_service import service


router=APIRouter(
prefix="/automation",
tags=["Automation"]
)



@router.post("/schedule-report")
def schedule(data:dict):

    return service.schedule_report(data)



@router.post("/execute")
def execute(data:dict):

    return service.execute(data)
