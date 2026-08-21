from app.db.session import SessionLocal
from sqlalchemy import text


db = SessionLocal()


template_id = 23


fields = [
    ("نام واحد اپیدمیولوژیک", "name", "string"),
    ("کد واحد اپیدمیولوژیک", "unit_code", "string"),
    ("کد واحد قدیم", "old_unit_code", "string"),
    ("نوع واحد اپیدمیولوژیک", "unit_type", "string"),
    ("استان", "province", "string"),
    ("شهرستان", "county", "string"),
    ("X", "x", "float"),
    ("Y", "y", "float"),
    ("نام کاربر", "user_name", "string"),
    ("کد کاربر", "user_code", "string"),
    ("تعداد گوسفند", "sheep_count", "integer"),
    ("تعداد گاو", "cattle_count", "integer"),
    ("تعداد بز", "goat_count", "integer"),
    ("کد واحد پدر", "parent_unit_code", "string"),
    ("تاریخ ثبت", "register_date", "string"),
    ("وضعیت فعال بودن واحد", "is_active", "boolean"),
    ("تعداد اسب", "horse_count", "integer"),
    ("تعداد سگ", "dog_count", "integer"),
    ("تعداد شتر", "camel_count", "integer"),
    ("تعداد گاومیش", "buffalo_count", "integer"),
    ("کد پستی", "postal_code", "string"),
    ("شماره پروانه بهداشتی", "health_license_no", "string"),
    ("تاریخ پروانه بهداشتی", "health_license_date", "string"),
    ("شماره پروانه بهره برداری", "operation_license_no", "string"),
    ("تاریخ پروانه بهره برداری", "operation_license_date", "string"),
    ("آدرس", "address", "string"),
    ("کد پنجره", "window_code", "string"),
    ("نوع پروانه بهره برداری", "license_type", "string"),
    ("HasSubUnit", "has_sub_unit", "boolean"),
]


# حذف Mapping قبلی
db.execute(
    text("""
        DELETE FROM gis_import_fields
        WHERE template_id = :template_id
    """),
    {
        "template_id": template_id
    }
)


# حذف Targetهای قبلی
db.execute(
    text("""
        DELETE FROM gis_import_targets
        WHERE template_id = :template_id
    """),
    {
        "template_id": template_id
    }
)


# ایجاد Target صحیح
db.execute(
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
            :template_id,
            :model_name,
            :table_name,
            :description
        )
    """),
    {
        "template_id": template_id,
        "model_name": "GISEpidemiologyUnit",
        "table_name": "gis_epidemiology_units",
        "description": "اپیدمیولوژیک دام",
    }
)


# ایجاد Field Mappingها
for index, (excel_column, database_column, data_type) in enumerate(fields):

    db.execute(
        text("""
            INSERT INTO gis_import_fields
            (
                template_id,
                excel_column,
                database_column,
                data_type,
                is_required,
                order_index
            )
            VALUES
            (
                :template_id,
                :excel_column,
                :database_column,
                :data_type,
                false,
                :order_index
            )
        """),
        {
            "template_id": template_id,
            "excel_column": excel_column,
            "database_column": database_column,
            "data_type": data_type,
            "order_index": index,
        }
    )


db.commit()


print("TEMPLATE 23 FIXED")
print("TARGETS: 1")
print(f"FIELDS: {len(fields)}")


db.close()