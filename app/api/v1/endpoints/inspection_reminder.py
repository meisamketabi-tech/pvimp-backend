from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.inspection_reminder_service import (
    get_reminders
)


router = APIRouter(
    prefix="/inspection-reminders",
    tags=["Inspection Reminders"]
)


@router.get("")
def list_all(
    db: Session = Depends(get_db)
):

    return get_reminders(db)
