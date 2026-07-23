from sqlalchemy import Column,Integer,String,Boolean

from app.core.database import Base


class PermissionRule(Base):

    __tablename__="permission_rules"


    id=Column(Integer,primary_key=True)

    role=Column(String(100))

    resource=Column(String(200))

    action=Column(String(100))

    allowed=Column(Boolean,default=True)
