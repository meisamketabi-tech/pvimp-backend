from fastapi import APIRouter

from app.services.system_service import service


router=APIRouter(
prefix="/system",
tags=["System"]
)



@router.get("/health")
def health():

    return service.health()



@router.get("/settings")
def settings():

    return service.settings()
