from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionPermissionRule(Base):

    __tablename__ = "inspection_permission_rules"


    id = Column(
        Integer,
        primary_key=True
    )


    role = Column(
        String(100)
    )


    permission = Column(
        String(200)
    )
