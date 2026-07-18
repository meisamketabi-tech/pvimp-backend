from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionDepartmentRule(Base):

    __tablename__ = "inspection_department_rules"

    id = Column(
        Integer,
        primary_key=True
    )

    department = Column(
        String(200)
    )

    rule = Column(
        String(500)
    )
