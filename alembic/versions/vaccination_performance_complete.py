"""add missing vaccination performance columns"""

from alembic import op
import sqlalchemy as sa

revision = "vaccination_performance_complete"
down_revision = "9139e94cb178"
branch_labels = None
depends_on = None


def upgrade():

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("vaccination_no", sa.String(100)),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("vaccine_category", sa.String(100)),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("province_code", sa.String(20)),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("county_code", sa.String(20)),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("epidemiology_unit_name", sa.String(255)),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("epidemiology_unit_code", sa.String(100)),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("epidemiology_unit_type", sa.String(100)),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("vaccination_center_name", sa.String(255)),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("vaccination_center_code", sa.String(100)),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("animal_count", sa.Integer()),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("dose_per_vial", sa.Float()),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("package_count", sa.Integer()),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("rappel_vaccination", sa.String(100)),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("operation_type", sa.String(100)),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("shock_after_injection", sa.Boolean()),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("shock_count", sa.Integer()),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("death_count", sa.Integer()),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("abortion", sa.Boolean()),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("abortion_count", sa.Integer()),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("hypersensitivity", sa.Boolean()),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("hypersensitivity_count", sa.Integer()),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("local_complication", sa.Boolean()),
    )

    op.add_column(
        "gis_vaccination_performances",
        sa.Column("local_complication_count", sa.Integer()),
    )


def downgrade():

    cols = [
        "local_complication_count",
        "local_complication",
        "hypersensitivity_count",
        "hypersensitivity",
        "abortion_count",
        "abortion",
        "death_count",
        "shock_count",
        "shock_after_injection",
        "operation_type",
        "rappel_vaccination",
        "package_count",
        "dose_per_vial",
        "animal_count",
        "vaccination_center_code",
        "vaccination_center_name",
        "epidemiology_unit_type",
        "epidemiology_unit_code",
        "epidemiology_unit_name",
        "county_code",
        "province_code",
        "vaccination_no",
        "vaccine_category",
    ]

    for c in cols:
        op.drop_column("gis_vaccination_performances", c)
