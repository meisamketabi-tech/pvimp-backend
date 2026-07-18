"""add inspection assignments table

Revision ID: e4a2ecb54c92
Revises: 6f0d200c013f
Create Date: 2026-07-18 11:04:38.673509

"""

from alembic import op
import sqlalchemy as sa


revision = "e4a2ecb54c92"
down_revision = "6f0d200c013f"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "inspection_assignments",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            "inspection_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "inspector_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "assigned_at",
            sa.DateTime(),
            nullable=True
        ),
    )


def downgrade() -> None:

    op.drop_table(
        "inspection_assignments"
    )