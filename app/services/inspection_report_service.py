from sqlalchemy.orm import Session

from app.db.models.inspection import Inspection


def count_inspections(
    db: Session
):

    return (
        db.query(Inspection)
        .count()
    )


def count_completed_inspections(
    db: Session
):

    return (
        db.query(Inspection)
        .filter(
            Inspection.status == "completed"
        )
        .count()
    )


def inspection_statistics(
    db: Session
):

    return {
        "total":
            count_inspections(db),

        "completed":
            count_completed_inspections(db),
    }