import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="pvimp_db",
    user="postgres",
    password="postgres123"
)

cur = conn.cursor()

cur.execute("""
INSERT INTO gis_import_targets
(
    template_id,
    model_name,
    table_name,
    description
)
VALUES
(
    14,
    'GIS Disease Action History',
    'gis_dam_operation_history',
    'سابقه عملیات در واحد دامی'
)
ON CONFLICT DO NOTHING;
""")

conn.commit()

cur.close()
conn.close()

print("template14 target created")
