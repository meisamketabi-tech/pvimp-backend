from fastapi import APIRouter

from app.services.complaint_service import service


router=APIRouter(
prefix="/complaints",
tags=["Complaints"]
)



@router.post("/")
def submit(data:dict):

    return service.submit(data)



@router.get("/{id}")
def track(id:int):

    return service.track(id)
