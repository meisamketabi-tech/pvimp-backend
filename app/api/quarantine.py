from fastapi import APIRouter

from app.services.quarantine_service import service


router=APIRouter(
prefix="/quarantine",
tags=["Quarantine"]
)



@router.post("/")
def create(data:dict):

    return service.create(data)



@router.post("/{id}/release")
def release(id:int):

    return service.release(id)
