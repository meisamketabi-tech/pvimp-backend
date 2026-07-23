from fastapi import APIRouter

from app.services.export_manager import manager


router=APIRouter(
prefix="/exports",
tags=["Exports"]
)



@router.post("/create")
def create(data:dict):

    return manager.create(data)



@router.get("/{id}")
def status(id:int):

    return manager.status(id)
