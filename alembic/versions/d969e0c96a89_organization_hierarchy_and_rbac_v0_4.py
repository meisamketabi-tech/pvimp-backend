"""organization hierarchy and RBAC v0.4

Revision ID: d969e0c96a89
Revises: c362d30c9cb4
Create Date: 2026-07-17 10:46:18.455465

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d969e0c96a89"
down_revision = "c362d30c9cb4"
branch_labels = None
depends_on = None


def upgrade() -> None:

    # ==========================
    # New RBAC
    # ==========================

    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_roles_id",
        "roles",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_roles_name",
        "roles",
        ["name"],
        unique=True,
    )


    # ==========================
    # Organization hierarchy
    # ==========================

    op.create_table(
        "organization_units",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "name",
            sa.String(length=150),
            nullable=False,
        ),

        sa.Column(
            "code",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "unit_type",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "parent_id",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "province_id",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "county_id",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["organization_units.id"],
        ),

        sa.ForeignKeyConstraint(
            ["province_id"],
            ["province.id"],
        ),

        sa.ForeignKeyConstraint(
            ["county_id"],
            ["county.id"],
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),
    )


    op.create_index(
        "ix_organization_units_id",
        "organization_units",
        ["id"],
        unique=False,
    )


    op.create_index(
        "ix_organization_units_code",
        "organization_units",
        ["code"],
        unique=True,
    )


    # ==========================
    # User assignments
    # ==========================

    op.create_table(
        "user_assignments",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "organization_unit_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "role_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "start_date",
            sa.Date(),
            nullable=True,
        ),

        sa.Column(
            "end_date",
            sa.Date(),
            nullable=True,
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user_account.id"],
        ),

        sa.ForeignKeyConstraint(
            ["organization_unit_id"],
            ["organization_units.id"],
        ),

        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),
    )


    op.create_index(
        "ix_user_assignments_id",
        "user_assignments",
        ["id"],
        unique=False,
    )


    # ==========================
    # Remove old user relation
    # ==========================

    op.drop_constraint(
        "user_account_default_veterinary_unit_id_fkey",
        "user_account",
        type_="foreignkey",
    )

    op.drop_column(
        "user_account",
        "default_veterinary_unit_id",
    )


    # ==========================
    # Remove old user_role first
    # ==========================

    op.drop_constraint(
        "user_role_veterinary_unit_id_fkey",
        "user_role",
        type_="foreignkey",
    )


    op.drop_index(
        "ix_user_role_id",
        table_name="user_role",
    )


    op.drop_table(
        "user_role",
    )


    # ==========================
    # Remove old veterinary_unit
    # ==========================

    op.drop_index(
        "ix_veterinary_unit_code",
        table_name="veterinary_unit",
    )

    op.drop_index(
        "ix_veterinary_unit_id",
        table_name="veterinary_unit",
    )

    op.drop_index(
        "ix_veterinary_unit_name",
        table_name="veterinary_unit",
    )

    op.drop_index(
        "ix_veterinary_unit_unit_type",
        table_name="veterinary_unit",
    )


    op.drop_table(
        "veterinary_unit",
    )


    # ==========================
    # Remove old role
    # ==========================

    op.drop_index(
        "ix_role_id",
        table_name="role",
    )

    op.drop_index(
        "ix_role_name",
        table_name="role",
    )


    op.drop_table(
        "role",
    )



def downgrade() -> None:

    raise NotImplementedError(
        "Downgrade is not implemented for v0.4"
    )