from sqlalchemy import Column,Integer,String,Boolean

from app.core.database import Base


class OrganizationUnit(Base):

    __tablename__="organization_units"


    id=Column(Integer,primary_key=True)

    parent_id=Column(Integer)

    name=Column(String(300))

    unit_type=Column(String(100))

    code=Column(String(100))

    active=Column(Boolean,default=True)
