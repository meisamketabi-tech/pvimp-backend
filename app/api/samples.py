from fastapi import APIRouter

from app.services.sample_service import service


router=APIRouter(
prefix="/samples",
tags=["Samples"]
)



@router.post("/register")
def register(data:dict):

    return service.register(data)



@router.get("/{id}/result")
def result(id:int):

    return service.result(id)
