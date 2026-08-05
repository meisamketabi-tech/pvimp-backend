from sqlalchemy import text
from app.db.session import SessionLocal
from pathlib import Path
import pandas as pd
import math
import unicodedata
from datetime import date, datetime


print("=" * 100)
print("TEMPLATE 20 / FINAL EXCEL -> DATABASE VALUE VALIDATION")
print("=" * 100)


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(value):
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except Exception:
        pass

    value = str(value).strip()

    replacements = {
        "ي": "ی",
        "ى": "ی",
        "ك": "ک",
        "\u200b": "",
        "\u200c": "",
        "\u200d": "",
        "\u200e": "",
        "\u200f": "",
        "\ufeff": "",
        "\xa0": " ",
        "ـ": "",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    value = "".join(
        ch
        for ch in value
        if unicodedata.category(ch) not in ("Cc", "Cf")
    )

    value = " ".join(value.split()).strip()

    return value


def normalize_number(value):
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except Exception:
        pass

    try:
        number = float(value)

        if math.isnan(number):
            return None

        if number.is_integer():
            return int(number)

        return number

    except Exception:
        return normalize_text(value)


# ============================================================
# JALALI -> GREGORIAN
# ============================================================

def jalali_to_gregorian(jy, jm, jd):
    """
    Convert Jalali/Persian calendar date to Gregorian date.

    Supports Jalali years used by the Template 20 Excel file.
    """

    jy = int(jy)
    jm = int(jm)
    jd = int(jd)

    jy2 = jy - 979

    if jy2 < 0:
        raise ValueError(f"Invalid Jalali year: {jy}")

    days = (
        365 * jy2
        + (jy2 // 33) * 8
        + ((jy2 % 33) + 3) // 4
    )

    if jm <= 6:
        days += (jm - 1) * 31
    else:
        days += (jm - 1) * 30 + 6

    days += jd - 1

    days += 79

    gy = 1600 + 400 * (days // 146097)
    days %= 146097

    leap = True

    if days >= 36525:
        days -= 1

        gy += 100 * (days // 36524)
        days %= 36524

        if days >= 365:
            days += 1

        leap = False

    gy += 4 * (days // 1461)
    days %= 1461

    if days >= 366:
        leap = False
        days -= 1
        gy += days // 365
        days %= 365

    if leap:
        month_days = [
            31, 29, 31, 30, 31, 30,
            31, 31, 30, 31, 30, 31
        ]
    else:
        month_days = [
            31, 28, 31, 30, 31, 30,
            31, 31, 30, 31, 30, 31
        ]

    gm = 1

    while gm <= 12 and days >= month_days[gm - 1]:
        days -= month_days[gm - 1]
        gm += 1

    gd = days + 1

    return date(gy, gm, gd)


def normalize_date(value):
    """
    Normalize both Persian/Jalali and Gregorian dates
    to datetime.date.

    Examples:

        1405/04/28 -> 2026-07-19
        1405/02/29 -> 2026-05-19
        datetime.date(...) -> same date
    """

    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except Exception:
        pass

    # Already a Python date
    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    text_value = normalize_text(value)

    if not text_value:
        return None

    # Normalize separators
    text_value = (
        text_value
        .replace("-", "/")
        .replace(".", "/")
        .replace("\\", "/")
    )

    parts = text_value.split("/")

    if len(parts) == 3:
        try:
            y = int(parts[0])
            m = int(parts[1])
            d = int(parts[2])

            # Persian/Jalali year
            if 1200 <= y <= 1600:
                return jalali_to_gregorian(y, m, d)

            # Gregorian year
            if 1900 <= y <= 2200:
                return date(y, m, d)

        except Exception:
            pass

    # Try pandas datetime as final fallback
    try:
        parsed = pd.to_datetime(value, errors="coerce")

        if not pd.isna(parsed):
            return parsed.date()

    except Exception:
        pass

    return normalize_text(value)


def values_equal(excel_value, db_value, numeric=False, date_value=False):

    if date_value:
        return normalize_date(excel_value) == normalize_date(db_value)

    if numeric:
        return normalize_number(excel_value) == normalize_number(db_value)

    return normalize_text(excel_value) == normalize_text(db_value)


# ============================================================
# DATABASE
# ============================================================

db = SessionLocal()


# ============================================================
# REAL EXCEL
# ============================================================

excel_path = Path(r"D:\pvimp_backend\uploads\gis").glob("*.xlsx")

excel_files = list(excel_path)

if not excel_files:
    print("ERROR: No Excel file found.")
    db.close()
    raise SystemExit(1)

excel_file = max(
    excel_files,
    key=lambda p: p.stat().st_mtime
)

df = pd.read_excel(excel_file)


print("\nEXCEL FILE:")
print(excel_file)

print("\nEXCEL ROWS:", len(df))


# ============================================================
# VALIDATION COUNTERS
# ============================================================

value_errors = 0
missing_records = 0
duplicate_records = 0
duplicate_rows = 0


# ============================================================
# VALIDATE EACH EXCEL ROW
# ============================================================

for excel_row_number, (_, row) in enumerate(
    df.iterrows(),
    start=2
):

    # --------------------------------------------------------
    # Excel positional columns
    # --------------------------------------------------------

    obs = normalize_number(row.iloc[1])
    report = normalize_number(row.iloc[16])

    result = db.execute(
        text("""
            SELECT
                id,
                observation_detail_vcode,
                disease_report_number,
                epidemiological_unit_code,
                epidemiological_unit_name,
                epidemiological_unit_type,
                province,
                county,
                disease_name,
                animal_type,
                disease_start_date,
                at_risk_animals,
                total_animals,
                slaughtered_animals,
                affected_animals,
                dead_animals,
                report_date,
                total_population,
                x,
                y,
                report_info,
                user_title,
                user_code,
                expert_names,
                status,
                window_code,
                operation_license_type,
                register_date
            FROM gis_disease_outbreaks
            WHERE observation_detail_vcode = :obs
              AND disease_report_number = :report
            ORDER BY id
        """),
        {
            "obs": obs,
            "report": report,
        },
    ).fetchall()

    # --------------------------------------------------------
    # Missing record
    # --------------------------------------------------------

    if not result:

        print(
            f"MISSING | Excel Row={excel_row_number} | "
            f"OBS={obs} | REPORT={report}"
        )

        missing_records += 1
        continue

    # --------------------------------------------------------
    # Duplicate records
    # --------------------------------------------------------

    if len(result) > 1:

        duplicate_records += 1
        duplicate_rows += len(result)

        print(
            f"DUPLICATE | Excel Row={excel_row_number} | "
            f"OBS={obs} | REPORT={report} | "
            f"DB RECORDS={len(result)} | "
            f"IDS={[r[0] for r in result]}"
        )

    # --------------------------------------------------------
    # Compare against every duplicate record
    # --------------------------------------------------------

    row_has_error = False

    for db_row in result:

        checks = [
            (
                "observation_detail_vcode",
                obs,
                db_row[1],
                True,
                False,
            ),
            (
                "disease_report_number",
                report,
                db_row[2],
                True,
                False,
            ),
            (
                "epidemiological_unit_code",
                row.iloc[2],
                db_row[3],
                False,
                False,
            ),
            (
                "epidemiological_unit_name",
                row.iloc[3],
                db_row[4],
                False,
                False,
            ),
            (
                "epidemiological_unit_type",
                row.iloc[4],
                db_row[5],
                False,
                False,
            ),
            (
                "province",
                row.iloc[5],
                db_row[6],
                False,
                False,
            ),
            (
                "county",
                row.iloc[6],
                db_row[7],
                False,
                False,
            ),
            (
                "disease_name",
                row.iloc[7],
                db_row[8],
                False,
                False,
            ),
            (
                "animal_type",
                row.iloc[8],
                db_row[9],
                False,
                False,
            ),
            (
                "disease_start_date",
                row.iloc[9],
                db_row[10],
                False,
                True,
            ),
            (
                "at_risk_animals",
                row.iloc[10],
                db_row[11],
                True,
                False,
            ),
            (
                "total_animals",
                row.iloc[11],
                db_row[12],
                True,
                False,
            ),
            (
                "slaughtered_animals",
                row.iloc[12],
                db_row[13],
                True,
                False,
            ),
            (
                "affected_animals",
                row.iloc[13],
                db_row[14],
                True,
                False,
            ),
            (
                "dead_animals",
                row.iloc[14],
                db_row[15],
                True,
                False,
            ),
            (
                "report_date",
                row.iloc[15],
                db_row[16],
                False,
                True,
            ),
            (
                "total_population",
                row.iloc[17],
                db_row[17],
                True,
                False,
            ),
            (
                "x",
                row.iloc[18],
                db_row[18],
                True,
                False,
            ),
            (
                "y",
                row.iloc[19],
                db_row[19],
                True,
                False,
            ),
            (
                "report_info",
                row.iloc[20],
                db_row[20],
                False,
                False,
            ),
            (
                "user_title",
                row.iloc[21],
                db_row[21],
                False,
                False,
            ),
            (
                "user_code",
                row.iloc[22],
                db_row[22],
                True,
                False,
            ),
            (
                "expert_names",
                row.iloc[23],
                db_row[23],
                False,
                False,
            ),
            (
                "status",
                row.iloc[24],
                db_row[24],
                False,
                False,
            ),
            (
                "window_code",
                row.iloc[25],
                db_row[25],
                False,
                False,
            ),
            (
                "operation_license_type",
                row.iloc[26],
                db_row[26],
                False,
                False,
            ),
            (
                "register_date",
                row.iloc[27],
                db_row[27],
                False,
                True,
            ),
        ]

        row_errors = []

        for (
            field,
            excel_value,
            db_value,
            numeric,
            date_value,
        ) in checks:

            if not values_equal(
                excel_value,
                db_value,
                numeric=numeric,
                date_value=date_value,
            ):

                if date_value:
                    excel_display = normalize_date(excel_value)
                    db_display = normalize_date(db_value)
                else:
                    excel_display = excel_value
                    db_display = db_value

                row_errors.append(
                    f"{field}: "
                    f"EXCEL={excel_display!r} | "
                    f"DB={db_display!r}"
                )

        if row_errors:

            row_has_error = True

            print(
                f"MISMATCH | Excel Row={excel_row_number} | "
                f"OBS={obs} | REPORT={report} | "
                f"DB_ID={db_row[0]}"
            )

            for error in row_errors:
                print("   ", error)

    if row_has_error:

        value_errors += 1

    else:

        print(
            f"OK | Excel Row={excel_row_number} | "
            f"OBS={obs} | REPORT={report} | "
            f"DB_IDS={[r[0] for r in result]}"
        )


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 100)
print("TEMPLATE 20 / FINAL VALUE VALIDATION RESULT")
print("=" * 100)

print("EXCEL FILE:", excel_file)
print("TOTAL EXCEL ROWS:", len(df))
print("MISSING DATABASE RECORDS:", missing_records)
print("ROWS WITH VALUE ERRORS:", value_errors)
print("ROWS WITH DUPLICATE DB RECORDS:", duplicate_records)
print("TOTAL DUPLICATE DB ROWS ENCOUNTERED:", duplicate_rows)

print("\n--- RESULT ---")

if missing_records == 0 and value_errors == 0:

    print("ALL EXCEL VALUES MATCH DATABASE VALUES")

else:

    print("VALUE VALIDATION FAILED")


if duplicate_records == 0:

    print("NO DATABASE DUPLICATES")

else:

    print("DATABASE CONTAINS PRE-EXISTING DUPLICATE LOGICAL KEYS")


print("\nIMPORTANT:")
print("Unicode equivalents such as ي/ی and ك/ک are treated as equal.")
print("Excel NaN and database NULL are treated as equal.")
print("Persian/Jalali Excel dates are converted to Gregorian dates before comparison.")

print("=" * 100)

db.close()