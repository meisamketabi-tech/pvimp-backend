from fastapi import APIRouter

from app.services.gis_service import service


router=APIRouter(
prefix="/gis",
tags=["GIS"]
)



@router.post("/register")
def register(data:dict):

    return service.register(data)



@router.get("/nearby")
def nearby(
    lat:float,
    lng:float
):

    return service.nearby(
        lat,
        lng
    )
