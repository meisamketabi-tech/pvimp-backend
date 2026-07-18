from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.inspection_template import (
    InspectionTemplateCreate,
    InspectionTemplateResponse,
)

from app.services.inspection_template_service import (
    create_template,
    get_templates,
)


router = APIRouter(
    prefix="/inspection-templates",
    tags=["Inspection Templates"]
)


@router.post(
    "",
    response_model=InspectionTemplateResponse
)
def create(
    data: InspectionTemplateCreate,
    db: Session = Depends(get_db)
):

    return create_template(
        db,
        data
    )


@router.get(
    "",
    response_model=List[InspectionTemplateResponse]
)
def list_all(
    db: Session = Depends(get_db)
):

    return get_templates(
        db
    )