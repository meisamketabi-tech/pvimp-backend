from sqlalchemy import Column,Integer,String,Text,DateTime,Boolean

from sqlalchemy.sql import func

from app.core.database import Base


class Violation(Base):

    __tablename__="violations"


    id=Column(Integer,primary_key=True)

    inspection_id=Column(Integer)

    violation_type=Column(String(200))

    description=Column(Text)

    severity=Column(String(50))

    legal_reference=Column(String(300))

    resolved=Column(Boolean,default=False)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
