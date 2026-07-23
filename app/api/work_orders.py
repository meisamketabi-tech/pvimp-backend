from fastapi import APIRouter

from app.services.work_order_service import service


router=APIRouter(
prefix="/work-orders",
tags=["Work Orders"]
)



@router.post("/")
def create(data:dict):

    return service.create(data)



@router.post("/{id}/assign")
def assign(
    id:int,
    data:dict
):

    return service.assign(
        id,
        data.get("user_id")
    )
