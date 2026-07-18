from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionStatusHistory(Base):

    __tablename__ = "inspection_status_histories"

    id = Column(
        Integer,
        primary_key=True
    )

    inspection_id = Column(
        Integer
    )

    old_status = Column(
        String(50)
    )

    new_status = Column(
        String(50)
    )
