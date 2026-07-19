"""create inspection assignment history table

Revision ID: 40bcc6f5fc9e
Revises: 41d39bcee9ac
Create Date: 2026-07-19

"""

from alembic import op
import sqlalchemy as sa


revision = "40bcc6f5fc9e"
down_revision = "41d39bcee9ac"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "inspection_assignment_histories",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True
        ),

        sa.Column(
            "inspection_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "assigned_from",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "assigned_to",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "changed_by",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "action",
            sa.String(50),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False
        ),
    )


def downgrade() -> None:

    op.drop_table(
        "inspection_assignment_histories"
    )
