from fastapi import APIRouter

from app.services.inspection_service import service


router=APIRouter(
prefix="/inspections",
tags=["Inspections"]
)



@router.post("/")
def create(data:dict):

    return service.create(data)



@router.get("/")
def list():

    return service.list()
