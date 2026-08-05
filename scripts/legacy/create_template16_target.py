from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres123@localhost:5432/pvimp_db"
)

with engine.begin() as conn:

    conn.execute(
        text("""
        DELETE FROM gis_import_targets
        WHERE template_id = 16
        """)
    )

    conn.execute(
        text("""
        INSERT INTO gis_import_targets
        (
            template_id,
            model_name,
            table_name,
            description
        )
        VALUES
        (
            16,
            'GISParasiteControl',
            'gis_parasite_controls',
            'مبارزه با انگل ها'
        )
        """)
    )

print("template 16 target created")