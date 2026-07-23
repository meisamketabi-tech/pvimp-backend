from sqlalchemy import Column,Integer,String,Float,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class DashboardMetric(Base):

    __tablename__="dashboard_metrics"


    id=Column(Integer,primary_key=True)

    name=Column(String(200))

    value=Column(Float)

    unit=Column(String(50))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
