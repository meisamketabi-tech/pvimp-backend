"""apply_model_changes

Revision ID: 678f8de2055a
Revises: e0373e1f11c1
Create Date: 2026-07-18 13:36:05.732574

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '678f8de2055a'
down_revision = 'e0373e1f11c1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()

    inspectionstatusenum = sa.Enum(
        'DRAFT',
        'SCHEDULED',
        'IN_PROGRESS',
        'COMPLETED',
        'CANCELLED',
        name='inspectionstatusenum'
    )

    inspectionresultenum = sa.Enum(
        'ACCEPTED',
        'REJECTED',
        'CONDITIONAL',
        'PENDING',
        name='inspectionresultenum'
    )

    inspectionstatusenum.create(bind, checkfirst=True)
    inspectionresultenum.create(bind, checkfirst=True)

    op.create_index(
        op.f('ix_checklist_items_id'),
        'checklist_items',
        ['id'],
        unique=False
    )

    op.create_index(
        op.f('ix_checklists_id'),
        'checklists',
        ['id'],
        unique=False
    )

    op.alter_column(
        'inspection_item_results',
        'created_at',
        existing_type=postgresql.TIMESTAMP(),
        nullable=False
    )

    op.create_index(
        op.f('ix_inspection_item_results_id'),
        'inspection_item_results',
        ['id'],
        unique=False
    )

    op.create_index(
        op.f('ix_inspection_types_id'),
        'inspection_types',
        ['id'],
        unique=False
    )

    op.alter_column(
        'inspections',
        'status',
        existing_type=sa.VARCHAR(length=50),
        type_=inspectionstatusenum,
        existing_nullable=False,
        postgresql_using="status::inspectionstatusenum"
    )

    op.alter_column(
        'inspections',
        'result',
        existing_type=sa.VARCHAR(length=50),
        type_=inspectionresultenum,
        existing_nullable=False,
        postgresql_using="result::inspectionresultenum"
    )

    op.alter_column(
        'inspections',
        'created_at',
        existing_type=postgresql.TIMESTAMP(),
        nullable=False
    )

    op.alter_column(
        'inspections',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(),
        nullable=False
    )

    op.drop_constraint(
        op.f('inspections_inspection_number_key'),
        'inspections',
        type_='unique'
    )

    op.create_index(
        op.f('ix_inspections_id'),
        'inspections',
        ['id'],
        unique=False
    )

    op.create_index(
        op.f('ix_inspections_inspection_number'),
        'inspections',
        ['inspection_number'],
        unique=True
    )

    op.create_foreign_key(
        None,
        'inspections',
        'organization_units',
        ['organization_unit_id'],
        ['id']
    )

    op.create_foreign_key(
        None,
        'inspections',
        'user_account',
        ['inspector_id'],
        ['id']
    )

    op.add_column(
        'user_assignments',
        sa.Column(
            'is_primary',
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        )
    )

    op.alter_column(
        'user_assignments',
        'is_primary',
        server_default=None
    )

    op.alter_column(
        'user_assignments',
        'start_date',
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        nullable=False
    )

    op.alter_column(
        'user_assignments',
        'end_date',
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=True
    )


def downgrade() -> None:

    op.alter_column(
        'user_assignments',
        'end_date',
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=True
    )

    op.alter_column(
        'user_assignments',
        'start_date',
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        nullable=True
    )

    op.drop_column(
        'user_assignments',
        'is_primary'
    )

    op.drop_constraint(
        None,
        'inspections',
        type_='foreignkey'
    )

    op.drop_constraint(
        None,
        'inspections',
        type_='foreignkey'
    )

    op.drop_index(
        op.f('ix_inspections_inspection_number'),
        table_name='inspections'
    )

    op.drop_index(
        op.f('ix_inspections_id'),
        table_name='inspections'
    )

    op.create_unique_constraint(
        op.f('inspections_inspection_number_key'),
        'inspections',
        ['inspection_number'],
        postgresql_nulls_not_distinct=False
    )

    op.alter_column(
        'inspections',
        'updated_at',
        existing_type=postgresql.TIMESTAMP(),
        nullable=True
    )

    op.alter_column(
        'inspections',
        'created_at',
        existing_type=postgresql.TIMESTAMP(),
        nullable=True
    )

    op.alter_column(
        'inspections',
        'result',
        existing_type=inspectionresultenum,
        type_=sa.VARCHAR(length=50),
        existing_nullable=False
    )

    op.alter_column(
        'inspections',
        'status',
        existing_type=inspectionstatusenum,
        type_=sa.VARCHAR(length=50),
        existing_nullable=False
    )

    op.drop_index(
        op.f('ix_inspection_types_id'),
        table_name='inspection_types'
    )

    op.drop_index(
        op.f('ix_inspection_item_results_id'),
        table_name='inspection_item_results'
    )

    op.alter_column(
        'inspection_item_results',
        'created_at',
        existing_type=postgresql.TIMESTAMP(),
        nullable=True
    )

    op.drop_index(
        op.f('ix_checklists_id'),
        table_name='checklists'
    )

    op.drop_index(
        op.f('ix_checklist_items_id'),
        table_name='checklist_items'
    )