from typing import List

from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.inspection_attachment import (
    InspectionAttachmentCreate,
    InspectionAttachmentResponse,
)

from app.services.inspection_attachment_service import (
    create_attachment,
    get_attachments,
)



router = APIRouter(
    prefix="/inspection-attachments",
    tags=["Inspection Attachments"]
)



@router.post(
    "",
    response_model=InspectionAttachmentResponse
)
def create(
    data: InspectionAttachmentCreate,
    db: Session = Depends(get_db)
):

    return create_attachment(
        db,
        data
    )



@router.get(
    "/{inspection_id}",
    response_model=List[InspectionAttachmentResponse]
)
def list_files(
    inspection_id: int,
    db: Session = Depends(get_db)
):

    return get_attachments(
        db,
        inspection_id
    )