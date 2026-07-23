from sqlalchemy import Column,Integer,String,Text,DateTime,Boolean

from sqlalchemy.sql import func

from app.core.database import Base


class Quarantine(Base):

    __tablename__="quarantines"


    id=Column(Integer,primary_key=True)

    shipment_id=Column(Integer)

    location=Column(String(300))

    quarantine_type=Column(String(100))

    status=Column(String(50))

    reason=Column(Text)

    released=Column(Boolean,default=False)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
