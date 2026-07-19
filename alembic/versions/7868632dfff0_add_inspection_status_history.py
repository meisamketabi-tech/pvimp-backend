from alembic import op
import sqlalchemy as sa


revision = '7868632dfff0'
down_revision = '3f62b209a74a'
branch_labels = None
depends_on = None


inspection_status_enum = sa.Enum(
    'DRAFT',
    'SCHEDULED',
    'IN_PROGRESS',
    'COMPLETED',
    'CANCELLED',
    name='inspectionstatusenum'
)


def upgrade() -> None:

    op.create_table(
        'inspection_status_history',

        sa.Column(
            'id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'inspection_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'old_status',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'new_status',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'changed_by',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'changed_at',
            sa.DateTime(),
            nullable=False
        ),

        sa.Column(
            'note',
            sa.Text(),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ['changed_by'],
            ['user_account.id']
        ),

        sa.ForeignKeyConstraint(
            ['inspection_id'],
            ['inspections.id']
        ),

        sa.PrimaryKeyConstraint('id')
    )


    op.create_index(
        'ix_inspection_status_history_id',
        'inspection_status_history',
        ['id'],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        'ix_inspection_status_history_id',
        table_name='inspection_status_history'
    )

    op.drop_table(
        'inspection_status_history'
    )
