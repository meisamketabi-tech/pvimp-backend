from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class Report(Base):

    __tablename__="reports"


    id=Column(Integer,primary_key=True)

    title=Column(String(300))

    report_type=Column(String(100))

    parameters=Column(Text)

    generated_by=Column(Integer)

    file_path=Column(String(500))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
