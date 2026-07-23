from fastapi import APIRouter

from app.services.veterinary_center_service import service


router=APIRouter(
prefix="/veterinary-centers",
tags=["Veterinary Centers"]
)



@router.post("/register")
def register(data:dict):

    return service.register(data)



@router.get("/search")
def search(keyword:str):

    return service.search(keyword)
