from sqlalchemy import Column,Integer,String,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class DataExport(Base):

    __tablename__="data_exports"


    id=Column(Integer,primary_key=True)

    export_type=Column(String(100))

    requested_by=Column(Integer)

    file_path=Column(String(500))

    status=Column(String(50))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
