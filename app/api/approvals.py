from fastapi import APIRouter

from app.services.approval_service import service


router=APIRouter(
prefix="/approvals",
tags=["Approvals"]
)



@router.post("/request")
def request(data:dict):

    return service.request(data)



@router.post("/{id}/approve")
def approve(
    id:int,
    data:dict
):

    return service.approve(id,data)



@router.post("/{id}/reject")
def reject(
    id:int,
    data:dict
):

    return service.reject(id,data)
