from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.organization import OrganizationUnit
from app.schemas.organization import (
    OrganizationUnitCreate,
    OrganizationUnitUpdate,
)



router = APIRouter(
    prefix="/organization",
    tags=["organization-crud"]
)


@router.post("/")
def create_unit(
    unit: OrganizationUnitCreate,
    db: Session = Depends(get_db),
    
):
    parent = None

    if unit.parent_id:
        parent = (
            db.query(OrganizationUnit)
            .filter(OrganizationUnit.id == unit.parent_id)
            .first()
        )

        if not parent:
            raise HTTPException(
                status_code=404,
                detail="Parent unit not found"
            )

    new_unit = OrganizationUnit(
        name=unit.name,
        code=unit.code,
        unit_type=unit.unit_type,
        parent_id=unit.parent_id,
        type_id=unit.type_id,
        level_id=unit.level_id,
        province_id=unit.province_id,
        county_id=unit.county_id,
        description=unit.description,
        is_active=True,
    )

    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)

    return new_unit


@router.get("/{unit_id}")
def get_unit(
    unit_id: int,
    db: Session = Depends(get_db),
    
):
    unit = (
        db.query(OrganizationUnit)
        .filter(OrganizationUnit.id == unit_id)
        .first()
    )

    if not unit:
        raise HTTPException(
            status_code=404,
            detail="Organization unit not found"
        )

    return unit


@router.put("/{unit_id}")
def update_unit(
    unit_id: int,
    data: OrganizationUnitUpdate,
    db: Session = Depends(get_db),
    
):
    unit = (
        db.query(OrganizationUnit)
        .filter(OrganizationUnit.id == unit_id)
        .first()
    )

    if not unit:
        raise HTTPException(
            status_code=404,
            detail="Organization unit not found"
        )

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(unit, key, value)

    db.commit()
    db.refresh(unit)

    return unit


@router.delete("/{unit_id}")
def delete_unit(
    unit_id: int,
    db: Session = Depends(get_db),
    
):
    unit = (
        db.query(OrganizationUnit)
        .filter(OrganizationUnit.id == unit_id)
        .first()
    )

    if not unit:
        raise HTTPException(
            status_code=404,
            detail="Organization unit not found"
        )

    children = (
        db.query(OrganizationUnit)
        .filter(OrganizationUnit.parent_id == unit_id)
        .count()
    )

    if children > 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete unit with children"
        )

    db.delete(unit)
    db.commit()

    return {
        "message": "Organization unit deleted successfully"
    }