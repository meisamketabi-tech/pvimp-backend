"""recreate gis send sample details

Revision ID: 2402c02b4868
Revises: ca1469091496
Create Date: 2026-08-04 16:57:26.306835

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2402c02b4868"
down_revision = "ca1469091496"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ------------------------------------------------------------------
    # GIS Send Sample Details
    # ------------------------------------------------------------------

    op.add_column(
        "gis_send_sample_details",
        sa.Column("epidemiology_unit_code", sa.String(length=50), nullable=True),
    )

    op.add_column(
        "gis_send_sample_details",
        sa.Column("epidemiology_unit_type", sa.String(length=100), nullable=True),
    )

    op.add_column(
        "gis_send_sample_details",
        sa.Column("disease_id", sa.Integer(), nullable=True),
    )

    op.add_column(
        "gis_send_sample_details",
        sa.Column("disease_name", sa.String(length=255), nullable=True),
    )

    op.alter_column(
        "gis_send_sample_details",
        "province_code",
        existing_type=sa.String(length=50),
        type_=sa.String(length=20),
        existing_nullable=True,
    )

    op.alter_column(
        "gis_send_sample_details",
        "county_code",
        existing_type=sa.String(length=50),
        type_=sa.String(length=20),
        existing_nullable=True,
    )

    op.create_index(
        "ix_gis_send_sample_details_disease_id",
        "gis_send_sample_details",
        ["disease_id"],
    )

    op.create_foreign_key(
        "fk_gis_send_sample_details_disease_id",
        "gis_send_sample_details",
        "gis_diseases",
        ["disease_id"],
        ["id"],
    )

    op.drop_column(
        "gis_send_sample_details",
        "unit_type_name",
    )

    op.drop_column(
        "gis_send_sample_details",
        "disease_or_surveillance_type",
    )


def downgrade() -> None:
    op.add_column(
        "gis_send_sample_details",
        sa.Column(
            "disease_or_surveillance_type",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_send_sample_details",
        sa.Column(
            "unit_type_name",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.drop_constraint(
        "fk_gis_send_sample_details_disease_id",
        "gis_send_sample_details",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_gis_send_sample_details_disease_id",
        table_name="gis_send_sample_details",
    )

    op.alter_column(
        "gis_send_sample_details",
        "county_code",
        existing_type=sa.String(length=20),
        type_=sa.String(length=50),
        existing_nullable=True,
    )

    op.alter_column(
        "gis_send_sample_details",
        "province_code",
        existing_type=sa.String(length=20),
        type_=sa.String(length=50),
        existing_nullable=True,
    )

    op.drop_column("gis_send_sample_details", "disease_name")
    op.drop_column("gis_send_sample_details", "disease_id")
    op.drop_column("gis_send_sample_details", "epidemiology_unit_type")
    op.drop_column("gis_send_sample_details", "epidemiology_unit_code")