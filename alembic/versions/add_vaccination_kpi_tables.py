"""add vaccination KPI snapshot and alert tables

Revision ID: add_vaccination_kpi_tables
Revises:
Create Date: 2026-08-12
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "add_vaccination_kpi_tables"
down_revision = "7d641e46407a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "gis_vaccination_kpi_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("snapshot_date", sa.Date(), nullable=False, index=True),
        sa.Column("province_code", sa.String(length=50), nullable=True, index=True),
        sa.Column("county_code", sa.String(length=50), nullable=True, index=True),
        sa.Column("unit_code", sa.String(length=100), nullable=True, index=True),
        sa.Column("vaccine_type", sa.String(length=255), nullable=True, index=True),
        sa.Column(
            "coverage_percent", sa.Numeric(10, 2), nullable=False, server_default="0"
        ),
        sa.Column("eligible_animals", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "vaccinated_animals", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column(
            "remaining_animals", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column("adverse_events", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "adverse_event_rate_percent",
            sa.Numeric(10, 2),
            nullable=False,
            server_default="0",
        ),
        sa.Column("effectiveness_signal", sa.String(length=50), nullable=True),
        sa.Column("metrics", postgresql.JSONB(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )

    op.create_table(
        "gis_vaccination_kpi_alerts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("snapshot_date", sa.Date(), nullable=False, index=True),
        sa.Column("severity", sa.String(length=30), nullable=False, index=True),
        sa.Column("alert_type", sa.String(length=80), nullable=False, index=True),
        sa.Column("province_code", sa.String(length=50), nullable=True, index=True),
        sa.Column("county_code", sa.String(length=50), nullable=True, index=True),
        sa.Column("unit_code", sa.String(length=100), nullable=True, index=True),
        sa.Column("vaccine_type", sa.String(length=255), nullable=True, index=True),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("details", postgresql.JSONB(), nullable=True),
        sa.Column(
            "is_resolved", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_table("gis_vaccination_kpi_alerts")
    op.drop_table("gis_vaccination_kpi_snapshots")
