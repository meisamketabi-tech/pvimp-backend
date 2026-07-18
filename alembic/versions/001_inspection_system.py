"""create inspection system tables

Revision ID: 001_inspection_system
Revises: e82a89808316
Create Date: 2026-07-17
"""

from alembic import op
import sqlalchemy as sa


revision = "001_inspection_system"
down_revision = "e82a89808316"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "inspection_types",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(100), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False
        ),
    )


    op.create_table(
        "checklists",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "inspection_type_id",
            sa.Integer(),
            sa.ForeignKey("inspection_types.id"),
            nullable=False
        ),
        sa.Column(
            "title",
            sa.String(200),
            nullable=False
        ),
        sa.Column("description", sa.Text()),
        sa.Column("is_active", sa.Boolean()),
    )


    op.create_table(
        "checklist_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "checklist_id",
            sa.Integer(),
            sa.ForeignKey("checklists.id"),
            nullable=False
        ),
        sa.Column(
            "title",
            sa.String(300),
            nullable=False
        ),
        sa.Column("description", sa.Text()),
        sa.Column("weight", sa.Integer()),
        sa.Column("is_required", sa.Boolean()),
    )


    op.create_table(
        "inspections",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "inspection_number",
            sa.String(50),
            unique=True,
            nullable=False
        ),
        sa.Column(
            "inspection_type_id",
            sa.Integer(),
            sa.ForeignKey("inspection_types.id"),
            nullable=False
        ),
        sa.Column(
            "organization_unit_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "inspector_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "inspection_date",
            sa.DateTime(),
            nullable=False
        ),
        sa.Column(
            "status",
            sa.String(50),
            nullable=False
        ),
        sa.Column(
            "result",
            sa.String(50),
            nullable=False
        ),
        sa.Column("notes", sa.Text()),
        sa.Column(
            "created_at",
            sa.DateTime()
        ),
        sa.Column(
            "updated_at",
            sa.DateTime()
        ),
    )


    op.create_table(
        "inspection_item_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "inspection_id",
            sa.Integer(),
            sa.ForeignKey("inspections.id"),
            nullable=False
        ),
        sa.Column(
            "checklist_item_id",
            sa.Integer(),
            sa.ForeignKey("checklist_items.id"),
            nullable=False
        ),
        sa.Column(
            "is_compliant",
            sa.Boolean(),
            nullable=False
        ),
        sa.Column(
            "score",
            sa.Integer()
        ),
        sa.Column(
            "inspector_note",
            sa.Text()
        ),
        sa.Column(
            "created_at",
            sa.DateTime()
        ),
    )


def downgrade():

    op.drop_table("inspection_item_results")
    op.drop_table("inspections")
    op.drop_table("checklist_items")
    op.drop_table("checklists")
    op.drop_table("inspection_types")