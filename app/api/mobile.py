from fastapi import APIRouter

from app.services.mobile_service import service


router=APIRouter(
prefix="/mobile",
tags=["Mobile"]
)



@router.post("/sync")
def sync(data:dict):

    return service.sync(
        data.get("user_id"),
        data
    )



@router.get("/offline/{user_id}")
def offline(user_id:int):

    return service.offline_package(user_id)
