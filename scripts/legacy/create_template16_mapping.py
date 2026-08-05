from sqlalchemy import create_engine, text


engine = create_engine(
    "postgresql+psycopg2://postgres:postgres123@localhost:5432/pvimp_db"
)


mapping = [

    ("SprayingVCode", "spraying_v_code"),

    ("استان", "province"),

    ("شهرستان", "county"),

    ("نام واحد اپیدمیولوژیک", "unit_name"),

    ("کد واحد اپیدمیولوژیک", "unit_code"),

    ("نوع واحد اپیدمیولوژیک", "unit_type"),

    ("تاریخ سمپاشی", "spraying_date"),

    ("نوع طرح", "plan_type"),

    ("نوع عمیات سمپاشی", "operation_type"),

    ("نوع سم", "pesticide_type"),

    ("مساحت سمپاشی شده", "sprayed_area"),

    ("تعداد دام سمپاشی شده", "sprayed_animal_count"),

    ("نوع دام", "animal_type"),

    ("کد استان", "province_code"),

    ("کد شهرستان", "county_code"),

    ("تعداد دام موجود", "existing_animal_count"),

]


with engine.begin() as conn:

    conn.execute(
        text("""
        DELETE FROM gis_import_fields
        WHERE template_id = 16
        """)
    )


    for index, (excel_column, database_column) in enumerate(mapping, start=1):

        conn.execute(
            text("""
            INSERT INTO gis_import_fields
            (
                template_id,
                excel_column,
                database_column,
                order_index
            )
            VALUES
            (
                16,
                :excel_column,
                :database_column,
                :order_index
            )
            """),
            {
                "excel_column": excel_column,
                "database_column": database_column,
                "order_index": index
            }
        )


print("template 16 mapping created")