from sqlalchemy import Column,Integer,String

from app.core.database import Base


class RoleAssignment(Base):

    __tablename__="role_assignments"


    id=Column(Integer,primary_key=True)

    user_id=Column(Integer)

    role=Column(String(100))

    unit_id=Column(Integer)
