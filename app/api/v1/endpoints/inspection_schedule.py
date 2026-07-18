from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.inspection_schedule import (
    InspectionScheduleCreate,
    InspectionScheduleResponse,
)

from app.services.inspection_schedule_service import (
    create_schedule,
    get_schedules,
)


router = APIRouter(
    prefix="/inspection-schedules",
    tags=["Inspection Schedules"]
)


@router.post(
    "",
    response_model=InspectionScheduleResponse
)
def create(
    data: InspectionScheduleCreate,
    db: Session = Depends(get_db)
):

    return create_schedule(
        db,
        data
    )


@router.get(
    "",
    response_model=List[InspectionScheduleResponse]
)
def list_all(
    db: Session = Depends(get_db)
):

    return get_schedules(
        db
    )