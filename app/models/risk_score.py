from sqlalchemy import Column,Integer,Float,String,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class RiskScore(Base):

    __tablename__="risk_scores"


    id=Column(Integer,primary_key=True)

    entity_type=Column(String(100))

    entity_id=Column(Integer)

    score=Column(Float)

    level=Column(String(50))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
