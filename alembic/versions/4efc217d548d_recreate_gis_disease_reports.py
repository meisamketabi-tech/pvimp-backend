"""recreate gis disease reports

Revision ID: 4efc217d548d
Revises: 57dc2be424c0
Create Date: 2026-08-04 15:58:44.099693
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4efc217d548d"
down_revision = "57dc2be424c0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table("gis_disease_reports")

    op.create_table(
        "gis_disease_reports",

        sa.Column("id", sa.Integer(), primary_key=True),

        sa.Column("observation_detail_vcode", sa.String()),
        sa.Column("observation_vcode", sa.String()),

        sa.Column("province_code", sa.String()),
        sa.Column("province_name", sa.String()),

        sa.Column("county_code", sa.String()),
        sa.Column("county_name", sa.String()),

        sa.Column(
            "epidemiology_unit_id",
            sa.Integer(),
            sa.ForeignKey("gis_epidemiology_units.id"),
            nullable=True,
        ),

        sa.Column("epidemiology_unit_code", sa.String()),
        sa.Column("epidemiology_unit_name", sa.String()),
        sa.Column("epidemiology_unit_type", sa.String()),

        sa.Column(
            "disease_id",
            sa.Integer(),
            sa.ForeignKey("gis_diseases.id"),
            nullable=True,
        ),

        sa.Column("disease_name", sa.String()),

        sa.Column("animal_type", sa.String()),

        sa.Column("start_date", sa.Date()),

        sa.Column("total_animals", sa.Integer()),
        sa.Column("infected_count", sa.Integer()),
        sa.Column("dead_count", sa.Integer()),
        sa.Column("slaughtered_count", sa.Integer()),
        sa.Column("destroyed_count", sa.Integer()),

        sa.Column("sampling", sa.String()),

        sa.Column("old_information_id", sa.String()),
        sa.Column("age_group", sa.String()),
        sa.Column("old_unit_code", sa.String()),

        sa.Column("biting_animal", sa.String()),

        sa.Column("user_code", sa.String()),
        sa.Column("user_name", sa.String()),

        sa.Column("operation_license_type", sa.String()),

        sa.Column("source_unit_code", sa.String()),
        sa.Column("source_unit_name", sa.String()),
        sa.Column("source_unit_type", sa.String()),
    )

    op.create_index(
        "ix_gis_disease_reports_id",
        "gis_disease_reports",
        ["id"],
    )

    op.create_index(
        "ix_gis_disease_reports_observation_detail_vcode",
        "gis_disease_reports",
        ["observation_detail_vcode"],
    )

    op.create_index(
        "ix_gis_disease_reports_observation_vcode",
        "gis_disease_reports",
        ["observation_vcode"],
    )

    op.create_index(
        "ix_gis_disease_reports_epidemiology_unit_id",
        "gis_disease_reports",
        ["epidemiology_unit_id"],
    )

    op.create_index(
        "ix_gis_disease_reports_disease_id",
        "gis_disease_reports",
        ["disease_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_gis_disease_reports_disease_id")
    op.drop_index("ix_gis_disease_reports_epidemiology_unit_id")
    op.drop_index("ix_gis_disease_reports_observation_vcode")
    op.drop_index("ix_gis_disease_reports_observation_detail_vcode")
    op.drop_index("ix_gis_disease_reports_id")

    op.drop_table("gis_disease_reports")