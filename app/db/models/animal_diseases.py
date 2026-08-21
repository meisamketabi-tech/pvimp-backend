from __future__ import annotations

from datetime import datetime, date
from typing import Optional

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Enum,
    Float,
    Text,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.mixins import TimestampMixin


class EpidemiologicalUnitType(str, Enum):
    FARM = "FARM"
    SLAUGHTERHOUSE = "SLAUGHTERHOUSE"
    MARKET = "MARKET"
    VILLAGE = "VILLAGE"
    DISTRICT = "DISTRICT"
    OTHER = "OTHER"


class DiseaseCategory(str, Enum):
    FOOT_AND_MOUTH = "FOOT_AND_MOUTH"
    ANTHRAX = "ANTHRAX"
    PPR = "PPR"
    RINDERPEST = "RINDERPEST"
    BSE = "BSE"
    OTHER = "OTHER"


class DiseaseGroup(str, Enum):
    GROUP_I = "GROUP_I"
    GROUP_II = "GROUP_II"
    OTHER = "OTHER"


class DiseaseReportStatus(str, Enum):
    DRAFT = "DRAFT"
    REPORTED = "REPORTED"
    UNDER_INVESTIGATION = "UNDER_INVESTIGATION"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"
    CLOSED = "CLOSED"


class OutbreakStatus(str, Enum):
    OPEN = "OPEN"
    ACTIVE = "ACTIVE"
    CONTAINED = "CONTAINED"
    CLOSED = "CLOSED"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class VaccinationCampaignStatus(str, Enum):
    PLANNED = "PLANNED"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class SurveillanceVisitType(str, Enum):
    ACTIVE = "ACTIVE"
    PASSIVE = "PASSIVE"
    TARGETED = "TARGETED"


class SampleStatus(str, Enum):
    DRAFT = "DRAFT"
    COLLECTED = "COLLECTED"
    SUBMITTED_TO_LAB = "SUBMITTED_TO_LAB"
    RECEIVED_BY_LAB = "RECEIVED_BY_LAB"
    TESTED = "TESTED"


class LabTestResult(str, Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    INCONCLUSIVE = "INCONCLUSIVE"


class FieldOperationType(str, Enum):
    CULLING = "CULLING"
    DISINFECTION = "DISINFECTION"
    MOVEMENT_CONTROL = "MOVEMENT_CONTROL"
    EDUCATION = "EDUCATION"
    OTHER = "OTHER"


class GISOperationType(str, Enum):
    INSPECTION = "INSPECTION"
    SEIZURE = "SEIZURE"
    MOVEMENT = "MOVEMENT"
    OTHER = "OTHER"


class EpidemiologicalUnit(Base, TimestampMixin):
    __tablename__ = "epidemiological_units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    unit_type: Mapped[EpidemiologicalUnitType] = mapped_column(
        Enum(EpidemiologicalUnitType), nullable=False
    )

    province_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    county_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    village_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    population_cattle: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    population_sheep: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    population_goat: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    population_other: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    organization_unit_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("organization_units.id", ondelete="SET NULL"), nullable=True
    )

    organization_unit = relationship("OrganizationUnit", back_populates="epidemiological_units")

    disease_reports = relationship("DiseaseReport", back_populates="epidemiological_unit")
    outbreaks = relationship("DiseaseOutbreak", back_populates="epidemiological_unit")
    vaccination_operations = relationship(
        "VaccinationOperation", back_populates="epidemiological_unit"
    )
    surveillance_visits = relationship(
        "SurveillanceVisit", back_populates="epidemiological_unit"
    )
    samples = relationship("Sample", back_populates="epidemiological_unit")

    __table_args__ = (
        Index("ix_epidemiological_units_province_county", "province_id", "county_id"),
    )


class Disease(Base, TimestampMixin):
    __tablename__ = "diseases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, unique=True)
    category: Mapped[Optional[DiseaseCategory]] = mapped_column(
        Enum(DiseaseCategory), nullable=True
    )
    species_scope: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_strategic: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_reportable: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_zoonotic: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    reports = relationship("DiseaseReport", back_populates="disease")
    outbreaks = relationship("DiseaseOutbreak", back_populates="disease")
    vaccination_campaigns = relationship(
        "VaccinationCampaign", back_populates="disease"
    )


