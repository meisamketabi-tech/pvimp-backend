from fastapi import APIRouter

from app.services.backup_service import service


router=APIRouter(
prefix="/backup",
tags=["Backup"]
)



@router.post("/create")
def create():

    return service.create()



@router.post("/restore")
def restore(data:dict):

    return service.restore(
        data.get("file")
    )
