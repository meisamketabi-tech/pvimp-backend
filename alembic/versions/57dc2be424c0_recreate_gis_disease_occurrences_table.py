"""recreate gis disease occurrences table

Revision ID: 57dc2be424c0
Revises: 3eb58823457a
Create Date: 2026-08-04 15:27:07.709181

"""

from alembic import op
import sqlalchemy as sa


revision = "57dc2be424c0"
down_revision = "3eb58823457a"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.drop_table(
        "gis_disease_occurrences"
    )

    op.create_table(
        "gis_disease_occurrences",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            index=True,
        ),

        sa.Column(
            "occurrence_vcode",
            sa.String(length=100),
            unique=True,
            index=True,
        ),

        sa.Column(
            "epidemiology_unit_id",
            sa.Integer(),
            sa.ForeignKey(
                "gis_epidemiology_units.id"
            ),
            nullable=False,
            index=True,
        ),

        sa.Column(
            "unit_name",
            sa.String(length=255),
        ),

        sa.Column(
            "disease_id",
            sa.Integer(),
            sa.ForeignKey(
                "gis_diseases.id"
            ),
            nullable=False,
            index=True,
        ),

        sa.Column(
            "province_id",
            sa.Integer(),
            sa.ForeignKey(
                "gis_provinces.id"
            ),
            nullable=True,
            index=True,
        ),

        sa.Column(
            "county_id",
            sa.Integer(),
            sa.ForeignKey(
                "gis_counties.id"
            ),
            nullable=True,
            index=True,
        ),

        sa.Column(
            "province_name",
            sa.String(length=100),
        ),

        sa.Column(
            "county_name",
            sa.String(length=100),
        ),

        sa.Column(
            "animal_type_id",
            sa.Integer(),
            sa.ForeignKey(
                "gis_animal_types.id"
            ),
            nullable=True,
            index=True,
        ),

        sa.Column(
            "disease_start_date",
            sa.Date(),
        ),

        sa.Column(
            "report_date",
            sa.Date(),
        ),

        sa.Column(
            "registered_at",
            sa.DateTime(),
            server_default=sa.func.now(),
        ),

        sa.Column(
            "risk_animals_count",
            sa.Integer(),
            default=0,
        ),

        sa.Column(
            "total_animals_count",
            sa.Integer(),
            default=0,
        ),

        sa.Column(
            "affected_animals_count",
            sa.Integer(),
            default=0,
        ),

        sa.Column(
            "dead_animals_count",
            sa.Integer(),
            default=0,
        ),

        sa.Column(
            "slaughtered_animals_count",
            sa.Integer(),
            default=0,
        ),

        sa.Column(
            "sample_taken",
            sa.Boolean(),
            default=False,
        ),

        sa.Column(
            "report_number",
            sa.String(length=100),
            index=True,
        ),

        sa.Column(
            "report_info",
            sa.Text(),
        ),

        sa.Column(
            "user_code",
            sa.String(length=50),
        ),

        sa.Column(
            "user_name",
            sa.String(length=100),
        ),

        sa.Column(
            "expert_names",
            sa.String(length=255),
        ),

        sa.Column(
            "latitude",
            sa.Float(),
        ),

        sa.Column(
            "longitude",
            sa.Float(),
        ),

        sa.Column(
            "window_code",
            sa.String(length=100),
        ),

        sa.Column(
            "operation_license_type",
            sa.String(length=255),
        ),

        sa.Column(
            "status",
            sa.String(length=50),
        ),

        sa.Column(
            "old_system_id",
            sa.String(length=100),
            index=True,
        ),

        sa.Column(
            "description",
            sa.Text(),
        ),
    )


def downgrade() -> None:

    op.drop_table(
        "gis_disease_occurrences"
    )