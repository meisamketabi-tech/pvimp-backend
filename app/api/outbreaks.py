from fastapi import APIRouter

from app.services.outbreak_service import service


router=APIRouter(
prefix="/outbreaks",
tags=["Outbreaks"]
)



@router.post("/register")
def register(data:dict):

    return service.register(data)



@router.get("/monitor")
def monitor():

    return service.monitor()
