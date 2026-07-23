from fastapi import APIRouter

from app.services.config_service import service


router=APIRouter(
prefix="/config",
tags=["Configuration"]
)



@router.post("/set")
def set_config(data:dict):

    return service.set(
        data.get("key"),
        data.get("value")
    )



@router.get("/{key}")
def get_config(key:str):

    return service.get(key)
