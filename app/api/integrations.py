from fastapi import APIRouter

from app.services.integration_service import service


router=APIRouter(
prefix="/integrations",
tags=["Integrations"]
)



@router.post("/register")
def register(data:dict):

    return service.register(data)



@router.post("/sync/{system}")
def sync(system:str):

    return service.sync(system)
