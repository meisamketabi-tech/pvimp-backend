from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionApiKey(Base):

    __tablename__ = "inspection_api_keys"


    id = Column(
        Integer,
        primary_key=True
    )


    name = Column(
        String(200)
    )


    key_hash = Column(
        String(500)
    )
