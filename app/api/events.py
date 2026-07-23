from fastapi import APIRouter

from app.services.event_service import service


router=APIRouter(
prefix="/events",
tags=["Events"]
)



@router.post("/publish")
def publish(data:dict):

    return service.publish(data)



@router.get("/stream")
def stream():

    return service.stream()
