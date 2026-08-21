from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionCategory(Base):

    __tablename__ = "inspection_categories"


    id = Column(
        Integer,
        primary_key=True
    )


    name = Column(
        String(200),
        nullable=False
    )


    code = Column(
        String(50)
    )
