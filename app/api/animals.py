from fastapi import APIRouter

from app.services.animal_service import service


router=APIRouter(
prefix="/animals",
tags=["Animals"]
)



@router.post("/register")
def register(data:dict):

    return service.register(data)



@router.get("/{id}")
def get(id:int):

    return service.get(id)
