"""add veterinary unit relation to inspections

Revision ID: 86454b41da2f
Revises: cf81978b1623
"""

from alembic import op
import sqlalchemy as sa


revision = "86454b41da2f"
down_revision = "cf81978b1623"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column(
        "inspections",
        sa.Column(
            "veterinary_unit_id",
            sa.Integer(),
            nullable=True
        )
    )

    # اگر واحد دامپزشکی وجود ندارد یک رکورد پیش فرض بساز
    op.execute(
        """
        INSERT INTO veterinary_units (name, code, county_id, is_active)
        SELECT 'واحد پیش فرض', 'DEFAULT', id, true
        FROM county
        WHERE NOT EXISTS (
            SELECT 1 FROM veterinary_units
        )
        LIMIT 1;
        """
    )

    # مقداردهی رکوردهای قبلی
    op.execute(
        """
        UPDATE inspections
        SET veterinary_unit_id = (
            SELECT id
            FROM veterinary_units
            ORDER BY id
            LIMIT 1
        )
        WHERE veterinary_unit_id IS NULL;
        """
    )

    op.create_foreign_key(
        "fk_inspections_veterinary_unit",
        "inspections",
        "veterinary_units",
        ["veterinary_unit_id"],
        ["id"],
    )

    op.alter_column(
        "inspections",
        "veterinary_unit_id",
        nullable=False
    )


def downgrade() -> None:

    op.drop_constraint(
        "fk_inspections_veterinary_unit",
        "inspections",
        type_="foreignkey"
    )

    op.drop_column(
        "inspections",
        "veterinary_unit_id"
    )