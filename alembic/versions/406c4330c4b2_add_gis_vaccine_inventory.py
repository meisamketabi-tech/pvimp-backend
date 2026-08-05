"""add gis vaccine inventory

Revision ID: 406c4330c4b2
Revises: 0e9a1e1b1f49
Create Date: 2026-08-04 19:59:46.249755

"""

from alembic import op
import sqlalchemy as sa


revision = "406c4330c4b2"
down_revision = "0e9a1e1b1f49"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "gis_vaccine_inventories",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            "distribution_vaccine_center_vcode",
            sa.String(100),
            nullable=True
        ),

        sa.Column(
            "epidemiology_unit_id",
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            "province_name",
            sa.String(100)
        ),

        sa.Column(
            "county_name",
            sa.String(100)
        ),

        sa.Column(
            "epidemiology_unit_type",
            sa.String(100)
        ),

        sa.Column(
            "epidemiology_unit_code",
            sa.String(100)
        ),

        sa.Column(
            "epidemiology_unit_name",
            sa.String(255)
        ),


        sa.Column(
            "user_code",
            sa.String(100)
        ),

        sa.Column(
            "user_name",
            sa.String(255)
        ),


        sa.Column(
            "distribution_no",
            sa.String(100)
        ),

        sa.Column(
            "distribution_date",
            sa.Date()
        ),


        sa.Column(
            "vaccine_type",
            sa.String(100)
        ),

        sa.Column(
            "vaccine_brand",
            sa.String(255)
        ),

        sa.Column(
            "manufacturer",
            sa.String(255)
        ),

        sa.Column(
            "batch_number",
            sa.String(100)
        ),


        sa.Column(
            "vaccine_shape",
            sa.String(100)
        ),


        sa.Column(
            "package_count",
            sa.Integer()
        ),

        sa.Column(
            "dose_volume",
            sa.Float()
        ),


        sa.Column(
            "unit_name",
            sa.String(255)
        ),


        sa.Column(
            "registration_date",
            sa.Date()
        ),


        sa.Column(
            "production_import_date",
            sa.Date()
        ),

        sa.Column(
            "expiration_date",
            sa.Date()
        ),

        sa.ForeignKeyConstraint(
            ["epidemiology_unit_id"],
            ["gis_epidemiology_units.id"]
        ),
    )


    op.create_index(
        "ix_gis_vaccine_inventories_id",
        "gis_vaccine_inventories",
        ["id"],
        unique=False
    )


    op.create_index(
        "ix_gis_vaccine_inventories_distribution_vaccine_center_vcode",
        "gis_vaccine_inventories",
        ["distribution_vaccine_center_vcode"],
        unique=False
    )


    op.create_index(
        "ix_gis_vaccine_inventories_epidemiology_unit_id",
        "gis_vaccine_inventories",
        ["epidemiology_unit_id"],
        unique=False
    )



def downgrade() -> None:

    op.drop_index(
        "ix_gis_vaccine_inventories_epidemiology_unit_id",
        table_name="gis_vaccine_inventories"
    )

    op.drop_index(
        "ix_gis_vaccine_inventories_distribution_vaccine_center_vcode",
        table_name="gis_vaccine_inventories"
    )

    op.drop_index(
        "ix_gis_vaccine_inventories_id",
        table_name="gis_vaccine_inventories"
    )

    op.drop_table(
        "gis_vaccine_inventories"
    )