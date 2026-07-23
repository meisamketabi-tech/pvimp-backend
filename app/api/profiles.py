from fastapi import APIRouter

from app.services.profile_service import service


router=APIRouter(
prefix="/profiles",
tags=["Profiles"]
)



@router.post("/update")
def update(data:dict):

    return service.update(data)



@router.get("/{user_id}")
def get(user_id:int):

    return service.get(user_id)
