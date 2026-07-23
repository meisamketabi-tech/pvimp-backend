from fastapi import APIRouter

from app.services.sync_service import service


router=APIRouter(
prefix="/integration",
tags=["Integration"]
)



@router.get("/gis/{id}")
def gis(id:int):

    return service.gis_sync(id)



@router.post("/lims")
def lims(data:dict):

    return service.lims_sync(data)



@router.post("/eivo")
def eivo(data:dict):

    return service.eivo_sync(data)
