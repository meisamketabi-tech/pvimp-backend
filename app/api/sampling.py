from fastapi import APIRouter

from app.services.sampling_service import service


router=APIRouter(
prefix="/sampling",
tags=["Sampling"]
)



@router.post("/register")
def register(data:dict):

    return service.register(data)



@router.get("/{id}/result")
def result(id:int):

    return service.result(id)
