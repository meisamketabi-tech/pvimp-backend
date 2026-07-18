from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.inspection_approval_service import (
    get_approvals
)


router = APIRouter(
    prefix="/inspection-approvals",
    tags=["Inspection Approvals"]
)


@router.get("/{inspection_id}")
def list_all(
    inspection_id: int,
    db: Session = Depends(get_db)
):

    return get_approvals(
        db,
        inspection_id
    )
