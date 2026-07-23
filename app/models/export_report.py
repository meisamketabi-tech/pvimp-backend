
from sqlalchemy import Column,Integer,String,Text,DateTime
from sqlalchemy.sql import func

from app.core.database import Base



class ExportReport(Base):

    __tablename__="export_reports"


    id=Column(
        Integer,
        primary_key=True
    )


    report_type=Column(
        String(100)
    )


    title=Column(
        String(200)
    )


    parameters=Column(
        Text
    )


    file_path=Column(
        String(500)
    )


    created_by=Column(
        Integer
    )


    created_at=Column(
        DateTime,
        server_default=func.now()
    )

