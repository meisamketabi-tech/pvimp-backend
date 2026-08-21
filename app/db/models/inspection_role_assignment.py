from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionRoleAssignment(Base):

    __tablename__ = "inspection_role_assignments"


    id = Column(
        Integer,
        primary_key=True
    )


    role = Column(
        String(100)
    )


    description = Column(
        String(500)
    )