class DiseaseReport(Base, TimestampMixin):
    __tablename__ = "disease_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    disease_id: Mapped[int] = mapped_column(
        ForeignKey("diseases.id", ondelete="RESTRICT"), nullable=False
    )
    epidemiological_unit_id: Mapped[int] = mapped_column(
        ForeignKey("epidemiological_units.id", ondelete="RESTRICT"), nullable=False
    )
    reporting_unit_id: Mapped[int] = mapped_column(
        ForeignKey("organization_units.id", ondelete="RESTRICT"), nullable=False
    )
    reported_by_user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    report_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    disease_group: Mapped[Optional[DiseaseGroup]] = mapped_column(
        Enum(DiseaseGroup), nullable=True
    )
    status: Mapped[DiseaseReportStatus] = mapped_column(
        Enum(DiseaseReportStatus), default=DiseaseReportStatus.REPORTED, nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    suspected_animals_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    dead_animals_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    affected_species: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    first_seen_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    notification_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    disease = relationship("Disease", back_populates="reports")
    epidemiological_unit = relationship(
        "EpidemiologicalUnit", back_populates="disease_reports"
    )
    reporting_unit = relationship("OrganizationUnit", back_populates="disease_reports")
    reported_by_user = relationship("User", back_populates="disease_reports")

    outbreaks = relationship("DiseaseOutbreak", back_populates="source_report")
    samples = relationship("Sample", back_populates="disease_report")


class DiseaseOutbreak(Base, TimestampMixin):
    __tablename__ = "disease_outbreaks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    disease_id: Mapped[int] = mapped_column(
        ForeignKey("diseases.id", ondelete="RESTRICT"), nullable=False
    )
    epidemiological_unit_id: Mapped[int] = mapped_column(
        ForeignKey("epidemiological_units.id", ondelete="RESTRICT"), nullable=False
    )
    source_report_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("disease_reports.id", ondelete="SET NULL"), nullable=True
    )

    discovery_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    confirmation_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    status: Mapped[OutbreakStatus] = mapped_column(
        Enum(OutbreakStatus), default=OutbreakStatus.OPEN, nullable=False
    )
    risk_level: Mapped[Optional[RiskLevel]] = mapped_column(
        Enum(RiskLevel), nullable=True
    )

    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    total_cases: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_deaths: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    disease = relationship("Disease", back_populates="outbreaks")
    epidemiological_unit = relationship(
        "EpidemiologicalUnit", back_populates="outbreaks"
    )
    source_report = relationship("DiseaseReport", back_populates="outbreaks")
    field_operations = relationship(
        "FieldOperation", back_populates="disease_outbreak"
    )


class VaccinationCampaign(Base, TimestampMixin):
    __tablename__ = "vaccination_campaigns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    disease_id: Mapped[int] = mapped_column(
        ForeignKey("diseases.id", ondelete="RESTRICT"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    campaign_type: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    planned_start: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    planned_end: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    target_coverage_percent: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    status: Mapped[VaccinationCampaignStatus] = mapped_column(
        Enum(VaccinationCampaignStatus),
        default=VaccinationCampaignStatus.PLANNED,
        nullable=False,
    )

    disease = relationship("Disease", back_populates="vaccination_campaigns")
    operations = relationship(
        "VaccinationOperation", back_populates="campaign", cascade="all, delete-orphan"
    )


class VaccinationOperation(Base, TimestampMixin):
    __tablename__ = "vaccination_operations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("vaccination_campaigns.id", ondelete="CASCADE"), nullable=False
    )
    epidemiological_unit_id: Mapped[int] = mapped_column(
        ForeignKey("epidemiological_units.id", ondelete="RESTRICT"), nullable=False
    )
    operator_unit_id: Mapped[int] = mapped_column(
        ForeignKey("organization_units.id", ondelete="RESTRICT"), nullable=False
    )

    operation_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    animal_type: Mapped[str] = mapped_column(String(64), nullable=False)
    animal_count: Mapped[int] = mapped_column(Integer, nullable=False)
    vaccinated_count: Mapped[int] = mapped_column(Integer, nullable=False)

    vaccine_type: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    campaign = relationship("VaccinationCampaign", back_populates="operations")
    epidemiological_unit = relationship(
        "EpidemiologicalUnit", back_populates="vaccination_operations"
    )
    operator_unit = relationship("OrganizationUnit", back_populates="vaccination_operations")

    __table_args__ = (
        Index(
            "ix_vaccination_operations_campaign_date_unit",
            "campaign_id",
            "operation_date",
            "epidemiological_unit_id",
        ),
    )


