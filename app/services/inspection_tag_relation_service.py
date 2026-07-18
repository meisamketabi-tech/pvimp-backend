from sqlalchemy.orm import Session

from app.db.models.inspection_tag_relation import InspectionTagRelation


def get_tag_relations(
    db: Session
):

    return (
        db.query(
            InspectionTagRelation
        )
        .all()
    )
