from fastapi import APIRouter

from app.services.license_service import service


router=APIRouter(
prefix="/licenses",
tags=["Licenses"]
)



@router.post("/issue")
def issue(data:dict):

    return service.issue(data)



@router.get("/verify/{number}")
def verify(number:str):

    return service.verify(number)
