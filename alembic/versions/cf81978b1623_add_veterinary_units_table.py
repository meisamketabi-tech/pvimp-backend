"""add veterinary units table

Revision ID: cf81978b1623
Revises: e4a2ecb54c92
Create Date: 2026-07-18 12:46:46.427211

"""

from alembic import op
import sqlalchemy as sa


revision = 'cf81978b1623'
down_revision = 'e4a2ecb54c92'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        'veterinary_units',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('county_id', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ['county_id'],
            ['county.id'],
        ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        'ix_veterinary_units_code',
        'veterinary_units',
        ['code'],
        unique=True
    )

    op.create_index(
        'ix_veterinary_units_id',
        'veterinary_units',
        ['id'],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        'ix_veterinary_units_id',
        table_name='veterinary_units'
    )

    op.drop_index(
        'ix_veterinary_units_code',
        table_name='veterinary_units'
    )

    op.drop_table(
        'veterinary_units'
    )
