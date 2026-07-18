from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from sqlalchemy.orm import relationship

from app.db.base_class import Base


class OrganizationStructureNode(Base):

    __tablename__ = "organization_structure_nodes"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    organization_unit_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=False,
        index=True,
    )

    parent_id = Column(
        Integer,
        ForeignKey("organization_structure_nodes.id"),
        nullable=True,
        index=True,
    )

    title = Column(
        String(200),
        nullable=False,
    )

    node_type = Column(
        String(100),
        nullable=False,
    )

    display_order = Column(
        Integer,
        nullable=False,
        default=0,
    )

    is_visible = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )


    organization_unit = relationship(
        "OrganizationUnit",
    )


    parent = relationship(
        "OrganizationStructureNode",
        remote_side=[id],
        back_populates="children",
    )


    children = relationship(
        "OrganizationStructureNode",
        back_populates="parent",
        cascade="all, delete-orphan",
    )
