
from sqlalchemy import Column,Integer,String,Float,DateTime
from sqlalchemy.sql import func

from app.core.database import Base



class HealthScore(Base):

    __tablename__="health_scores"


    id=Column(
        Integer,
        primary_key=True
    )


    unit_id=Column(
        Integer
    )


    unit_name=Column(
        String(200)
    )


    inspection_score=Column(
        Float
    )


    compliance_score=Column(
        Float
    )


    final_score=Column(
        Float
    )


    grade=Column(
        String(50)
    )


    created_at=Column(
        DateTime,
        server_default=func.now()
    )

