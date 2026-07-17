from sqlalchemy.orm import Session

from app.db.models.org import Province, County, VeterinaryUnit
from app.schemas.org import (
    ProvinceCreate,
    ProvinceUpdate,
    CountyCreate,
    CountyUpdate,
    VeterinaryUnitCreate,
    VeterinaryUnitUpdate,
)


def create_province(db: Session, obj_in: ProvinceCreate) -> Province:
    province = Province(**obj_in.model_dump())
    db.add(province)
    db.commit()
    db.refresh(province)
    return province


def update_province(db: Session, db_obj: Province, obj_in: ProvinceUpdate) -> Province:
    data = obj_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_county(db: Session, obj_in: CountyCreate) -> County:
    county = County(**obj_in.model_dump())
    db.add(county)
    db.commit()
    db.refresh(county)
    return county


def update_county(db: Session, db_obj: County, obj_in: CountyUpdate) -> County:
    data = obj_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_veterinary_unit(db: Session, obj_in: VeterinaryUnitCreate) -> VeterinaryUnit:
    vu = VeterinaryUnit(**obj_in.model_dump())
    db.add(vu)
    db.commit()
    db.refresh(vu)
    return vu


def update_veterinary_unit(
    db: Session,
    db_obj: VeterinaryUnit,
    obj_in: VeterinaryUnitUpdate,
) -> VeterinaryUnit:
    data = obj_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
