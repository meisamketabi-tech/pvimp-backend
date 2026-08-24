"""Materialize the expensive vaccination KPI classification view.

The source ``gis_vaccination_kpi`` view performs regex normalization and
multiple CASE/ILIKE classifications for every request. The materialized view
keeps the exact existing classification output but pays that cost only when
the source vaccination-performance data changes.
"""

from alembic import op


revision = "perf_vaccination_kpi_materialized"
down_revision = "vaccination_performance_complete"
branch_labels = None
depends_on = None


MV_NAME = "gis_vaccination_kpi_mv"


def upgrade() -> None:
    op.execute(
        f"""
        CREATE MATERIALIZED VIEW IF NOT EXISTS {MV_NAME} AS
        SELECT *
        FROM gis_vaccination_kpi
        WITH DATA
        """
    )

    # id is inherited from gis_vaccination_performances and is the stable
    # unique key needed for cheap freshness checks and future concurrent
    # refreshes.
    op.execute(
        f"""
        CREATE UNIQUE INDEX IF NOT EXISTS {MV_NAME}_id_uidx
        ON {MV_NAME} (id)
        """
    )

    op.execute(
        f"""
        CREATE INDEX IF NOT EXISTS {MV_NAME}_province_county_idx
        ON {MV_NAME} (province_code, county_code)
        """
    )

    op.execute(
        f"""
        CREATE INDEX IF NOT EXISTS {MV_NAME}_unit_vaccine_animal_idx
        ON {MV_NAME} (
            epidemiology_unit_code,
            vaccine_type,
            animal_group
        )
        """
    )

    op.execute(f"ANALYZE {MV_NAME}")


def downgrade() -> None:
    op.execute(f"DROP MATERIALIZED VIEW IF EXISTS {MV_NAME}")
