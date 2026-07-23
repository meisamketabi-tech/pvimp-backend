from sqlalchemy import Column,Integer,String,DateTime,Boolean

from sqlalchemy.sql import func

from app.core.database import Base


class Backup(Base):

    __tablename__="backups"


    id=Column(Integer,primary_key=True)

    backup_type=Column(String(100))

    file_path=Column(String(500))

    size=Column(String(100))

    status=Column(String(50))

    verified=Column(Boolean,default=False)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
