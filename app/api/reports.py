from fastapi import APIRouter

from app.services.report_service import service


router=APIRouter(
prefix="/reports",
tags=["Reports"]
)



@router.post("/generate")
def generate(data:dict):

    return service.generate(data)



@router.get("/")
def reports():

    return service.list_reports()
