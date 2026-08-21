from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres123@localhost:5432/pvimp_db"
)


mapping = [

    ("SprayingVCode", "spraying_code"),

    ("استان", "province"),

    ("شهرستان", "county"),

    ("نام واحد اپیدمیولوژیک", "unit_name"),

    ("کد واحد اپیدمیولوژیک", "unit_code"),

    ("نوع واحد اپیدمیولوژیک", "unit_type"),

    ("تاریخ سمپاشی", "control_date"),

    ("نوع طرح", "plan_type"),

    ("نوع عمیات سمپاشی", "operation_type"),

    ("نوع سم", "pesticide"),

    ("مساحت سمپاشی شده", "sprayed_area"),

    ("تعداد دام سمپاشی شده", "sprayed_animals"),

    ("نوع دام", "animal_type"),

    ("کد استان", "province_code"),

    ("کد شهرستان", "county_code"),

    ("تعداد دام موجود", "total_animals"),

]


with engine.begin() as conn:

    conn.execute(
        text("""
        DELETE FROM gis_import_fields
        WHERE template_id=16
        """)
    )


    for excel_column, database_column in mapping:

        conn.execute(
            text("""
            INSERT INTO gis_import_fields
            (
                template_id,
                excel_column,
                database_column
            )
            VALUES
            (
                16,
                :excel_column,
                :database_column
            )
            """),
            {
                "excel_column": excel_column,
                "database_column": database_column
            }
        )


print("template 16 full 16-column mapping created")