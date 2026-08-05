"""refactor gis enable care

Revision ID: 9e47d9b2362b
Revises: c15c6f50840f
Create Date: 2026-08-04 17:20:50.137417

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e47d9b2362b'
down_revision = 'c15c6f50840f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'gis_enable_cares',
        sa.Column(
            'epidemiology_unit_code',
            sa.String(length=50),
            nullable=True
        )
    )

    op.add_column(
        'gis_enable_cares',
        sa.Column(
            'epidemiology_unit_type',
            sa.String(length=100),
            nullable=True
        )
    )

    op.add_column(
        'gis_enable_cares',
        sa.Column(
            'care_type',
            sa.String(length=255),
            nullable=True
        )
    )

    op.alter_column(
        'gis_enable_cares',
        'province_code',
        existing_type=sa.VARCHAR(length=50),
        type_=sa.String(length=20),
        existing_nullable=True
    )

    op.alter_column(
        'gis_enable_cares',
        'county_code',
        existing_type=sa.VARCHAR(length=50),
        type_=sa.String(length=20),
        existing_nullable=True
    )

    op.alter_column(
        'gis_enable_cares',
        'old_unit_code',
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=50),
        existing_nullable=True
    )

    op.create_index(
        op.f('ix_gis_enable_cares_old_system_id'),
        'gis_enable_cares',
        ['old_system_id'],
        unique=False
    )

    op.drop_column(
        'gis_enable_cares',
        'unit_type_name'
    )

    op.drop_column(
        'gis_enable_cares',
        'surveillance_type'
    )


def downgrade() -> None:
    op.add_column(
        'gis_enable_cares',
        sa.Column(
            'surveillance_type',
            sa.VARCHAR(length=255),
            nullable=True
        )
    )

    op.add_column(
        'gis_enable_cares',
        sa.Column(
            'unit_type_name',
            sa.VARCHAR(length=100),
            nullable=True
        )
    )

    op.drop_index(
        op.f('ix_gis_enable_cares_old_system_id'),
        table_name='gis_enable_cares'
    )

    op.alter_column(
        'gis_enable_cares',
        'old_unit_code',
        existing_type=sa.String(length=50),
        type_=sa.VARCHAR(length=100),
        existing_nullable=True
    )

    op.alter_column(
        'gis_enable_cares',
        'county_code',
        existing_type=sa.String(length=20),
        type_=sa.VARCHAR(length=50),
        existing_nullable=True
    )

    op.alter_column(
        'gis_enable_cares',
        'province_code',
        existing_type=sa.String(length=20),
        type_=sa.VARCHAR(length=50),
        existing_nullable=True
    )

    op.drop_column(
        'gis_enable_cares',
        'care_type'
    )

    op.drop_column(
        'gis_enable_cares',
        'epidemiology_unit_type'
    )

    op.drop_column(
        'gis_enable_cares',
        'epidemiology_unit_code'
    )