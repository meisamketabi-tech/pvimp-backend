from sqlalchemy import Column,Integer,String,Text,DateTime,Boolean

from sqlalchemy.sql import func

from app.core.database import Base


class Outbreak(Base):

    __tablename__="outbreaks"


    id=Column(Integer,primary_key=True)

    disease_id=Column(Integer)

    location=Column(String(300))

    severity=Column(String(100))

    description=Column(Text)

    status=Column(String(50))

    controlled=Column(Boolean,default=False)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
