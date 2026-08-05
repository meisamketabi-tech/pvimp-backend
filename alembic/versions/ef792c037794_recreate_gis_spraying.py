"""recreate gis spraying

Revision ID: ef792c037794
Revises: b2c2b77722b2
Create Date: 2026-08-04 16:37:50.036739

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ef792c037794"
down_revision = "b2c2b77722b2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "gis_spraying",
        sa.Column("spraying_vcode", sa.String(length=100), nullable=True),
    )

    op.add_column(
        "gis_spraying",
        sa.Column("province_code", sa.String(length=20), nullable=True),
    )

    op.add_column(
        "gis_spraying",
        sa.Column("county_code", sa.String(length=20), nullable=True),
    )

    op.add_column(
        "gis_spraying",
        sa.Column("epidemiology_unit_code", sa.String(length=50), nullable=True),
    )

    op.add_column(
        "gis_spraying",
        sa.Column("epidemiology_unit_name", sa.String(length=255), nullable=True),
    )

    op.add_column(
        "gis_spraying",
        sa.Column("epidemiology_unit_type", sa.String(length=100), nullable=True),
    )

    op.add_column(
        "gis_spraying",
        sa.Column("plan_type", sa.String(length=100), nullable=True),
    )

    op.add_column(
        "gis_spraying",
        sa.Column("operation_type", sa.String(length=100), nullable=True),
    )

    op.add_column(
        "gis_spraying",
        sa.Column("poison_type", sa.String(length=200), nullable=True),
    )

    op.add_column(
        "gis_spraying",
        sa.Column("sprayed_animal_count", sa.Integer(), nullable=True),
    )

    op.add_column(
        "gis_spraying",
        sa.Column("total_animals", sa.Integer(), nullable=True),
    )

    op.alter_column(
        "gis_spraying",
        "epidemiology_unit_id",
        existing_type=sa.Integer(),
        nullable=True,
    )

    op.drop_index(
        "ix_gis_spraying_spraying_no",
        table_name="gis_spraying",
    )

    op.create_index(
        "ix_gis_spraying_spraying_vcode",
        "gis_spraying",
        ["spraying_vcode"],
        unique=True,
    )

    op.drop_column("gis_spraying", "sprayed_animals")
    op.drop_column("gis_spraying", "pesticide_type")
    op.drop_column("gis_spraying", "spraying_no")
    op.drop_column("gis_spraying", "spraying_operation_type")
    op.drop_column("gis_spraying", "current_animals")
    op.drop_column("gis_spraying", "project_type")


def downgrade() -> None:
    op.add_column(
        "gis_spraying",
        sa.Column("project_type", sa.String(length=100), nullable=True),
    )

    op.add_column(
        "gis_spraying",
        sa.Column("current_animals", sa.Integer(), nullable=True),
    )

    op.add_column(
        "gis_spraying",
        sa.Column("spraying_operation_type", sa.String(length=100), nullable=True),
    )

    op.add_column(
        "gis_spraying",
        sa.Column("spraying_no", sa.String(length=100), nullable=False),
    )

    op.add_column(
        "gis_spraying",
        sa.Column("pesticide_type", sa.String(length=200), nullable=True),
    )

    op.add_column(
        "gis_spraying",
        sa.Column("sprayed_animals", sa.Integer(), nullable=True),
    )

    op.drop_index(
        "ix_gis_spraying_spraying_vcode",
        table_name="gis_spraying",
    )

    op.create_index(
        "ix_gis_spraying_spraying_no",
        "gis_spraying",
        ["spraying_no"],
        unique=True,
    )

    op.alter_column(
        "gis_spraying",
        "epidemiology_unit_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.drop_column("gis_spraying", "total_animals")
    op.drop_column("gis_spraying", "sprayed_animal_count")
    op.drop_column("gis_spraying", "poison_type")
    op.drop_column("gis_spraying", "operation_type")
    op.drop_column("gis_spraying", "plan_type")
    op.drop_column("gis_spraying", "epidemiology_unit_type")
    op.drop_column("gis_spraying", "epidemiology_unit_name")
    op.drop_column("gis_spraying", "epidemiology_unit_code")
    op.drop_column("gis_spraying", "county_code")
    op.drop_column("gis_spraying", "province_code")
    op.drop_column("gis_spraying", "spraying_vcode")