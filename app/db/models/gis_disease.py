from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class GISDisease(Base):
    __tablename__ = "gis_diseases"

    id = Column(Integer, primary_key=True, index=True)

    disease_code = Column(String(20), unique=True, index=True)
    disease_name = Column(String(200), nullable=False)

    disease_group = Column(String(100))

    is_notifiable = Column(Integer, default=1)