"""merge vaccination performance and GIS surveillance heads

Revision ID: 529565a4cb7d
Revises: vaccination_performance_complete, add_vaccination_kpi_tables
Create Date: 2026-08-12 01:12:04.720141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '529565a4cb7d'
down_revision = ('vaccination_performance_complete', 'add_vaccination_kpi_tables')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
