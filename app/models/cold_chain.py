
from sqlalchemy import Column,Integer,String,Float,DateTime

from sqlalchemy.sql import func

from app.core.database import Base



class ColdChainLog(Base):

    __tablename__="cold_chain_logs"


    id=Column(
        Integer,
        primary_key=True
    )


    unit_id=Column(
        Integer
    )


    equipment_name=Column(
        String(200)
    )


    temperature=Column(
        Float
    )


    min_temperature=Column(
        Float
    )


    max_temperature=Column(
        Float
    )


    status=Column(
        String(50)
    )


    recorded_at=Column(
        DateTime,
        server_default=func.now()
    )

