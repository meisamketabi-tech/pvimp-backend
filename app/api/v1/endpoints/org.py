from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.schemas.org import (
    CountyCreate,
    CountyRead,
    CountyUpdate,
    ProvinceCreate,
    ProvinceRead,
    ProvinceUpdate,
    VeterinaryUnitCreate,
    VeterinaryUnitRead,
    VeterinaryUnitUpdate,
)
from app.services import org_service
from app.db.models.org import County, Province, VeterinaryUnit


router = APIRouter()


@router.post(
    "/provinces",
    response_model=ProvinceRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
def create_province(
    province_in: ProvinceCreate,
    db: Session = Depends(get_db),
) -> ProvinceRead:
    return org_service.create_province(db, province_in)


@router.get(
    "/provinces",
    response_model=List[ProvinceRead],
    dependencies=[Depends(require_roles("admin", "viewer"))],
)
def list_provinces(
    db: Session = Depends(get_db),
) -> List[ProvinceRead]:
    items = db.query(Province).order_by(Province.id.asc()).all()
    return [ProvinceRead.model_validate(item) for item in items]


@router.get(
    "/provinces/{province_id}",
    response_model=ProvinceRead,
    dependencies=[Depends(require_roles("admin", "viewer"))],
)
def get_province(
    province_id: int,
    db: Session = Depends(get_db),
) -> ProvinceRead:
    obj = db.query(Province).get(province_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Province not found",
        )
    return ProvinceRead.model_validate(obj)


@router.put(
    "/provinces/{province_id}",
    response_model=ProvinceRead,
    dependencies=[Depends(require_roles("admin"))],
)
def update_province(
    province_id: int,
    province_in: ProvinceUpdate,
    db: Session = Depends(get_db),
) -> ProvinceRead:
    obj = db.query(Province).get(province_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Province not found",
        )
    return org_service.update_province(db, obj, province_in)


@router.post(
    "/counties",
    response_model=CountyRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
def create_county(
    county_in: CountyCreate,
    db: Session = Depends(get_db),
) -> CountyRead:
    return org_service.create_county(db, county_in)


@router.get(
    "/counties",
    response_model=List[CountyRead],
    dependencies=[Depends(require_roles("admin", "viewer"))],
)
def list_counties(
    db: Session = Depends(get_db),
) -> List[CountyRead]:
    items = db.query(County).order_by(County.id.asc()).all()
    return [CountyRead.model_validate(item) for item in items]


@router.get(
    "/counties/{county_id}",
    response_model=CountyRead,
    dependencies=[Depends(require_roles("admin", "viewer"))],
)
def get_county(
    county_id: int,
    db: Session = Depends(get_db),
) -> CountyRead:
    obj = db.query(County).get(county_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="County not found",
        )
    return CountyRead.model_validate(obj)


@router.put(
    "/counties/{county_id}",
    response_model=CountyRead,
    dependencies=[Depends(require_roles("admin"))],
)
def update_county(
    county_id: int,
    county_in: CountyUpdate,
    db: Session = Depends(get_db),
) -> CountyRead:
    obj = db.query(County).get(county_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="County not found",
        )
    return org_service.update_county(db, obj, county_in)


@router.post(
    "/veterinary-units",
    response_model=VeterinaryUnitRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
def create_veterinary_unit(
    unit_in: VeterinaryUnitCreate,
    db: Session = Depends(get_db),
) -> VeterinaryUnitRead:
    return org_service.create_veterinary_unit(db, unit_in)


@router.get(
    "/veterinary-units",
    response_model=List[VeterinaryUnitRead],
    dependencies=[Depends(require_roles("admin", "viewer"))],
)
def list_veterinary_units(
    db: Session = Depends(get_db),
) -> List[VeterinaryUnitRead]:
    items = db.query(VeterinaryUnit).order_by(VeterinaryUnit.id.asc()).all()
    return [VeterinaryUnitRead.model_validate(item) for item in items]


@router.get(
    "/veterinary-units/{unit_id}",
    response_model=VeterinaryUnitRead,
    dependencies=[Depends(require_roles("admin", "viewer"))],
)
def get_veterinary_unit(
    unit_id: int,
    db: Session = Depends(get_db),
) -> VeterinaryUnitRead:
    obj = db.query(VeterinaryUnit).get(unit_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veterinary unit not found",
        )
    return VeterinaryUnitRead.model_validate(obj)


@router.put(
    "/veterinary-units/{unit_id}",
    response_model=VeterinaryUnitRead,
    dependencies=[Depends(require_roles("admin"))],
)
def update_veterinary_unit(
    unit_id: int,
    unit_in: VeterinaryUnitUpdate,
    db: Session = Depends(get_db),
) -> VeterinaryUnitRead:
    obj = db.query(VeterinaryUnit).get(unit_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veterinary unit not found",
        )
    return org_service.update_veterinary_unit(db, obj, unit_in)
