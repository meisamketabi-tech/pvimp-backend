from fastapi import APIRouter

from app.services.organization_service import service


router=APIRouter(
prefix="/organization",
tags=["Organization"]
)



@router.post("/unit")
def create(data:dict):

    return service.create(data)



@router.get("/tree")
def tree():

    return service.tree()
