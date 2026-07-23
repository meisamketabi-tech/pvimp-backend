from fastapi import APIRouter

from app.services.task_service import service


router=APIRouter(
prefix="/tasks",
tags=["Tasks"]
)



@router.post("/")
def create(data:dict):

    return service.create(data)



@router.get("/")
def list():

    return service.list()



@router.put("/{id}")
def update(
    id:int,
    data:dict
):

    return service.update(
        id,
        data
    )
