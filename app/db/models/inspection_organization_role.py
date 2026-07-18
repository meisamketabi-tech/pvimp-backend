from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionOrganizationRole(Base):

    __tablename__ = "inspection_organization_roles"


    id = Column(
        Integer,
        primary_key=True
    )


    name = Column(
        String(200)
    )


    permission = Column(
        String(500)
    )
