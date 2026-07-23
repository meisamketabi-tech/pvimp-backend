from fastapi import APIRouter

from app.services.notification_service import service


router=APIRouter(
prefix="/notifications",
tags=["Notifications"]
)



@router.post("/send")
def send(data:dict):

    return service.send(data)



@router.get("/unread/{user_id}")
def unread(user_id:int):

    return service.unread(user_id)
