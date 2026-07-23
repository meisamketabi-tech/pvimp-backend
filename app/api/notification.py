from fastapi import APIRouter


router=APIRouter(
prefix="/notifications",
tags=["Notifications"]
)


@router.get("/{user_id}")
def user_notifications(user_id:int):

    return []
