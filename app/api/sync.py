from fastapi import APIRouter

from app.services.sync_service import service


router=APIRouter(
prefix="/sync",
tags=["Synchronization"]
)



@router.post("/{system}")
def execute(system:str):

    return service.execute(system)



@router.get("/history")
def history():

    return service.history()
