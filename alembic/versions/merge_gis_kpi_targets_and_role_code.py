"""merge gis kpi targets and role code heads

Revision ID: merge_gis_kpi_targets_and_role_code
Revises: ad5e1a4c8998, add_gis_kpi_targets
Create Date: 2026-08-15

This migration only merges two existing Alembic branches:

    529565a4cb7d
       ├── ad5e1a4c8998
       └── add_gis_kpi_targets

No database objects are created or modified here.
"""

revision = "merge_gis_kpi_targets_and_role_code"

down_revision = (
    "ad5e1a4c8998",
    "add_gis_kpi_targets",
)

branch_labels = None

depends_on = None


def upgrade():
    pass


def downgrade():
    pass