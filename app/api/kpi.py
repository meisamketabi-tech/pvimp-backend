from fastapi import APIRouter

from app.services.kpi_service import service


router=APIRouter(
prefix="/kpi",
tags=["KPI"]
)



@router.post("/calculate")
def calculate(data:dict):

    return service.calculate(data)



@router.get("/dashboard")
def dashboard():

    return service.dashboard()
