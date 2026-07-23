from fastapi import APIRouter

from app.services.calendar_service import service


router=APIRouter(
prefix="/calendar",
tags=["Calendar"]
)



@router.post("/event")
def event(data:dict):

    return service.create_event(data)



@router.post("/inspection")
def inspection(data:dict):

    return service.plan_inspection(data)



@router.get("/")
def list_calendar():

    return []
