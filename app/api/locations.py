from fastapi import APIRouter

from app.services.location_service import service


router=APIRouter(
prefix="/locations",
tags=["Locations"]
)



@router.post("/")
def create(data:dict):

    return service.create(data)



@router.get("/")
def locations():

    return service.list()
