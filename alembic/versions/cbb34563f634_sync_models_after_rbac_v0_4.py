"""sync models after rbac v0_4

Revision ID: cbb34563f634
Revises: d969e0c96a89
Create Date: 2026-07-17 11:03:54.070454
"""

from alembic import op
import sqlalchemy as sa


revision = "cbb34563f634"
down_revision = "d969e0c96a89"
branch_labels = None
depends_on = None


def upgrade() -> None:

    # province
    op.alter_column(
        "province",
        "name",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=100),
        existing_nullable=False,
    )

    op.alter_column(
        "province",
        "code",
        existing_type=sa.VARCHAR(length=50),
        type_=sa.String(length=10),
        existing_nullable=False,
    )

    op.drop_index(
        "ix_province_code",
        table_name="province"
    )

    op.drop_index(
        "ix_province_name",
        table_name="province"
    )

    op.create_unique_constraint(
        "uq_province_code",
        "province",
        ["code"]
    )


    # county
    op.alter_column(
        "county",
        "name",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=100),
        existing_nullable=False,
    )

    op.alter_column(
        "county",
        "code",
        existing_type=sa.VARCHAR(length=50),
        type_=sa.String(length=10),
        existing_nullable=False,
    )

    op.drop_index(
        "ix_county_code",
        table_name="county"
    )

    op.drop_index(
        "ix_county_name",
        table_name="county"
    )

    op.create_unique_constraint(
        "uq_county_code",
        "county",
        ["code"]
    )

    op.drop_constraint(
        "county_province_id_fkey",
        "county",
        type_="foreignkey"
    )

    op.create_foreign_key(
        "fk_county_province",
        "county",
        "province",
        ["province_id"],
        ["id"],
        ondelete="RESTRICT"
    )


    # user_account

    op.alter_column(
        "user_account",
        "username",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=50),
        existing_nullable=False,
    )


    op.alter_column(
        "user_account",
        "full_name",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=255),
        nullable=True,
    )


    op.alter_column(
        "user_account",
        "email",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=255),
        existing_nullable=True,
    )


    op.alter_column(
        "user_account",
        "mobile",
        existing_type=sa.VARCHAR(length=50),
        type_=sa.String(length=20),
        existing_nullable=True,
    )


    op.drop_index(
        "ix_user_account_is_active",
        table_name="user_account"
    )



def downgrade() -> None:

    op.create_index(
        "ix_user_account_is_active",
        "user_account",
        ["is_active"],
        unique=False
    )


    op.alter_column(
        "user_account",
        "mobile",
        existing_type=sa.String(length=20),
        type_=sa.VARCHAR(length=50),
        existing_nullable=True,
    )

    op.alter_column(
        "user_account",
        "email",
        existing_type=sa.String(length=255),
        type_=sa.VARCHAR(length=200),
        existing_nullable=True,
    )

    op.alter_column(
        "user_account",
        "full_name",
        existing_type=sa.String(length=255),
        type_=sa.VARCHAR(length=200),
        nullable=False,
    )

    op.alter_column(
        "user_account",
        "username",
        existing_type=sa.String(length=50),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )


    op.drop_constraint(
        "uq_province_code",
        "province",
        type_="unique"
    )

    op.create_index(
        "ix_province_code",
        "province",
        ["code"],
        unique=True
    )

    op.create_index(
        "ix_province_name",
        "province",
        ["name"],
        unique=False
    )


    op.drop_constraint(
        "uq_county_code",
        "county",
        type_="unique"
    )

    op.drop_constraint(
        "fk_county_province",
        "county",
        type_="foreignkey"
    )

    op.create_foreign_key(
        "county_province_id_fkey",
        "county",
        "province",
        ["province_id"],
        ["id"],
        ondelete="RESTRICT"
    )

    op.create_index(
        "ix_county_code",
        "county",
        ["code"],
        unique=True
    )

    op.create_index(
        "ix_county_name",
        "county",
        ["name"],
        unique=False
    )


    op.alter_column(
        "county",
        "code",
        existing_type=sa.String(length=10),
        type_=sa.VARCHAR(length=50),
        existing_nullable=False,
    )

    op.alter_column(
        "county",
        "name",
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(length=200),
        existing_nullable=False,
    )