from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class LegalCase(Base):

    __tablename__="legal_cases"


    id=Column(Integer,primary_key=True)

    violation_id=Column(Integer)

    case_number=Column(String(100))

    subject=Column(String(300))

    description=Column(Text)

    status=Column(String(50))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
