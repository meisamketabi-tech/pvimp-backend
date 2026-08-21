"""recreate gis laboratory results

Revision ID: ca1469091496
Revises: f23b350c5af0
Create Date: 2026-08-04 16:46:54.612349
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ca1469091496"
down_revision = "f23b350c5af0"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column(
        "gis_laboratory_results",
        sa.Column("answer_no", sa.String(100), nullable=True),
    )

    op.add_column(
        "gis_laboratory_results",
        sa.Column("epidemiology_unit_code", sa.String(50), nullable=True),
    )

    op.add_column(
        "gis_laboratory_results",
        sa.Column("epidemiology_unit_name", sa.String(255), nullable=True),
    )

    op.add_column(
        "gis_laboratory_results",
        sa.Column("epidemiology_unit_type", sa.String(100), nullable=True),
    )

    op.add_column(
        "gis_laboratory_results",
        sa.Column("province_code", sa.String(20), nullable=True),
    )

    op.add_column(
        "gis_laboratory_results",
        sa.Column("county_code", sa.String(20), nullable=True),
    )

    op.add_column(
        "gis_laboratory_results",
        sa.Column("disease_id", sa.Integer(), nullable=True),
    )

    op.add_column(
        "gis_laboratory_results",
        sa.Column("isolate_name_1", sa.String(255), nullable=True),
    )

    op.add_column(
        "gis_laboratory_results",
        sa.Column("isolate_name_2", sa.String(255), nullable=True),
    )

    op.add_column(
        "gis_laboratory_results",
        sa.Column("serotype_a", sa.String(50), nullable=True),
    )

    op.add_column(
        "gis_laboratory_results",
        sa.Column("serotype_o", sa.String(50), nullable=True),
    )

    op.add_column(
        "gis_laboratory_results",
        sa.Column("serotype_asia1", sa.String(50), nullable=True),
    )

    op.add_column(
        "gis_laboratory_results",
        sa.Column("unacceptable_cases", sa.String(500), nullable=True),
    )

    op.alter_column(
        "gis_laboratory_results",
        "laboratory_owner",
        existing_type=sa.String(length=255),
        type_=sa.String(length=100),
        existing_nullable=True,
    )

    op.create_index(
        "ix_gis_laboratory_results_disease_id",
        "gis_laboratory_results",
        ["disease_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_gis_laboratory_results_disease_id",
        "gis_laboratory_results",
        "gis_diseases",
        ["disease_id"],
        ["id"],
    )

    op.drop_column("gis_laboratory_results", "agent_a")
    op.drop_column("gis_laboratory_results", "agent_o")
    op.drop_column("gis_laboratory_results", "agent_asia1")
    op.drop_column("gis_laboratory_results", "isolated_agent_1")
    op.drop_column("gis_laboratory_results", "isolated_agent_2")
    op.drop_column("gis_laboratory_results", "answer_number")


def downgrade() -> None:

    op.add_column(
        "gis_laboratory_results",
        sa.Column("answer_number", sa.String(100), nullable=True),
    )

    op.add_column(
        "gis_laboratory_results",
        sa.Column("isolated_agent_2", sa.String(255), nullable=True),
    )

    op.add_column(
        "gis_laboratory_results",
        sa.Column("isolated_agent_1", sa.String(255), nullable=True),
    )

    op.add_column(
        "gis_laboratory_results",
        sa.Column("agent_a", sa.String(50), nullable=True),
    )

    op.add_column(
        "gis_laboratory_results",
        sa.Column("agent_o", sa.String(50), nullable=True),
    )

    op.add_column(
        "gis_laboratory_results",
        sa.Column("agent_asia1", sa.String(50), nullable=True),
    )

    op.drop_constraint(
        "fk_gis_laboratory_results_disease_id",
        "gis_laboratory_results",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_gis_laboratory_results_disease_id",
        table_name="gis_laboratory_results",
    )

    op.alter_column(
        "gis_laboratory_results",
        "laboratory_owner",
        existing_type=sa.String(length=100),
        type_=sa.String(length=255),
        existing_nullable=True,
    )

    op.drop_column("gis_laboratory_results", "unacceptable_cases")
    op.drop_column("gis_laboratory_results", "serotype_asia1")
    op.drop_column("gis_laboratory_results", "serotype_o")
    op.drop_column("gis_laboratory_results", "serotype_a")
    op.drop_column("gis_laboratory_results", "isolate_name_2")
    op.drop_column("gis_laboratory_results", "isolate_name_1")
    op.drop_column("gis_laboratory_results", "disease_id")
    op.drop_column("gis_laboratory_results", "county_code")
    op.drop_column("gis_laboratory_results", "province_code")
    op.drop_column("gis_laboratory_results", "epidemiology_unit_type")
    op.drop_column("gis_laboratory_results", "epidemiology_unit_name")
    op.drop_column("gis_laboratory_results", "epidemiology_unit_code")
    op.drop_column("gis_laboratory_results", "answer_no")