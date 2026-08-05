"""refactor gis disease occurrence

Revision ID: 53484d4e7583
Revises: 2402c02b4868
Create Date: 2026-08-04 17:02:50.883217

"""

from alembic import op
import sqlalchemy as sa

revision = "53484d4e7583"
down_revision = "2402c02b4868"
branch_labels = None
depends_on = None


def upgrade():

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("observation_detail_vcode", sa.String(100), nullable=True),
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("observation_vcode", sa.String(100), nullable=True),
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("province_code", sa.String(20), nullable=True),
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("county_code", sa.String(20), nullable=True),
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("epidemiology_unit_code", sa.String(50), nullable=True),
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("epidemiology_unit_name", sa.String(255), nullable=True),
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("epidemiology_unit_type", sa.String(100), nullable=True),
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("disease_name", sa.String(255), nullable=True),
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("animal_type", sa.String(100), nullable=True),
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("total_animals", sa.Integer(), nullable=True),
    )

    op.alter_column(
        "gis_disease_occurrences",
        "epidemiology_unit_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )

    op.alter_column(
        "gis_disease_occurrences",
        "disease_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )

    op.drop_index(
        op.f("ix_gis_disease_occurrences_animal_type_id"),
        table_name="gis_disease_occurrences",
    )

    op.drop_index(
        op.f("ix_gis_disease_occurrences_occurrence_vcode"),
        table_name="gis_disease_occurrences",
    )

    op.create_index(
        op.f("ix_gis_disease_occurrences_observation_detail_vcode"),
        "gis_disease_occurrences",
        ["observation_detail_vcode"],
        unique=True,
    )

    op.create_index(
        op.f("ix_gis_disease_occurrences_observation_vcode"),
        "gis_disease_occurrences",
        ["observation_vcode"],
        unique=False,
    )

    op.drop_constraint(
        op.f("gis_disease_occurrences_animal_type_id_fkey"),
        "gis_disease_occurrences",
        type_="foreignkey",
    )

    op.drop_column("gis_disease_occurrences", "affected_animals_count")
    op.drop_column("gis_disease_occurrences", "animal_type_id")
    op.drop_column("gis_disease_occurrences", "unit_name")
    op.drop_column("gis_disease_occurrences", "disease_start_date")
    op.drop_column("gis_disease_occurrences", "risk_animals_count")
    op.drop_column("gis_disease_occurrences", "occurrence_vcode")
    op.drop_column("gis_disease_occurrences", "total_animals_count")
    op.drop_column("gis_disease_occurrences", "slaughtered_animals_count")
    op.drop_column("gis_disease_occurrences", "dead_animals_count")


def downgrade():

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("dead_animals_count", sa.Integer(), nullable=True),
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("slaughtered_animals_count", sa.Integer(), nullable=True),
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("total_animals_count", sa.Integer(), nullable=True),
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("occurrence_vcode", sa.String(100), nullable=True),
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("risk_animals_count", sa.Integer(), nullable=True),
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("disease_start_date", sa.Date(), nullable=True),
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("unit_name", sa.String(255), nullable=True),
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("animal_type_id", sa.Integer(), nullable=True),
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("affected_animals_count", sa.Integer(), nullable=True),
    )

    op.create_foreign_key(
        op.f("gis_disease_occurrences_animal_type_id_fkey"),
        "gis_disease_occurrences",
        "gis_animal_types",
        ["animal_type_id"],
        ["id"],
    )

    op.drop_index(
        op.f("ix_gis_disease_occurrences_observation_vcode"),
        table_name="gis_disease_occurrences",
    )

    op.drop_index(
        op.f("ix_gis_disease_occurrences_observation_detail_vcode"),
        table_name="gis_disease_occurrences",
    )

    op.create_index(
        op.f("ix_gis_disease_occurrences_occurrence_vcode"),
        "gis_disease_occurrences",
        ["occurrence_vcode"],
        unique=True,
    )

    op.create_index(
        op.f("ix_gis_disease_occurrences_animal_type_id"),
        "gis_disease_occurrences",
        ["animal_type_id"],
    )

    op.alter_column(
        "gis_disease_occurrences",
        "disease_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )

    op.alter_column(
        "gis_disease_occurrences",
        "epidemiology_unit_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )

    op.drop_column("gis_disease_occurrences", "total_animals")
    op.drop_column("gis_disease_occurrences", "animal_type")
    op.drop_column("gis_disease_occurrences", "disease_name")
    op.drop_column("gis_disease_occurrences", "epidemiology_unit_type")
    op.drop_column("gis_disease_occurrences", "epidemiology_unit_name")
    op.drop_column("gis_disease_occurrences", "epidemiology_unit_code")
    op.drop_column("gis_disease_occurrences", "county_code")
    op.drop_column("gis_disease_occurrences", "province_code")
    op.drop_column("gis_disease_occurrences", "observation_vcode")
    op.drop_column("gis_disease_occurrences", "observation_detail_vcode")