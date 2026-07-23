from fastapi import APIRouter

from app.services.legal_service import service


router=APIRouter(
prefix="/legal",
tags=["Legal"]
)



@router.post("/case")
def create(data:dict):

    return service.create_case(data)



@router.put("/case/{id}")
def update(
    id:int,
    data:dict
):

    return service.update_status(
        id,
        data.get("status")
    )
