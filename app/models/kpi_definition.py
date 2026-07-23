from sqlalchemy import Column,Integer,String,Float,Boolean

from app.core.database import Base


class KPIDefinition(Base):

    __tablename__="kpi_definitions"


    id=Column(Integer,primary_key=True)

    code=Column(String(100))

    title=Column(String(300))

    category=Column(String(100))

    target=Column(Float)

    active=Column(Boolean,default=True)
