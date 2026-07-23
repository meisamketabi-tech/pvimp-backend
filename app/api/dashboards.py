from fastapi import APIRouter

from app.services.dashboard_service import service


router=APIRouter(
prefix="/dashboards",
tags=["Dashboards"]
)



@router.post("/")
def create(data:dict):

    return service.create(data)



@router.get("/{role}")
def load(role:str):

    return service.load(role)
