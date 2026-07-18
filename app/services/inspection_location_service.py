from sqlalchemy.orm import Session

from app.db.models.inspection_location import (
    InspectionLocation
)


def create_location(
    db: Session,
    data
):

    location = InspectionLocation(
        **data.model_dump()
    )

    db.add(location)

    db.commit()

    db.refresh(location)

    return location