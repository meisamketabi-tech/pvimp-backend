from fastapi import APIRouter

from app.services.disease_service import service


router=APIRouter(
prefix="/diseases",
tags=["Diseases"]
)



@router.post("/register")
def register(data:dict):

    return service.register(data)



@router.get("/")
def list():

    return service.list()
