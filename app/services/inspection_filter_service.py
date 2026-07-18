from sqlalchemy.orm import Session

from app.db.models.inspection import Inspection


def filter_inspections(
    db: Session,
    filters
):

    query = db.query(
        Inspection
    )


    if filters.inspection_type_id:

        query = query.filter(
            Inspection.inspection_type_id
            ==
            filters.inspection_type_id
        )


    if filters.organization_unit_id:

        query = query.filter(
            Inspection.organization_unit_id
            ==
            filters.organization_unit_id
        )


    if filters.inspector_id:

        query = query.filter(
            Inspection.inspector_id
            ==
            filters.inspector_id
        )


    if filters.status:

        query = query.filter(
            Inspection.status
            ==
            filters.status
        )


    if filters.result:

        query = query.filter(
            Inspection.result
            ==
            filters.result
        )


    return query.all()