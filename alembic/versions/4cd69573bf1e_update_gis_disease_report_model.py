"""update gis disease report model

Revision ID: 4cd69573bf1e
Revises: 9e47d9b2362b
Create Date: 2026-08-04 17:35:51.863916

"""

from alembic import op


revision = "4cd69573bf1e"
down_revision = "9e47d9b2362b"
branch_labels = None
depends_on = None


def upgrade() -> None:

    # Rename existing columns (preserve data)
    op.alter_column(
        "gis_disease_reports",
        "start_date",
        new_column_name="disease_start_date",
    )

    op.alter_column(
        "gis_disease_reports",
        "dead_count",
        new_column_name="death_count",
    )

    op.alter_column(
        "gis_disease_reports",
        "old_information_id",
        new_column_name="old_system_id",
    )

    op.alter_column(
        "gis_disease_reports",
        "user_code",
        new_column_name="creator_user_code",
    )

    op.alter_column(
        "gis_disease_reports",
        "user_name",
        new_column_name="creator_user_name",
    )


def downgrade() -> None:

    # Reverse rename

    op.alter_column(
        "gis_disease_reports",
        "disease_start_date",
        new_column_name="start_date",
    )

    op.alter_column(
        "gis_disease_reports",
        "death_count",
        new_column_name="dead_count",
    )

    op.alter_column(
        "gis_disease_reports",
        "old_system_id",
        new_column_name="old_information_id",
    )

    op.alter_column(
        "gis_disease_reports",
        "creator_user_code",
        new_column_name="user_code",
    )

    op.alter_column(
        "gis_disease_reports",
        "creator_user_name",
        new_column_name="user_name",
    )