class SurveillanceVisit(Base, TimestampMixin):
    __tablename__ = "surveillance_visits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    epidemiological_unit_id: Mapped[int] = mapped_column(
        ForeignKey("epidemiological_units.id", ondelete="RESTRICT"), nullable=False
    )
    visit_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    visit_type: Mapped[SurveillanceVisitType] = mapped_column(
        Enum(SurveillanceVisitType), nullable=False
    )

    performed_by_unit_id: Mapped[int] = mapped_column(
        ForeignKey("organization_units.id", ondelete="RESTRICT"), nullable=False
    )
    performed_by_user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    findings: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    follow_up_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    epidemiological_unit = relationship(
        "EpidemiologicalUnit", back_populates="surveillance_visits"
    )
    performed_by_unit = relationship("OrganizationUnit", back_populates="surveillance_visits")
    performed_by_user = relationship("User", back_populates="surveillance_visits")


class Sample(Base, TimestampMixin):
    __tablename__ = "samples"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    disease_report_id: Mapped[int] = mapped_column(
        ForeignKey("disease_reports.id", ondelete="CASCADE"), nullable=False
    )
    epidemiological_unit_id: Mapped[int] = mapped_column(
        ForeignKey("epidemiological_units.id", ondelete="RESTRICT"), nullable=False
    )

    sample_type: Mapped[str] = mapped_column(String(64), nullable=False)
    collection_date: Mapped[date] = mapped_column(Date, nullable=False)
    collected_by_user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    laboratory_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("organization_units.id", ondelete="SET NULL"), nullable=True
    )

    status: Mapped[SampleStatus] = mapped_column(
        Enum(SampleStatus), default=SampleStatus.DRAFT, nullable=False
    )

    disease_report = relationship("DiseaseReport", back_populates="samples")
    epidemiological_unit = relationship("EpidemiologicalUnit", back_populates="samples")
    collected_by_user = relationship("User", back_populates="samples_collected")
    laboratory = relationship("OrganizationUnit", back_populates="laboratory_samples")

    lab_tests = relationship("LaboratoryTest", back_populates="sample", cascade="all, delete-orphan")


class LaboratoryTest(Base, TimestampMixin):
    __tablename__ = "laboratory_tests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    sample_id: Mapped[int] = mapped_column(
        ForeignKey("samples.id", ondelete="CASCADE"), nullable=False
    )

    test_type: Mapped[str] = mapped_column(String(128), nullable=False)
    requested_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    result: Mapped[Optional[LabTestResult]] = mapped_column(
        Enum(LabTestResult), nullable=True
    )
    is_positive: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    sample = relationship("Sample", back_populates="lab_tests")


class FieldOperation(Base, TimestampMixin):
    __tablename__ = "field_operations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    disease_outbreak_id: Mapped[int] = mapped_column(
        ForeignKey("disease_outbreaks.id", ondelete="CASCADE"), nullable=False
    )

    operation_type: Mapped[FieldOperationType] = mapped_column(
        Enum(FieldOperationType), nullable=False
    )
    operation_date: Mapped[date] = mapped_column(Date, nullable=False)
    performed_by_unit_id: Mapped[int] = mapped_column(
        ForeignKey("organization_units.id", ondelete="RESTRICT"), nullable=False
    )
    performed_by_user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    disease_outbreak = relationship("DiseaseOutbreak", back_populates="field_operations")
    performed_by_unit = relationship("OrganizationUnit", back_populates="field_operations")
    performed_by_user = relationship("User", back_populates="field_operations")


class GISImportBatch(Base, TimestampMixin):
    __tablename__ = "gis_import_batches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_name: Mapped[str] = mapped_column(String(128), nullable=False)
    imported_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, index=True
    )
    file_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    record_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class GISInspectionRecord(Base, TimestampMixin):
    __tablename__ = "gis_inspection_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    batch_id: Mapped[int] = mapped_column(
        ForeignKey("gis_import_batches.id", ondelete="CASCADE"), nullable=False
    )

    certificate_number: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    certificate_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    registered_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    epidemiological_unit_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    epidemiological_unit_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    epidemiological_unit_type: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    province_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    county_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    source_unit_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    source_unit_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    source_unit_type: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    operation_type: Mapped[Optional[GISOperationType]] = mapped_column(
        Enum(GISOperationType), nullable=True
    )
    disease_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    animal_type: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    seizure_type: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    organ: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    quantity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    weight_kg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    batch = relationship("GISImportBatch", back_populates="records")


GISImportBatch.records = relationship(
    "GISInspectionRecord", back_populates="batch", cascade="all, delete-orphan"
)
