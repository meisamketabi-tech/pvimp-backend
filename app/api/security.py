from fastapi import APIRouter

from app.services.security_service import service


router=APIRouter(
prefix="/security",
tags=["Security"]
)



@router.post("/log")
def log(data:dict):

    return service.log(data)



@router.get("/monitor")
def monitor():

    return service.monitor()
