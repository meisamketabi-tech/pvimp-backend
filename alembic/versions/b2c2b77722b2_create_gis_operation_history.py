"""create gis operation history

Revision ID: b2c2b77722b2
Revises: 4efc217d548d
Create Date: 2026-08-04 16:25:12.342958

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b2c2b77722b2"
down_revision = "4efc217d548d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "gis_operation_history",
        sa.Column("id", sa.Integer(), primary_key=True),

        sa.Column("action_type_title", sa.String(), nullable=True),
        sa.Column("action_no", sa.String(), nullable=True),
        sa.Column("certificate_no", sa.String(), nullable=True),

        sa.Column("action_date", sa.Date(), nullable=True),

        sa.Column(
            "registered_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),

        sa.Column(
            "epidemiology_unit_id",
            sa.Integer(),
            sa.ForeignKey("gis_epidemiology_units.id"),
            nullable=True,
        ),

        sa.Column("epidemiology_unit_code", sa.String(), nullable=True),
        sa.Column("epidemiology_unit_name", sa.String(), nullable=True),
        sa.Column("epidemiology_unit_type", sa.String(), nullable=True),

        sa.Column("province_name", sa.String(), nullable=True),
        sa.Column("county_name", sa.String(), nullable=True),

        sa.Column("action_name", sa.String(), nullable=True),

        sa.Column("report_date", sa.Date(), nullable=True),

        sa.Column("report_info", sa.Text(), nullable=True),
    )

    op.create_index(
        "ix_gis_operation_history_id",
        "gis_operation_history",
        ["id"],
    )

    op.create_index(
        "ix_gis_operation_history_action_no",
        "gis_operation_history",
        ["action_no"],
    )

    op.create_index(
        "ix_gis_operation_history_action_type_title",
        "gis_operation_history",
        ["action_type_title"],
    )

    op.create_index(
        "ix_gis_operation_history_epidemiology_unit_id",
        "gis_operation_history",
        ["epidemiology_unit_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_gis_operation_history_epidemiology_unit_id",
        table_name="gis_operation_history",
    )

    op.drop_index(
        "ix_gis_operation_history_action_type_title",
        table_name="gis_operation_history",
    )

    op.drop_index(
        "ix_gis_operation_history_action_no",
        table_name="gis_operation_history",
    )

    op.drop_index(
        "ix_gis_operation_history_id",
        table_name="gis_operation_history",
    )

    op.drop_table("gis_operation_history")