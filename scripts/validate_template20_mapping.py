from sqlalchemy import text
from app.db.session import SessionLocal

db = SessionLocal()

print("=" * 100)
print("TEMPLATE 20 / EXCEL -> DB MAPPING VALIDATION")
print("=" * 100)

rows = db.execute(text("""
    SELECT
        f.id,
        f.excel_column,
        f.database_column
    FROM gis_import_fields f
    WHERE f.template_id = 20
    ORDER BY f.id
""")).fetchall()

print(f"\nTOTAL MAPPINGS: {len(rows)}\n")

for r in rows:
    print(f"{r[0]} | EXCEL={r[1]} | DB={r[2]}")

expected = {
    "ObservationDetailVCode": "observation_detail_vcode",
    "کد واحد اپیدمیولوژیک": "epidemiological_unit_code",
    "نام واحد اپیدمیولوژیک": "epidemiological_unit_name",
    "نوع واحد اپیدمیولوژیک": "epidemiological_unit_type",
    "استان": "province",
    "شهرستان": "county",
    "نام بیماری": "disease_name",
    "نوع دام": "animal_type",
    "تاریخ شروع بیماری": "disease_start_date",
    "تعداد دام در معرض خطر": "at_risk_animals",
    "تعداد دام": "total_animals",
    "تعداد دام کشتار شده": "slaughtered_animals",
    "تعداد دام مبتلا": "affected_animals",
    "تعداد دام تلف شده": "dead_animals",
    "ReportDate": "report_date",
    "شماره گزارش بیماری": "disease_report_number",
    "تعداد کل دام": "total_population",
    "X": "x",
    "Y": "y",
    "ReportInfo": "report_info",
    "عنوان کاربر": "user_title",
    "کد کاربر": "user_code",
    "ExperterNames": "expert_names",
    "وضعیت": "status",
    "کد پنجره": "window_code",
    "نوع پروانه بهره برداری": "operation_license_type",
    "تاریخ ثبت": "register_date",
}

actual = {str(r[1]).strip(): str(r[2]).strip() for r in rows}

print("\n--- EXPECTED EXCEL -> DB ---")

errors = []

for excel_column, db_column in expected.items():

    if excel_column not in actual:
        errors.append(f"MISSING MAPPING | EXCEL={excel_column}")
        continue

    if actual[excel_column] != db_column:
        errors.append(
            f"WRONG MAPPING | EXCEL={excel_column} | "
            f"EXPECTED={db_column} | ACTUAL={actual[excel_column]}"
        )

    else:
        print(f"OK | EXCEL={excel_column} | DB={db_column}")

print("\n--- EXTRA MAPPINGS ---")

for excel_column, db_column in actual.items():

    if excel_column not in expected:
        errors.append(f"EXTRA MAPPING | EXCEL={excel_column} | DB={db_column}")
        print(f"EXTRA | EXCEL={excel_column} | DB={db_column}")

print("\n--- RESULT ---")

if len(rows) != 27:
    errors.append(f"EXPECTED 27 mappings but found {len(rows)}")

if errors:

    print("MAPPING VALIDATION FAILED")

    for error in errors:
        print("ERROR:", error)

    print("\nDO NOT IMPORT")

else:

    print("ALL 27 EXCEL DATA COLUMNS MATCH DATABASE COLUMNS")
    print("ردیف -> IGNORED")
    print("id -> DATABASE GENERATED")
    print("TEMPLATE 20 MAPPING VALIDATED")
    print("READY FOR IMPORT TEST")

print("=" * 100)

db.close()
