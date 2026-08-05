from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres123@localhost:5432/pvimp_db"
)

mappings = [

    ("ActionTypeTitle", "action_type"),
    ("ActionNo", "certificate_no"),
    ("ActionDate", "action_date"),

    ("تاریخ ثبت", "report_date"),
    ("کد واحد اپیدمیولوژیک", "unit_code"),
    ("نام واحد اپیدمیولوژیک", "unit_name"),
    ("نوع واحد اپیدمیولوژیک", "unit_type"),

    ("استان", "province"),
    ("شهرستان", "county"),

    ("ActionName", "action_name"),
    ("ReportDate", "report_date"),
    ("ReportInfo", "report_info"),

]


with engine.begin() as conn:

    for excel_column, database_column in mappings:

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
                14,
                :excel_column,
                :database_column
            )
            """),
            {
                "excel_column": excel_column,
                "database_column": database_column
            }
        )


print("template 14 mapping created")