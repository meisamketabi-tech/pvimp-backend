from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.inspection_location import (
    InspectionLocationCreate,
    InspectionLocationResponse,
)

from app.services.inspection_location_service import (
    create_location,
)


router = APIRouter(
    prefix="/inspection-locations",
    tags=["Inspection Locations"]
)


@router.post(
    "",
    response_model=InspectionLocationResponse
)
def create(
    data: InspectionLocationCreate,
    db: Session = Depends(get_db)
):

    return create_location(
        db,
        data
    )