from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionReview(Base):

    __tablename__ = "inspection_reviews"

    id = Column(
        Integer,
        primary_key=True
    )

    inspection_id = Column(
        Integer,
        ForeignKey("inspections.id"),
        nullable=False
    )

    reviewer_id = Column(
    Integer,
    ForeignKey("user_account.id")
)

    comment = Column(
        String(1000)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
