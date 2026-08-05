"""add gis vaccine disposal

Revision ID: 0e9a1e1b1f49
Revises: 4cd69573bf1e
Create Date: 2026-08-04 19:24:49.001001

"""

from alembic import op
import sqlalchemy as sa


revision = "0e9a1e1b1f49"
down_revision = "4cd69573bf1e"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "gis_vaccine_disposals",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            index=True
        ),

        # Distribution identity
        sa.Column(
            "distribution_vaccine_center_vcode",
            sa.String(),
            index=True
        ),

        sa.Column(
            "distribution_no",
            sa.String(100)
        ),


        # Epidemiology unit
        sa.Column(
            "epidemiology_unit_id",
            sa.Integer(),
            sa.ForeignKey(
                "gis_epidemiology_units.id"
            ),
            index=True
        ),

        sa.Column(
            "province_name",
            sa.String()
        ),

        sa.Column(
            "county_name",
            sa.String()
        ),


        # Distribution information

        sa.Column(
            "distribution_date",
            sa.Date()
        ),

        sa.Column(
            "distribution_status_id",
            sa.Integer()
        ),


        # Destination

        sa.Column(
            "destination_province",
            sa.String()
        ),

        sa.Column(
            "destination_county",
            sa.String()
        ),

        sa.Column(
            "destination_unit_code",
            sa.String()
        ),

        sa.Column(
            "destination_unit_name",
            sa.String()
        ),

        sa.Column(
            "destination_unit_type",
            sa.String()
        ),


        # Vaccine

        sa.Column(
            "vaccine_type",
            sa.String()
        ),

        sa.Column(
            "vaccine_brand",
            sa.String()
        ),

        sa.Column(
            "manufacturer",
            sa.String()
        ),

        sa.Column(
            "batch_number",
            sa.String()
        ),

        sa.Column(
            "vaccine_shape",
            sa.String()
        ),


        # Quantity

        sa.Column(
            "package_count",
            sa.Integer()
        ),

        sa.Column(
            "dose_volume",
            sa.Float()
        ),


        # Unit/User

        sa.Column(
            "unit_name",
            sa.String()
        ),

        sa.Column(
            "user_code",
            sa.String()
        ),

        sa.Column(
            "user_name",
            sa.String()
        ),


        sa.Column(
            "registration_date",
            sa.Date()
        ),


        # Disposal specific

        sa.Column(
            "disposal_status",
            sa.String(100)
        ),

        sa.Column(
            "disposal_date",
            sa.Date()
        ),

        sa.Column(
            "disposal_reason",
            sa.String(500)
        ),

    )


def downgrade() -> None:

    op.drop_table(
        "gis_vaccine_disposals"
    )