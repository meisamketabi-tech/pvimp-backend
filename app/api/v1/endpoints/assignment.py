from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.db.models.assignment import UserAssignment
from app.db.models.organization_unit_position import OrganizationUnitPosition
from app.schemas.assignment import AssignmentCreate, AssignmentRead


router = APIRouter(
    prefix="/assignments",
    tags=["Assignments"],
)


@router.post(
    "",
    response_model=AssignmentRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
def create_assignment(
    payload: AssignmentCreate,
    db: Session = Depends(get_db),
):

    if payload.organization_unit_position_id:

        position = (
            db.query(OrganizationUnitPosition)
            .filter(
                OrganizationUnitPosition.id
                == payload.organization_unit_position_id,
                OrganizationUnitPosition.organization_unit_id
                == payload.organization_unit_id,
                OrganizationUnitPosition.is_active == True,
            )
            .first()
        )

        if not position:
            existing_position = (
                db.query(OrganizationUnitPosition)
                .filter(
                    OrganizationUnitPosition.id
                    == payload.organization_unit_position_id
                )
                .first()
            )

            if existing_position:
                raise HTTPException(
                    status_code=400,
                    detail="Cannot assign inactive position",
                )

            raise HTTPException(
                status_code=400,
                detail="Position does not belong to organization unit",
            )


    if payload.organization_unit_position_id:

        position = (
            db.query(OrganizationUnitPosition)
            .filter(
                OrganizationUnitPosition.id == payload.organization_unit_position_id
            )
            .first()
        )

        if not position:
            raise HTTPException(
                status_code=404,
                detail="Organization position not found",
            )

        if not position.is_active:
            raise HTTPException(
                status_code=400,
                detail="Cannot assign inactive position",
            )


    exists = (
        db.query(UserAssignment)
        .filter(
            UserAssignment.user_id == payload.user_id,
            UserAssignment.organization_unit_id == payload.organization_unit_id,
            UserAssignment.organization_unit_position_id == payload.organization_unit_position_id,
            UserAssignment.is_active == True,
        )
        .first()
    )

    if exists:
        raise HTTPException(
            status_code=400,
            detail="Active assignment already exists",
        )


    obj = UserAssignment(
        user_id=payload.user_id,
        organization_unit_id=payload.organization_unit_id,
        organization_unit_position_id=payload.organization_unit_position_id,
        role_id=payload.role_id,
        is_primary=payload.is_primary,
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj



@router.get(
    "",
    response_model=List[AssignmentRead],
    dependencies=[Depends(require_roles("admin", "viewer"))],
)
def list_assignments(
    db: Session = Depends(get_db),
):

    return (
        db.query(UserAssignment)
        .filter(
            UserAssignment.is_active == True
        )
        .all()
    )



@router.get(
    "/user/{user_id}",
    response_model=List[AssignmentRead],
    dependencies=[Depends(require_roles("admin", "viewer"))],
)
def user_assignments(
    user_id: int,
    db: Session = Depends(get_db),
):

    return (
        db.query(UserAssignment)
        .filter(
            UserAssignment.user_id == user_id,
            UserAssignment.is_active == True,
        )
        .all()
    )
