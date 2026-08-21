from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class GISLaboratory(Base):
    __tablename__ = "gis_laboratories"

    id = Column(Integer, primary_key=True, index=True)

    lab_code = Column(String(30), unique=True, nullable=False, index=True)

    lab_name = Column(String(255), nullable=False)

    address = Column(String(500))

    phone = Column(String(50))

    is_active = Column(Integer, default=1)