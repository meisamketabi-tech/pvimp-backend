from sqlalchemy import Column,Integer,String,Float,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class KPI(Base):

    __tablename__="kpis"


    id=Column(Integer,primary_key=True)

    name=Column(String(200))

    category=Column(String(100))

    value=Column(Float)

    target=Column(Float)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
