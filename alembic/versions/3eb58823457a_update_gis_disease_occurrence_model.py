"""update gis disease occurrence model

Revision ID: 3eb58823457a
Revises: 0e31bcd9ce7d
Create Date: 2026-08-04 15:00:12.521266

"""

from alembic import op
import sqlalchemy as sa


revision = "3eb58823457a"
down_revision = "0e31bcd9ce7d"
branch_labels = None
depends_on = None


def upgrade() -> None:

    # -----------------------------------------
    # Animal Type Reference Table
    # -----------------------------------------

    op.create_table(
        "gis_animal_types",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "scientific_name",
            sa.String(length=150),
            nullable=True,
        ),
        sa.Column(
            "is_active",
            sa.Integer(),
            nullable=True,
            server_default="1",
        ),
        sa.UniqueConstraint(
            "title"
        ),
    )


    op.create_index(
        "ix_gis_animal_types_id",
        "gis_animal_types",
        ["id"],
    )


    # -----------------------------------------
    # Disease Occurrence Extensions
    # -----------------------------------------

    op.add_column(
        "gis_disease_occurrences",
        sa.Column(
            "occurrence_vcode",
            sa.String(length=100),
            nullable=True,
        ),
    )


    op.add_column(
        "gis_disease_occurrences",
        sa.Column(
            "province_id",
            sa.Integer(),
            nullable=True,
        ),
    )


    op.add_column(
        "gis_disease_occurrences",
        sa.Column(
            "county_id",
            sa.Integer(),
            nullable=True,
        ),
    )


    op.add_column(
        "gis_disease_occurrences",
        sa.Column(
            "province_name",
            sa.String(length=100),
            nullable=True,
        ),
    )


    op.add_column(
        "gis_disease_occurrences",
        sa.Column(
            "county_name",
            sa.String(length=100),
            nullable=True,
        ),
    )


    op.add_column(
        "gis_disease_occurrences",
        sa.Column(
            "disease_start_date",
            sa.Date(),
            nullable=True,
        ),
    )


    op.add_column(
        "gis_disease_occurrences",
        sa.Column(
            "animal_type_id",
            sa.Integer(),
            nullable=True,
        ),
    )


    op.add_column(
        "gis_disease_occurrences",
        sa.Column(
            "risk_animals_count",
            sa.Integer(),
            server_default="0",
        ),
    )


    op.add_column(
        "gis_disease_occurrences",
        sa.Column(
            "total_animals_count",
            sa.Integer(),
            server_default="0",
        ),
    )


    op.add_column(
        "gis_disease_occurrences",
        sa.Column(
            "slaughtered_animals_count",
            sa.Integer(),
            server_default="0",
        ),
    )


    op.add_column(
        "gis_disease_occurrences",
        sa.Column(
            "affected_animals_count",
            sa.Integer(),
            server_default="0",
        ),
    )


    op.add_column(
        "gis_disease_occurrences",
        sa.Column(
            "dead_animals_count",
            sa.Integer(),
            server_default="0",
        ),
    )


    op.add_column(
        "gis_disease_occurrences",
        sa.Column(
            "sample_taken",
            sa.Boolean(),
            server_default="false",
        ),
    )


    op.add_column(
        "gis_disease_occurrences",
        sa.Column(
            "old_system_id",
            sa.String(length=100),
            nullable=True,
        ),
    )


    # -----------------------------------------
    # Indexes
    # -----------------------------------------

    op.create_index(
        "ix_gis_disease_occurrences_occurrence_vcode",
        "gis_disease_occurrences",
        ["occurrence_vcode"],
    )


    op.create_index(
        "ix_gis_disease_occurrences_province_id",
        "gis_disease_occurrences",
        ["province_id"],
    )


    op.create_index(
        "ix_gis_disease_occurrences_county_id",
        "gis_disease_occurrences",
        ["county_id"],
    )


    op.create_index(
        "ix_gis_disease_occurrences_animal_type_id",
        "gis_disease_occurrences",
        ["animal_type_id"],
    )


    op.create_index(
        "ix_gis_disease_occurrences_old_system_id",
        "gis_disease_occurrences",
        ["old_system_id"],
    )


    # -----------------------------------------
    # Foreign Keys
    # -----------------------------------------

    op.create_foreign_key(
        "fk_occurrence_animal_type",
        "gis_disease_occurrences",
        "gis_animal_types",
        ["animal_type_id"],
        ["id"],
    )


    op.create_foreign_key(
        "fk_occurrence_province",
        "gis_disease_occurrences",
        "gis_provinces",
        ["province_id"],
        ["id"],
    )


    op.create_foreign_key(
        "fk_occurrence_county",
        "gis_disease_occurrences",
        "gis_counties",
        ["county_id"],
        ["id"],
    )



def downgrade() -> None:

    op.drop_constraint(
        "fk_occurrence_county",
        "gis_disease_occurrences",
        type_="foreignkey",
    )

    op.drop_constraint(
        "fk_occurrence_province",
        "gis_disease_occurrences",
        type_="foreignkey",
    )

    op.drop_constraint(
        "fk_occurrence_animal_type",
        "gis_disease_occurrences",
        type_="foreignkey",
    )


    op.drop_index(
        "ix_gis_disease_occurrences_old_system_id",
        table_name="gis_disease_occurrences",
    )

    op.drop_index(
        "ix_gis_disease_occurrences_animal_type_id",
        table_name="gis_disease_occurrences",
    )

    op.drop_index(
        "ix_gis_disease_occurrences_county_id",
        table_name="gis_disease_occurrences",
    )

    op.drop_index(
        "ix_gis_disease_occurrences_province_id",
        table_name="gis_disease_occurrences",
    )

    op.drop_index(
        "ix_gis_disease_occurrences_occurrence_vcode",
        table_name="gis_disease_occurrences",
    )


    columns = [
        "old_system_id",
        "sample_taken",
        "dead_animals_count",
        "affected_animals_count",
        "slaughtered_animals_count",
        "total_animals_count",
        "risk_animals_count",
        "animal_type_id",
        "disease_start_date",
        "county_name",
        "province_name",
        "county_id",
        "province_id",
        "occurrence_vcode",
    ]


    for column in columns:
        op.drop_column(
            "gis_disease_occurrences",
            column,
        )


    op.drop_index(
        "ix_gis_animal_types_id",
        table_name="gis_animal_types",
    )

    op.drop_table(
        "gis_animal_types"
    )