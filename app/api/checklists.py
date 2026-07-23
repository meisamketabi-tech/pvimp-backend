from fastapi import APIRouter

from app.services.checklist_service import service


router=APIRouter(
prefix="/checklists",
tags=["Checklists"]
)



@router.post("/")
def create(data:dict):

    return service.create(data)



@router.get("/{id}")
def get(id:int):

    return service.get(id)
