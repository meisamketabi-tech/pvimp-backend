from sqlalchemy import create_engine, text


engine = create_engine(
    "postgresql+psycopg2://postgres:postgres123@localhost:5432/pvimp_db"
)


mapping = [

    ("ActionTypeTitle", "action_type"),

    ("ActionNo", "certificate_no"),

    ("شماره گواهی", "certificate_no"),

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


    conn.execute(
        text("""
        DELETE FROM gis_import_fields
        WHERE template_id = 14
        """)
    )


    for index, item in enumerate(mapping, start=1):

        excel_column = item[0]

        database_column = item[1]


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
                14,
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


print("template 14 mapping recreated")