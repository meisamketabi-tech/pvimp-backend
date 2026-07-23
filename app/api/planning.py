from fastapi import APIRouter

from app.services.planning_service import service


router=APIRouter(
prefix="/planning",
tags=["Planning"]
)



@router.post("/plan")
def create(data:dict):

    return service.create_plan(data)



@router.get("/schedule/{id}")
def schedule(id:int):

    return service.generate_schedule(id)
