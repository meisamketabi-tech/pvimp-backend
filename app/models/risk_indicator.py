from sqlalchemy import Column,Integer,String,Float,Boolean

from app.core.database import Base


class RiskIndicator(Base):

    __tablename__="risk_indicators"


    id=Column(Integer,primary_key=True)

    title=Column(String(200))

    category=Column(String(100))

    weight=Column(Float)

    active=Column(Boolean,default=True)
