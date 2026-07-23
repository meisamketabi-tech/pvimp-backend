from sqlalchemy import Column,Integer,String,Float,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class KPIValue(Base):

    __tablename__="kpi_values"


    id=Column(Integer,primary_key=True)

    kpi_code=Column(String(100))

    value=Column(Float)

    organization_unit=Column(String(100))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
