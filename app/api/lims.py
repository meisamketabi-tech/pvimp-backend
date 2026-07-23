from fastapi import APIRouter

from app.services.lims_service import service


router=APIRouter(
prefix="/lims",
tags=["LIMS"]
)



@router.post("/send")
def send(data:dict):

    return service.send_sample(data)



@router.get("/result/{id}")
def result(id:int):

    return service.receive_result(id)
