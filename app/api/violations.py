from fastapi import APIRouter

from app.services.violation_service import service


router=APIRouter(
prefix="/violations",
tags=["Violations"]
)



@router.post("/")
def register(data:dict):

    return service.register(data)



@router.post("/{id}/resolve")
def resolve(id:int):

    return service.resolve(id)
