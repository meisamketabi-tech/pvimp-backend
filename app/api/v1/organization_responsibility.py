from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.db.models.organization_responsibility import OrganizationResponsibility

from app.schemas.organization_responsibility import (
    OrganizationResponsibilityCreate,
    OrganizationResponsibilityResponse,
)


router = APIRouter(
    prefix="/organization-responsibilities",
    tags=["Organization Responsibilities"],
)



@router.post(
    "",
    response_model=OrganizationResponsibilityResponse,
)
def create_responsibility(
    payload: OrganizationResponsibilityCreate,
    db: Session = Depends(get_db),
):

    obj = OrganizationResponsibility(
        organization_unit_id=payload.organization_unit_id,
        inspection_type_id=payload.inspection_type_id,
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
    )


    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj



@router.get(
    "/unit/{unit_id}",
    response_model=list[OrganizationResponsibilityResponse],
)
def get_unit_responsibilities(
    unit_id:int,
    db:Session=Depends(get_db),
):

    return (
        db.query(OrganizationResponsibility)
        .filter(
            OrganizationResponsibility.organization_unit_id==unit_id,
            OrganizationResponsibility.is_active==True,
        )
        .all()
    )
