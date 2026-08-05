from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres123@localhost:5432/pvimp_db"
)

with engine.begin() as conn:

    conn.execute(text("""
        UPDATE gis_import_templates
        SET is_active = false
        WHERE id IN (15,24,26,27);
    """))

print("Old duplicate templates disabled.")