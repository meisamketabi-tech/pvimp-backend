from fastapi import APIRouter

from app.services.permission_service import service


router=APIRouter(
prefix="/permissions",
tags=["Permissions"]
)



@router.post("/check")
def check(data:dict):

    return service.check(
        data.get("role"),
        data.get("resource"),
        data.get("action")
    )



@router.get("/{role}")
def permissions(role:str):

    return service.role_permissions(role)
