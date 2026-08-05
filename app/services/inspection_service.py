from sqlalchemy.orm import Session

from app.crud.inspection import (
    create_inspection_type as crud_create_inspection_type,
    get_inspection_types as crud_get_inspection_types,
    get_all_inspections,
    get_inspection as crud_get_inspection,
)

from app.db.models.inspection import Inspection


def create_inspection_type(
    db: Session,
    data,
):
    return crud_create_inspection_type(
        db,
        data,
    )


def get_inspection_types(
    db: Session,
):
    return crud_get_inspection_types(
        db,
    )


def create_inspection(
    db: Session,
    data,
):
    obj = Inspection(
        **data.model_dump()
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def get_inspections(
    db: Session,
):
    return get_all_inspections(
        db,
    )


def get_inspection(
    db: Session,
    inspection_id: int,
):
    return crud_get_inspection(
        db,
        inspection_id,
    )


def update_inspection(
    db: Session,
    inspection_id: int,
    data,
):
    obj = crud_get_inspection(
        db,
        inspection_id,
    )

    if obj is None:
        return None

    values = data.model_dump(
        exclude_unset=True,
    )

    for field, value in values.items():
        setattr(
            obj,
            field,
            value,
        )

    db.commit()
    db.refresh(obj)

    return obj


def update_inspection_status(
    db: Session,
    inspection_id: int,
    data,
):
    obj = crud_get_inspection(
        db,
        inspection_id,
    )

    if obj is None:
        return None

    obj.status = data.status

    db.commit()
    db.refresh(obj)

    return obj


def get_inspection_status_history(
    db: Session,
    inspection_id: int,
):
    if hasattr(
        Inspection,
        "status_history",
    ):
        obj = crud_get_inspection(
            db,
            inspection_id,
        )

        if obj is None:
            return []

        return obj.status_history

    return []