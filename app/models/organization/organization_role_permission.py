from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from datetime import datetime

from app.db.base_class import Base


class OrganizationRolePermission(Base):
    __tablename__ = "organization_role_permissions"

    id = Column(Integer, primary_key=True, index=True)

    role_id = Column(
        Integer,
        ForeignKey("organization_roles.id"),
        nullable=False
    )

    permission_id = Column(
        Integer,
        ForeignKey("organization_permissions.id"),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
