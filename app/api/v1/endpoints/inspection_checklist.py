from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.inspection import (
    ChecklistCreate,
    ChecklistResponse,
)

from app.services.inspection_service import (
    create_checklist,
    get_checklists,
)


router = APIRouter(
    prefix="/checklists",
    tags=["Checklists"]
)


@router.post(
    "",
    response_model=ChecklistResponse
)
def create(
    data: ChecklistCreate,
    db: Session = Depends(get_db)
):

    return create_checklist(
        db,
        data
    )


@router.get(
    "",
    response_model=List[ChecklistResponse]
)
def list_all(
    db: Session = Depends(get_db)
):

    return get_checklists(
        db
    )