from alembic import op
import sqlalchemy as sa


revision = "c15c6f50840f"
down_revision = "53484d4e7583"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "gis_disease_occurrences",
        sa.Column("animal_count", sa.Integer(), nullable=True)
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("exposed_count", sa.Integer(), nullable=True)
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("infected_count", sa.Integer(), nullable=True)
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("dead_count", sa.Integer(), nullable=True)
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("slaughtered_count", sa.Integer(), nullable=True)
    )

    op.add_column(
        "gis_disease_occurrences",
        sa.Column("start_date", sa.Date(), nullable=True)
    )


def downgrade():
    op.drop_column("gis_disease_occurrences", "start_date")
    op.drop_column("gis_disease_occurrences", "slaughtered_count")
    op.drop_column("gis_disease_occurrences", "dead_count")
    op.drop_column("gis_disease_occurrences", "infected_count")
    op.drop_column("gis_disease_occurrences", "exposed_count")
    op.drop_column("gis_disease_occurrences", "animal_count")