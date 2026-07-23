from fastapi import APIRouter

from app.services.backup_service import service


router=APIRouter(
prefix="/backups",
tags=["Backups"]
)



@router.post("/create")
def create(data:dict):

    return service.create(data)



@router.post("/{id}/restore")
def restore(id:int):

    return service.restore(id)



@router.get("/")
def history():

    return service.history()
