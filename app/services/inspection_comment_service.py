from sqlalchemy.orm import Session

from app.db.models.inspection_comment import (
    InspectionComment
)


def create_comment(
    db: Session,
    data
):

    comment = InspectionComment(
        **data.model_dump()
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment



def get_comments(
    db: Session,
    inspection_id: int
):

    return (
        db.query(InspectionComment)
        .filter(
            InspectionComment.inspection_id == inspection_id
        )
        .all()
    )