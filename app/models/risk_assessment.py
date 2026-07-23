from sqlalchemy import Column,Integer,String,Float,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class RiskAssessment(Base):

    __tablename__="risk_assessments"


    id=Column(Integer,primary_key=True)

    entity_type=Column(String(100))

    entity_id=Column(Integer)

    risk_level=Column(String(50))

    risk_score=Column(Float)

    factors=Column(Text)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
