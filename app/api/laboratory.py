from fastapi import APIRouter

from app.services.laboratory_service import service


router=APIRouter(
prefix="/laboratory",
tags=["Laboratory"]
)



@router.post("/send")
def send(data:dict):

    return service.send_sample(data)



@router.post("/result")
def result(data:dict):

    return service.receive_result(data)
