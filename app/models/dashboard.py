from sqlalchemy import Column,Integer,String,Text,Boolean

from app.core.database import Base


class Dashboard(Base):

    __tablename__="dashboards"


    id=Column(Integer,primary_key=True)

    title=Column(String(300))

    role=Column(String(100))

    widgets=Column(Text)

    active=Column(Boolean,default=True)
