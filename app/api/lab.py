from fastapi import APIRouter

from app.services.lab_service import service


router=APIRouter(
prefix="/lab",
tags=["Laboratory"]
)



@router.post("/result")
def register(data:dict):

    return service.register_result(data)



@router.get("/result/{sample_id}")
def get(sample_id:int):

    return service.get_result(sample_id)
