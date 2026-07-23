from fastapi import APIRouter

from app.services.message_service import service


router=APIRouter(
prefix="/messages",
tags=["Messages"]
)



@router.post("/send")
def send(data:dict):

    return service.send(data)



@router.get("/inbox/{user_id}")
def inbox(user_id:int):

    return service.inbox(user_id)
