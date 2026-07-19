from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class InspectionStatusEnum(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class InspectionResultEnum(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CONDITIONAL = "conditional"
    PENDING = "pending"


class InspectionType(Base):
    __tablename__ = "inspection_types"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False)
    description = Column(Text)

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    inspections = relationship(
        "Inspection",
        back_populates="inspection_type"
    )

    checklists = relationship(
        "Checklist",
        back_populates="inspection_type"
    )


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)

    inspection_number = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    inspection_type_id = Column(
        Integer,
        ForeignKey("inspection_types.id"),
        nullable=False
    )

    organization_unit_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=False
    )

    veterinary_unit_id = Column(
        Integer,
        ForeignKey("veterinary_units.id"),
        nullable=False
    )

    inspector_id = Column(
        Integer,
        ForeignKey("user_account.id"),
        nullable=False
    )

    inspection_date = Column(
        DateTime,
        nullable=False
    )

    status = Column(
        SQLEnum(InspectionStatusEnum),
        default=InspectionStatusEnum.DRAFT,
        nullable=False
    )

    result = Column(
        SQLEnum(InspectionResultEnum),
        default=InspectionResultEnum.PENDING,
        nullable=False
    )

    notes = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    inspection_type = relationship(
        "InspectionType",
        back_populates="inspections"
    )

    organization_unit = relationship(
        "OrganizationUnit"
    )

    veterinary_unit = relationship(
        "VeterinaryUnit",
        back_populates="inspections"
    )

    inspector = relationship(
        "User"
    )

    items_result = relationship(
        "InspectionItemResult",
        back_populates="inspection",
        cascade="all, delete-orphan"
    )

    assignments = relationship(
    "InspectionAssignment",
    back_populates="inspection",
    cascade="all, delete-orphan",
)


class Checklist(Base):
    __tablename__ = "checklists"

    id = Column(Integer, primary_key=True, index=True)

    inspection_type_id = Column(
        Integer,
        ForeignKey("inspection_types.id"),
        nullable=False
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(Text)

    is_active = Column(
        Boolean,
        default=True
    )

    inspection_type = relationship(
        "InspectionType",
        back_populates="checklists"
    )

    items = relationship(
        "ChecklistItem",
        back_populates="checklist",
        cascade="all, delete-orphan"
    )


class ChecklistItem(Base):
    __tablename__ = "checklist_items"

    id = Column(Integer, primary_key=True, index=True)

    checklist_id = Column(
        Integer,
        ForeignKey("checklists.id"),
        nullable=False
    )

    title = Column(
        String(300),
        nullable=False
    )

    description = Column(Text)

    weight = Column(
        Integer,
        default=1
    )

    is_required = Column(
        Boolean,
        default=True
    )

    checklist = relationship(
        "Checklist",
        back_populates="items"
    )

    results = relationship(
        "InspectionItemResult",
        back_populates="checklist_item"
    )


class InspectionItemResult(Base):
    __tablename__ = "inspection_item_results"

    id = Column(Integer, primary_key=True, index=True)

    inspection_id = Column(
        Integer,
        ForeignKey("inspections.id"),
        nullable=False
    )

    checklist_item_id = Column(
        Integer,
        ForeignKey("checklist_items.id"),
        nullable=False
    )

    is_compliant = Column(
        Boolean,
        nullable=False
    )

    score = Column(Integer)

    inspector_note = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    inspection = relationship(
        "Inspection",
        back_populates="items_result"
    )

    checklist_item = relationship(
        "ChecklistItem",
        back_populates="results"
    )


