import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="pvimp_db",
    user="postgres",
    password="postgres123"
)

cur = conn.cursor()

cur.execute("""
DELETE FROM gis_import_fields
WHERE template_id IN (28,29)
""")

conn.commit()

cur.close()
conn.close()

print("old mappings deleted")
