from fastapi import APIRouter

from app.services.farm_service import service


router=APIRouter(
prefix="/farms",
tags=["Farms"]
)



@router.post("/register")
def register(data:dict):

    return service.register(data)



@router.get("/search")
def search(keyword:str):

    return service.search(keyword)
