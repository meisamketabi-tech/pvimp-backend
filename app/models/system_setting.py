from sqlalchemy import Column,Integer,String,Text,Boolean

from app.core.database import Base


class SystemSetting(Base):

    __tablename__="system_settings"


    id=Column(Integer,primary_key=True)

    key=Column(String(200))

    value=Column(Text)

    description=Column(Text)

    active=Column(Boolean,default=True)
