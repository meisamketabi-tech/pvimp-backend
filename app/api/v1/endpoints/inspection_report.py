from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.inspection_report_service import (
    inspection_statistics,
)


router = APIRouter(
    prefix="/inspection-reports",
    tags=["Inspection Reports"]
)


@router.get("")
def get_report(
    db: Session = Depends(get_db)
):

    return inspection_statistics(db)