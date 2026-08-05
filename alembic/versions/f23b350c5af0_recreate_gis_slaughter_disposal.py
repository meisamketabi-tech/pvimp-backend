"""recreate gis slaughter disposal

Revision ID: f23b350c5af0
Revises: ef792c037794
Create Date: 2026-08-04 16:43:06.235989
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f23b350c5af0"
down_revision = "ef792c037794"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("province_code", sa.String(length=20), nullable=True),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("province_name", sa.String(length=100), nullable=True),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("county_code", sa.String(length=20), nullable=True),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("county_name", sa.String(length=100), nullable=True),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("epidemiology_unit_code", sa.String(length=50), nullable=True),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("epidemiology_unit_name", sa.String(length=255), nullable=True),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("old_unit_code", sa.String(length=50), nullable=True),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("epidemiology_unit_type", sa.String(length=100), nullable=True),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("action_date", sa.Date(), nullable=True),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("total_animals", sa.Integer(), nullable=True),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("destroyed_count", sa.Integer(), nullable=True),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column(
            "estimated_compensation",
            sa.Numeric(18, 2),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("disease_name", sa.String(length=255), nullable=True),
    )

    op.alter_column(
        "gis_slaughter_disposals",
        "control_action_emha_detail_vcode",
        existing_type=sa.String(length=100),
        nullable=True,
    )

    op.create_index(
        "ix_gis_slaughter_disposals_control_action_emha_vcode",
        "gis_slaughter_disposals",
        ["control_action_emha_vcode"],
        unique=False,
    )

    op.drop_column(
        "gis_slaughter_disposals",
        "predicted_compensation_amount",
    )

    op.drop_column(
        "gis_slaughter_disposals",
        "disposed_count",
    )

    op.drop_column(
        "gis_slaughter_disposals",
        "description",
    )

    op.drop_column(
        "gis_slaughter_disposals",
        "latitude",
    )

    op.drop_column(
        "gis_slaughter_disposals",
        "existing_animal_count",
    )

    op.drop_column(
        "gis_slaughter_disposals",
        "slaughter_date",
    )

    op.drop_column(
        "gis_slaughter_disposals",
        "longitude",
    )


def downgrade() -> None:
    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("longitude", sa.Float(), nullable=True),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("slaughter_date", sa.Date(), nullable=True),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("existing_animal_count", sa.Integer(), nullable=True),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("latitude", sa.Float(), nullable=True),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("description", sa.Text(), nullable=True),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column("disposed_count", sa.Integer(), nullable=True),
    )

    op.add_column(
        "gis_slaughter_disposals",
        sa.Column(
            "predicted_compensation_amount",
            sa.Float(),
            nullable=True,
        ),
    )

    op.drop_index(
        "ix_gis_slaughter_disposals_control_action_emha_vcode",
        table_name="gis_slaughter_disposals",
    )

    op.alter_column(
        "gis_slaughter_disposals",
        "control_action_emha_detail_vcode",
        existing_type=sa.String(length=100),
        nullable=False,
    )

    op.drop_column("gis_slaughter_disposals", "disease_name")
    op.drop_column("gis_slaughter_disposals", "estimated_compensation")
    op.drop_column("gis_slaughter_disposals", "destroyed_count")
    op.drop_column("gis_slaughter_disposals", "total_animals")
    op.drop_column("gis_slaughter_disposals", "action_date")
    op.drop_column("gis_slaughter_disposals", "epidemiology_unit_type")
    op.drop_column("gis_slaughter_disposals", "old_unit_code")
    op.drop_column("gis_slaughter_disposals", "epidemiology_unit_name")
    op.drop_column("gis_slaughter_disposals", "epidemiology_unit_code")
    op.drop_column("gis_slaughter_disposals", "county_name")
    op.drop_column("gis_slaughter_disposals", "county_code")
    op.drop_column("gis_slaughter_disposals", "province_name")
    op.drop_column("gis_slaughter_disposals", "province_code")