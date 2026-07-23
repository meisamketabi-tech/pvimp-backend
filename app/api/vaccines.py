from fastapi import APIRouter

from app.services.vaccine_service import service


router=APIRouter(
prefix="/vaccines",
tags=["Vaccines"]
)



@router.post("/register")
def register(data:dict):

    return service.register(data)



@router.get("/inventory")
def inventory():

    return service.inventory()
