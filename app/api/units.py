from fastapi import APIRouter

from app.services.unit_service import service


router=APIRouter(
prefix="/units",
tags=["Units"]
)



@router.post("/")
def register(data:dict):

    return service.register(data)



@router.get("/search")
def search(
    q:str=""
):

    return service.search(q)
