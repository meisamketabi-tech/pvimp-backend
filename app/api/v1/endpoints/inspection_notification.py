from fastapi import APIRouter

from app.services.inspection_notification_service import (
    create_notification
)


router = APIRouter(
    prefix="/inspection-notifications",
    tags=["Inspection Notifications"]
)


@router.post(
    "/{inspection_id}"
)
def notify(
    inspection_id: int,
    message: str
):

    return {
        "inspection_id": inspection_id,
        "message": message
    }