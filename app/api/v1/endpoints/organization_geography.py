from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.db.models.organization import OrganizationUnit
from app.db.models.geographic_area import GeographicArea
from app.db.models.organization_unit_area import OrganizationUnitArea


router = APIRouter(
    prefix="/organization-geography",
    tags=["Organization Geography"]
)


@router.get("/{unit_id}")
def get_unit_areas(
    unit_id: int,
    db: Session = Depends(get_db)
):

    unit = db.query(OrganizationUnit).filter(
        OrganizationUnit.id == unit_id
    ).first()

    if not unit:
        raise HTTPException(
            status_code=404,
            detail="Organization unit not found"
        )


    return [
        {
            "id": item.geographic_area.id,
            "code": item.geographic_area.code,
            "name": item.geographic_area.name,
            "type": item.geographic_area.area_type
        }
        for item in unit.geographic_areas
    ]



@router.post("/{unit_id}/{area_id}")
def assign_area(
    unit_id: int,
    area_id: int,
    db: Session = Depends(get_db)
):

    unit = db.query(OrganizationUnit).filter(
        OrganizationUnit.id == unit_id
    ).first()

    area = db.query(GeographicArea).filter(
        GeographicArea.id == area_id
    ).first()


    if not unit or not area:
        raise HTTPException(
            status_code=404,
            detail="Unit or area not found"
        )


    exists = db.query(OrganizationUnitArea).filter(
        OrganizationUnitArea.organization_unit_id == unit_id,
        OrganizationUnitArea.geographic_area_id == area_id
    ).first()


    if exists:
        return {
            "message": "Already assigned"
        }


    relation = OrganizationUnitArea(
        organization_unit_id=unit_id,
        geographic_area_id=area_id
    )


    db.add(relation)
    db.commit()


    return {
        "message": "Area assigned successfully"
    }



@router.delete("/{unit_id}/{area_id}")
def remove_area(
    unit_id: int,
    area_id: int,
    db: Session = Depends(get_db)
):

    relation = db.query(OrganizationUnitArea).filter(
        OrganizationUnitArea.organization_unit_id == unit_id,
        OrganizationUnitArea.geographic_area_id == area_id
    ).first()


    if not relation:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )


    db.delete(relation)
    db.commit()


    return {
        "message": "Removed successfully"
    }