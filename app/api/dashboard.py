from fastapi import APIRouter

from app.services.dashboard_service import service


router=APIRouter(
prefix="/dashboard",
tags=["Dashboard"]
)



@router.post("/build")
def build(data:dict):

    return service.build(data)



@router.get("/")
def default():

    return service.build({})
