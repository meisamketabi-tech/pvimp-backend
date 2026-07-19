"""enhance inspection assignment workflow

Revision ID: 41d39bcee9ac
Revises: 7868632dfff0
Create Date: 2026-07-19 12:00:56.976306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41d39bcee9ac'
down_revision = '7868632dfff0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'inspection_assignments',
        sa.Column('assigned_by', sa.Integer(), nullable=True)
    )

    op.add_column(
        'inspection_assignments',
        sa.Column('unassigned_at', sa.DateTime(), nullable=True)
    )

    op.add_column(
        'inspection_assignments',
        sa.Column('note', sa.Text(), nullable=True)
    )

    op.create_foreign_key(
        None,
        'inspection_assignments',
        'user_account',
        ['assigned_by'],
        ['id']
    )


def downgrade() -> None:
    op.drop_constraint(
        None,
        'inspection_assignments',
        type_='foreignkey'
    )

    op.drop_column(
        'inspection_assignments',
        'note'
    )

    op.drop_column(
        'inspection_assignments',
        'unassigned_at'
    )

    op.drop_column(
        'inspection_assignments',
        'assigned_by'
    )
