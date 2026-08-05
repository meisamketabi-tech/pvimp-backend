from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres123@localhost:5432/pvimp_db"
)

with engine.connect() as conn:
    rows = conn.execute(
        text("""
            select column_name, data_type
            from information_schema.columns
            where table_name = 'gis_epidemiology_units'
            order by ordinal_position
        """)
    ).fetchall()

    for row in rows:
        print(row)