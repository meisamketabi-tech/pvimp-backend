from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class SearchIndex(Base):

    __tablename__="search_indexes"


    id=Column(Integer,primary_key=True)

    entity_type=Column(String(100))

    entity_id=Column(Integer)

    keywords=Column(Text)

    content=Column(Text)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
