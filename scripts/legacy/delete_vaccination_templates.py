from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql://postgres:postgres123@localhost:5432/pvimp_db"
)

with engine.begin() as db:
    db.execute(
        text(
            """
            DELETE FROM gis_import_templates
