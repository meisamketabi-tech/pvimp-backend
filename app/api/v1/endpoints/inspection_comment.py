from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.inspection_comment import (
    InspectionCommentCreate,
    InspectionCommentResponse,
)

from app.services.inspection_comment_service import (
    create_comment,
    get_comments,
)


router = APIRouter(
    prefix="/inspection-comments",
    tags=["Inspection Comments"]
)


@router.post(
    "",
    response_model=InspectionCommentResponse
)
def create(
    data: InspectionCommentCreate,
    db: Session = Depends(get_db)
):

    return create_comment(db, data)



@router.get(
    "/{inspection_id}",
    response_model=List[InspectionCommentResponse]
)
def list_all(
    inspection_id: int,
    db: Session = Depends(get_db)
):

    return get_comments(
        db,
        inspection_id
    )