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
WHERE template_id = 14;
""")

fields = [
    ("ActionTypeTitle", "action_type", 1),
    ("ActionNo", "certificate_no", 2),
    ("ActionDate", "action_date", 3),
    ("تاریخ ثبت", "report_date", 4),
    ("کد واحد اپیدمیولوژیک", "unit_code", 5),
    ("ActionName", "action_name", 6),
]

for excel_column, database_column, order_index in fields:
    cur.execute("""
    INSERT INTO gis_import_fields
    (
        template_id,
        excel_column,
        database_column,
        order_index
    )
    VALUES
    (14,%s,%s,%s)
    """,
    (
        excel_column,
        database_column,
        order_index
    ))

conn.commit()

cur.close()
conn.close()

print("template 14 mapping updated")
