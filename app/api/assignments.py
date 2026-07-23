from fastapi import APIRouter

from app.services.assignment_service import service


router=APIRouter(
prefix="/assignments",
tags=["Assignments"]
)



@router.post("/")
def assign(data:dict):

    return service.assign(data)



@router.post("/{id}/accept")
def accept(id:int):

    return service.accept(id)
