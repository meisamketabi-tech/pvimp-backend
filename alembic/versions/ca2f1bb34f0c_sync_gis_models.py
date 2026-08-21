"""sync gis models

Revision ID: ca2f1bb34f0c
Revises: 380cbdc3b50e
Create Date: 2026-08-03 09:56:30.728328

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "ca2f1bb34f0c"
down_revision = "380cbdc3b50e"
branch_labels = None
depends_on = None


def upgrade() -> None:

    # ============================================================
    # gis_counties
    # ============================================================

    op.alter_column(
        "gis_counties",
        "county_code",
        existing_type=sa.VARCHAR(length=10),
        type_=sa.String(length=20),
        existing_nullable=False,
        postgresql_using="county_code::varchar(20)",
    )

    op.alter_column(
        "gis_counties",
        "county_name",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=100),
        existing_nullable=False,
        postgresql_using="county_name::varchar(100)",
    )

    op.drop_index(
        op.f("ix_gis_counties_county_code"),
        table_name="gis_counties",
    )

    op.create_index(
        op.f("ix_gis_counties_county_code"),
        "gis_counties",
        ["county_code"],
        unique=True,
    )

    op.create_index(
        op.f("ix_gis_counties_county_name"),
        "gis_counties",
        ["county_name"],
        unique=False,
    )

    # ============================================================
    # gis_epidemiology_unit_types
    # ============================================================

    op.add_column(
        "gis_epidemiology_unit_types",
        sa.Column(
            "code",
            sa.String(length=50),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_epidemiology_unit_types",
        sa.Column(
            "description",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.alter_column(
        "gis_epidemiology_unit_types",
        "title",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=255),
        existing_nullable=False,
        postgresql_using="title::varchar(255)",
    )

    op.drop_constraint(
        op.f("gis_epidemiology_unit_types_title_key"),
        "gis_epidemiology_unit_types",
        type_="unique",
    )

    op.create_index(
        op.f("ix_gis_epidemiology_unit_types_code"),
        "gis_epidemiology_unit_types",
        ["code"],
        unique=True,
    )

    op.create_index(
        op.f("ix_gis_epidemiology_unit_types_title"),
        "gis_epidemiology_unit_types",
        ["title"],
        unique=True,
    )
    # ============================================================
    # gis_epidemiology_units
    # ============================================================

    epidemiology_unit_columns = [
        ("user_name", sa.String(length=100)),
        ("user_code", sa.String(length=50)),
        ("sheep_count", sa.Integer()),
        ("cattle_count", sa.Integer()),
        ("goat_count", sa.Integer()),
        ("horse_count", sa.Integer()),
        ("dog_count", sa.Integer()),
        ("camel_count", sa.Integer()),
        ("buffalo_count", sa.Integer()),
        ("sanitary_license_number", sa.String(length=100)),
        ("operation_license_number", sa.String(length=100)),
        ("has_sub_unit", sa.Boolean()),
    ]

    for column_name, column_type in epidemiology_unit_columns:
        op.add_column(
            "gis_epidemiology_units",
            sa.Column(
                column_name,
                column_type,
                nullable=True,
            ),
        )

    op.add_column(
        "gis_epidemiology_units",
        sa.Column(
            "sanitary_license_date",
            sa.Date(),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_epidemiology_units",
        sa.Column(
            "operation_license_date",
            sa.Date(),
            nullable=True,
        ),
    )

    op.alter_column(
        "gis_epidemiology_units",
        "window_code",
        existing_type=sa.VARCHAR(length=50),
        type_=sa.String(length=100),
        existing_nullable=True,
        postgresql_using="window_code::varchar(100)",
    )

    op.alter_column(
        "gis_epidemiology_units",
        "province_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )

    op.alter_column(
        "gis_epidemiology_units",
        "county_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )

    op.alter_column(
        "gis_epidemiology_units",
        "license_type",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=255),
        existing_nullable=True,
        postgresql_using="license_type::varchar(255)",
    )

    op.alter_column(
        "gis_epidemiology_units",
        "is_active",
        existing_type=sa.BOOLEAN(),
        nullable=True,
    )

    # حذف فیلدهای قدیمی مجوزها
    old_license_columns = [
        "business_license_no",
        "business_license_date",
        "license_date",
        "license_no",
    ]

    for column_name in old_license_columns:
        op.drop_column(
            "gis_epidemiology_units",
            column_name,
        )

        # ============================================================
    # gis_import_columns
    # ============================================================

    op.add_column(
        "gis_import_columns",
        sa.Column(
            "column_name",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_import_columns",
        sa.Column(
            "position",
            sa.Integer(),
            nullable=True,
        ),
    )

    # تبدیل boolean به integer در PostgreSQL
    op.execute("""
        ALTER TABLE gis_import_columns
        ALTER COLUMN is_required TYPE INTEGER
        USING (
            CASE
                WHEN is_required = TRUE THEN 1
                WHEN is_required = FALSE THEN 0
                ELSE NULL
            END
        )
        """)

    op.create_index(
        op.f("ix_gis_import_columns_template_id"),
        "gis_import_columns",
        ["template_id"],
        unique=False,
    )

    op.drop_column(
        "gis_import_columns",
        "excel_column",
    )

    op.drop_column(
        "gis_import_columns",
        "database_column",
    )

    op.drop_column(
        "gis_import_columns",
        "is_unique",
    )

    # ============================================================
    # gis_import_duplicate
    # ============================================================

    op.add_column(
        "gis_import_duplicate",
        sa.Column(
            "job_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_import_duplicate",
        sa.Column(
            "row_number",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_import_duplicate",
        sa.Column(
            "duplicate_key",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_import_duplicate",
        sa.Column(
            "existing_data",
            sa.JSON(),
            nullable=True,
        ),
    )

    op.create_index(
        op.f("ix_gis_import_duplicate_job_id"),
        "gis_import_duplicate",
        ["job_id"],
        unique=False,
    )

    op.drop_constraint(
        op.f("gis_import_duplicate_template_id_fkey"),
        "gis_import_duplicate",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "fk_gis_import_duplicate_job",
        "gis_import_duplicate",
        "gis_import_jobs",
        ["job_id"],
        ["id"],
    )

    for column_name in [
        "strategy",
        "field_name",
        "template_id",
        "enabled",
    ]:
        op.drop_column(
            "gis_import_duplicate",
            column_name,
        )

    # ============================================================
    # gis_import_errors
    # ============================================================

    op.add_column(
        "gis_import_errors",
        sa.Column(
            "job_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_import_errors",
        sa.Column(
            "row_number",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_import_errors",
        sa.Column(
            "field_name",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.alter_column(
        "gis_import_errors",
        "error_code",
        existing_type=sa.VARCHAR(length=50),
        type_=sa.String(length=100),
        existing_nullable=True,
        postgresql_using="error_code::varchar(100)",
    )

    op.alter_column(
        "gis_import_errors",
        "error_message",
        existing_type=sa.TEXT(),
        type_=sa.String(length=500),
        existing_nullable=True,
        postgresql_using="error_message::varchar(500)",
    )

    op.create_index(
        op.f("ix_gis_import_errors_job_id"),
        "gis_import_errors",
        ["job_id"],
        unique=False,
    )

    op.drop_constraint(
        op.f("gis_import_errors_row_id_fkey"),
        "gis_import_errors",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "fk_gis_import_errors_job",
        "gis_import_errors",
        "gis_import_jobs",
        ["job_id"],
        ["id"],
    )

    op.drop_column(
        "gis_import_errors",
        "column_name",
    )

    op.drop_column(
        "gis_import_errors",
        "row_id",
    )

    # ============================================================
    # gis_import_files
    # ============================================================

    file_columns = [
        (
            "file_name",
            sa.String(length=255),
        ),
        (
            "file_path",
            sa.String(length=500),
        ),
        (
            "file_type",
            sa.String(length=50),
        ),
        (
            "uploaded_by",
            sa.String(length=100),
        ),
    ]

    for column_name, column_type in file_columns:
        op.add_column(
            "gis_import_files",
            sa.Column(
                column_name,
                column_type,
                nullable=True,
            ),
        )

    op.add_column(
        "gis_import_files",
        sa.Column(
            "uploaded_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )

    op.create_index(
        op.f("ix_gis_import_files_job_id"),
        "gis_import_files",
        ["job_id"],
        unique=False,
    )

    for column_name in [
        "original_name",
        "stored_name",
        "sheet_name",
        "file_extension",
    ]:
        op.drop_column(
            "gis_import_files",
            column_name,
        )

    # ============================================================
    # gis_import_history
    # ============================================================

    history_columns = [
        (
            "action",
            sa.String(length=100),
        ),
        (
            "username",
            sa.String(length=100),
        ),
    ]

    for column_name, column_type in history_columns:
        op.add_column(
            "gis_import_history",
            sa.Column(
                column_name,
                column_type,
                nullable=True,
            ),
        )

    op.add_column(
        "gis_import_history",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )

    op.create_index(
        op.f("ix_gis_import_history_job_id"),
        "gis_import_history",
        ["job_id"],
        unique=False,
    )

    op.drop_column(
        "gis_import_history",
        "executed_at",
    )

    # ============================================================
    # gis_import_jobs
    # ============================================================

    job_columns = [
        (
            "template_id",
            sa.Integer(),
        ),
        (
            "session_id",
            sa.Integer(),
        ),
        (
            "job_code",
            sa.String(length=100),
        ),
        (
            "processed_rows",
            sa.Integer(),
        ),
        (
            "is_completed",
            sa.Boolean(),
        ),
        (
            "started_at",
            sa.DateTime(),
        ),
    ]

    for column_name, column_type in job_columns:
        op.add_column(
            "gis_import_jobs",
            sa.Column(
                column_name,
                column_type,
                nullable=True,
            ),
        )

    op.alter_column(
        "gis_import_jobs",
        "status",
        existing_type=sa.VARCHAR(length=30),
        type_=sa.String(length=50),
        existing_nullable=True,
        postgresql_using="status::varchar(50)",
    )

    op.create_index(
        op.f("ix_gis_import_jobs_job_code"),
        "gis_import_jobs",
        ["job_code"],
        unique=True,
    )

    op.create_index(
        op.f("ix_gis_import_jobs_session_id"),
        "gis_import_jobs",
        ["session_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_gis_import_jobs_template_id"),
        "gis_import_jobs",
        ["template_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_gis_import_jobs_template",
        "gis_import_jobs",
        "gis_import_templates",
        ["template_id"],
        ["id"],
    )

    op.create_foreign_key(
        "fk_gis_import_jobs_session",
        "gis_import_jobs",
        "gis_import_sessions",
        ["session_id"],
        ["id"],
    )

    for column_name in [
        "import_type",
        "title",
        "created_by",
    ]:
        op.drop_column(
            "gis_import_jobs",
            column_name,
        )

    # ============================================================
    # gis_import_logs
    # ============================================================

    op.alter_column(
        "gis_import_logs",
        "level",
        existing_type=sa.VARCHAR(length=20),
        type_=sa.String(length=30),
        existing_nullable=True,
        postgresql_using="level::varchar(30)",
    )

    op.alter_column(
        "gis_import_logs",
        "message",
        existing_type=sa.TEXT(),
        type_=sa.String(length=500),
        existing_nullable=True,
        postgresql_using="message::varchar(500)",
    )

    op.create_index(
        op.f("ix_gis_import_logs_job_id"),
        "gis_import_logs",
        ["job_id"],
        unique=False,
    )

    # ============================================================
    # gis_import_mapping
    # ============================================================

    op.add_column(
        "gis_import_mapping",
        sa.Column(
            "excel_column",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_import_mapping",
        sa.Column(
            "database_field",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.alter_column(
        "gis_import_mapping",
        "transform_rule",
        existing_type=sa.VARCHAR(length=255),
        type_=sa.String(length=500),
        existing_nullable=True,
        postgresql_using="transform_rule::varchar(500)",
    )

    op.create_index(
        op.f("ix_gis_import_mapping_template_id"),
        "gis_import_mapping",
        ["template_id"],
        unique=False,
    )

    op.drop_column(
        "gis_import_mapping",
        "destination_field",
    )

    op.drop_column(
        "gis_import_mapping",
        "source_field",
    )

    # ============================================================
    # gis_import_preview
    # ============================================================

    op.alter_column(
        "gis_import_preview",
        "row_number",
        existing_type=sa.INTEGER(),
        nullable=False,
    )

    op.alter_column(
        "gis_import_preview",
        "preview_data",
        existing_type=postgresql.JSON(astext_type=sa.Text()),
        nullable=False,
    )

    op.create_index(
        op.f("ix_gis_import_preview_job_id"),
        "gis_import_preview",
        ["job_id"],
        unique=False,
    )

    # ============================================================
    # gis_import_queue
    # ============================================================

    op.alter_column(
        "gis_import_queue",
        "status",
        existing_type=sa.VARCHAR(length=30),
        type_=sa.String(length=50),
        existing_nullable=True,
        postgresql_using="status::varchar(50)",
    )

    # ============================================================
    # gis_import_rows
    # ============================================================

    op.add_column(
        "gis_import_rows",
        sa.Column(
            "raw_data",
            sa.JSON(),
            nullable=True,
        ),
    )

    op.create_index(
        op.f("ix_gis_import_rows_job_id"),
        "gis_import_rows",
        ["job_id"],
        unique=False,
    )

    op.drop_column(
        "gis_import_rows",
        "message",
    )

    op.drop_column(
        "gis_import_rows",
        "data",
    )

    # ============================================================
    # gis_import_schedules
    # ============================================================

    op.add_column(
        "gis_import_schedules",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_import_schedules",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )

    op.alter_column(
        "gis_import_schedules",
        "template_code",
        existing_type=sa.VARCHAR(length=100),
        nullable=False,
    )

    # ============================================================
    # gis_import_settings
    # ============================================================

    op.add_column(
        "gis_import_settings",
        sa.Column(
            "key",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_import_settings",
        sa.Column(
            "value",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.drop_constraint(
        op.f("gis_import_settings_setting_key_key"),
        "gis_import_settings",
        type_="unique",
    )

    op.create_index(
        op.f("ix_gis_import_settings_key"),
        "gis_import_settings",
        ["key"],
        unique=True,
    )

    op.drop_column(
        "gis_import_settings",
        "setting_value",
    )

    op.drop_column(
        "gis_import_settings",
        "setting_key",
    )

    # ============================================================
    # gis_import_statistics
    # ============================================================

    op.create_index(
        op.f("ix_gis_import_statistics_job_id"),
        "gis_import_statistics",
        ["job_id"],
        unique=False,
    )

    # ============================================================
    # gis_import_templates
    # ============================================================

    op.add_column(
        "gis_import_templates",
        sa.Column(
            "entity_name",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_import_templates",
        sa.Column(
            "version",
            sa.String(length=50),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_import_templates",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_import_templates",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )

    op.alter_column(
        "gis_import_templates",
        "description",
        existing_type=sa.TEXT(),
        type_=sa.String(length=500),
        existing_nullable=True,
        postgresql_using="description::varchar(500)",
    )

    op.alter_column(
        "gis_import_templates",
        "is_active",
        existing_type=sa.BOOLEAN(),
        nullable=True,
    )

    op.drop_column(
        "gis_import_templates",
        "worksheet_name",
    )

    op.drop_column(
        "gis_import_templates",
        "target_table",
    )

    op.drop_column(
        "gis_import_templates",
        "start_row",
    )

    # ============================================================
    # gis_import_validation
    # ============================================================

    op.add_column(
        "gis_import_validation",
        sa.Column(
            "job_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_import_validation",
        sa.Column(
            "row_number",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_import_validation",
        sa.Column(
            "message",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.add_column(
        "gis_import_validation",
        sa.Column(
            "status",
            sa.String(length=30),
            nullable=True,
        ),
    )

    op.create_index(
        op.f("ix_gis_import_validation_job_id"),
        "gis_import_validation",
        ["job_id"],
        unique=False,
    )

    op.drop_constraint(
        op.f("gis_import_validation_template_id_fkey"),
        "gis_import_validation",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "fk_gis_import_validation_job",
        "gis_import_validation",
        "gis_import_jobs",
        ["job_id"],
        ["id"],
    )

    op.drop_column(
        "gis_import_validation",
        "is_active",
    )

    op.drop_column(
        "gis_import_validation",
        "validation_value",
    )

    op.drop_column(
        "gis_import_validation",
        "template_id",
    )

    # ============================================================
    # gis_provinces
    # ============================================================

    op.alter_column(
        "gis_provinces",
        "province_code",
        existing_type=sa.VARCHAR(length=10),
        type_=sa.String(length=20),
        existing_nullable=False,
        postgresql_using="province_code::varchar(20)",
    )

    op.alter_column(
        "gis_provinces",
        "province_name",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=100),
        existing_nullable=False,
        postgresql_using="province_name::varchar(100)",
    )

    op.create_index(
        op.f("ix_gis_provinces_province_name"),
        "gis_provinces",
        ["province_name"],
        unique=False,
    )


def downgrade() -> None:
    """
    Downgrade intentionally kept minimal.
    Auto generated downgrade on large schema refactors
    is unsafe because data loss is unavoidable.
    """

    raise RuntimeError(
        "Downgrade disabled for this migration. "
        "Create a backup restore point before upgrading."
    )
