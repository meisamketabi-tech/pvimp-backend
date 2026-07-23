from fastapi import APIRouter

from app.services.alert_service import service


router=APIRouter(
prefix="/alerts",
tags=["Alerts"]
)



@router.post("/")
def create(data:dict):

    return service.create(data)



@router.get("/")
def active():

    return service.active()



@router.post("/{id}/resolve")
def resolve(id:int):

    return service.resolve(id)
