print("=" * 80)
print("VACCINE DISPOSAL IMPORT MODULE LOADED")
print("=" * 80)

import traceback

import pandas as pd
from sqlalchemy.orm import Session

from app.db.models.gis_vaccine_disposal import GISVaccineDisposal
from app.db.models.gis_epidemiology_unit import GISEpidemiologyUnit

# ============================================================
# Helpers
# ============================================================


def clean_string(value):
    """
    تبدیل مقدار Excel به string تمیز.
    """

    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    value = str(value).strip()

    if value in ("", "'"):
        return None

    return value


def normalize_digits(value):
    """
    تبدیل ارقام فارسی و عربی به ارقام انگلیسی.
    """

    value = clean_string(value)

    if value is None:
        return None

    translation_table = str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
        "01234567890123456789",
    )

    return value.translate(translation_table)


def normalize_text(value):
    """
    Normalize متن فارسی.
    """

    value = normalize_digits(value)

    if value is None:
        return None

    value = value.replace("ي", "ی")
    value = value.replace("ى", "ی")
    value = value.replace("ك", "ک")
    value = value.replace("ۀ", "ه")

    invisible_chars = [
        "\u200c",
        "\u200d",
        "\u200e",
        "\u200f",
        "\ufeff",
    ]

    for char in invisible_chars:
        value = value.replace(char, "")

    value = " ".join(value.split())

    return value.strip()


def normalize_compare(value):
    """
    Normalize برای مقایسه.
    """

    value = normalize_text(value)

    if not value:
        return None

    value = value.replace(" ", "")
    value = value.replace("‌", "")

    return value


def clean_code(value):
    """
    تمیز کردن کدهای واحد و کدهای توزیع.

    مثال:
        19040070012      -> 19040070012
        "19040070012"    -> 19040070012
        19040070012.0    -> 19040070012
        " 19040070012 "  -> 19040070012
        "۱۹۰۴۰۰۷۰۰۱۲"    -> 19040070012
    """

    value = normalize_digits(value)

    if value is None:
        return None

    value = value.strip()

    # اگر Excel مقدار عددی را به صورت 12345.0 برگرداند
    if value.endswith(".0"):
        try:
            numeric_value = float(value)

            if numeric_value.is_integer():
                value = str(int(numeric_value))
        except (ValueError, TypeError):
            pass

    return value


def clean_int(value):
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None


def clean_float(value):
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def convert_date(value):
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    try:
        return pd.to_datetime(value).date()
    except (ValueError, TypeError):
        return None


def normalize_warning(value):
    """
    تبدیل warning به string امن برای Frontend.
    """

    if value is None:
        return ""

    if isinstance(value, str):
        return value

    if isinstance(value, dict):

        message = value.get("message")

        if message:
            return str(message)

        warning_type = value.get("type")
        row = value.get("row")

        if warning_type and row:
            return f"{warning_type} - ردیف {row}"

        if warning_type:
            return str(warning_type)

        return str(value)

    return str(value)


def normalize_warnings(value):
    """
    همیشه خروجی warnings را به list[str] تبدیل می‌کند.
    """

    if not value:
        return []

    if not isinstance(value, list):
        value = [value]

    normalized = []

    for item in value:
        normalized.append(normalize_warning(item))

    return normalized


# ============================================================
# Import
# ============================================================


def import_vaccine_disposal(
    db: Session,
    file_path: str,
):
    print("=" * 80)
    print("VACCINE DISPOSAL IMPORT")
    print(f"FILE: {file_path}")
    print("=" * 80)

    inserted = 0
    skipped = 0
    failed = 0

    warnings = []

    missing_units = []
    missing_unit_codes = set()

    # --------------------------------------------------------
    # Read Excel
    # --------------------------------------------------------

    try:

        df = pd.read_excel(file_path)

    except Exception as exc:

        traceback.print_exc()

        return {
            "inserted": 0,
            "skipped": 0,
            "failed": 1,
            "missing_units": [],
            "missing_epidemiology_units": [],
            "warnings": [
                "امکان خواندن فایل Excel " f"معدوم‌سازی واکسن وجود ندارد: {exc}"
            ],
        }

    print(f"ROWS: {len(df)}")

    # --------------------------------------------------------
    # Normalize Excel column names
    # --------------------------------------------------------

    df.columns = [str(column).strip() for column in df.columns]

    # --------------------------------------------------------
    # Required columns
    # --------------------------------------------------------

    required_columns = [
        "DistributionVaccineCenterVCode",
        "شماره توزیع",
        "تاریخ توزیع",
        "استان",
        "شهرستان",
        "کد واحد اپیدمیولوژیک",
        "نام واحد اپیدمیولوژیک",
        "نوع واحد اپیدمیولوژیک",
        "نوع توزیع",
        "DistributionStatusId",
        "استان واحد مقصد",
        "شهر واحد مقصد",
        "کد واحد مقصد",
        "نام واحد مقصد",
        "نوع واحد مقصد",
        "نوع واکسن",
        "نام تجاری واکسن",
        "کارخانه سازنده",
        "سری ساخت",
        "وضعیت",
        "شکل واکسن",
        "تعداد بسته",
        "حجم/ دز هر بسته",
        "واحد",
        "کد کاربر",
        "نام کاربر",
        "تاریخ ثبت",
    ]

    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]

    if missing_columns:

        message = (
            "ستون‌های زیر در فایل Excel "
            "معدوم‌سازی واکسن وجود ندارند: " + ", ".join(missing_columns)
        )

        print("=" * 80)
        print("IMPORT STOPPED - MISSING COLUMNS")
        print(message)
        print("=" * 80)

        return {
            "inserted": 0,
            "skipped": 0,
            "failed": 0,
            "missing_units": [],
            "missing_epidemiology_units": [],
            "warnings": [message],
        }

    # --------------------------------------------------------
    # Unit cache
    #
    # کلید Cache:
    # کد واحد اپیدمیولوژیک
    #
    # فقط برای کدهای 190 استفاده می‌شود.
    # --------------------------------------------------------

    unit_cache = {}

    # ========================================================
    # Rows
    # ========================================================

    for index, row in df.iterrows():

        excel_row = index + 2

        try:

            # =================================================
            # Source / Epidemiology Unit Code
            # =================================================

            source_unit_code = clean_code(row["کد واحد اپیدمیولوژیک"])

            source_unit_name = normalize_text(row["نام واحد اپیدمیولوژیک"])

            # -------------------------------------------------
            # Missing source unit code
            # -------------------------------------------------

            if source_unit_code is None:

                skipped += 1

                warnings.append(
                    f"ردیف {excel_row}: "
                    "کد واحد اپیدمیولوژیک وجود ندارد "
                    "و رکورد وارد نشد."
                )

                print(f"Row {excel_row}: " "SKIPPED - Source Unit Code is empty")

                continue

            # -------------------------------------------------
            # Zanjan filter
            # -------------------------------------------------

            if not source_unit_code.startswith("190"):

                skipped += 1

                warnings.append(
                    f"ردیف {excel_row}: "
                    f"کد واحد اپیدمیولوژیک "
                    f"«{source_unit_code}» "
                    "با 190 شروع نمی‌شود و مربوط به "
                    "واحدهای زنجان محسوب نمی‌شود."
                )

                print(
                    f"Row {excel_row}: "
                    f"SKIPPED - Non-Zanjan Unit Code: "
                    f"{source_unit_code}"
                )

                continue

            # =================================================
            # Distribution Code
            # =================================================

            code = clean_code(row["DistributionVaccineCenterVCode"])

            if code is None:

                skipped += 1

                warnings.append(
                    f"ردیف {excel_row}: "
                    "کد توزیع واکسن وجود ندارد "
                    "و رکورد وارد نشد."
                )

                print(f"Row {excel_row}: " "SKIPPED - Distribution Code is empty")

                continue

            # =================================================
            # EVERYTHING DATABASE-RELATED
            # IS INSIDE SAVEPOINT
            # =================================================

            try:

                with db.begin_nested():

                    # =========================================
                    # Duplicate
                    # =========================================

                    exists = (
                        db.query(GISVaccineDisposal)
                        .filter(
                            GISVaccineDisposal.distribution_vaccine_center_vcode == code
                        )
                        .first()
                    )

                    if exists:

                        skipped += 1

                        print(f"Row {excel_row}: " f"SKIPPED - Already exists: {code}")

                        continue

                    # =========================================
                    # Find source epidemiology unit
                    # =========================================

                    source_unit_key = normalize_compare(source_unit_code)

                    if source_unit_key in unit_cache:

                        unit = unit_cache[source_unit_key]

                    else:

                        # -------------------------------------
                        # First: exact code
                        # -------------------------------------

                        unit = (
                            db.query(GISEpidemiologyUnit)
                            .filter(GISEpidemiologyUnit.unit_code == source_unit_code)
                            .first()
                        )

                        # -------------------------------------
                        # Second: safe normalized search
                        # -------------------------------------

                        if unit is None:

                            candidate_units = (
                                db.query(GISEpidemiologyUnit)
                                .filter(GISEpidemiologyUnit.unit_code.like("190%"))
                                .all()
                            )

                            for candidate in candidate_units:

                                candidate_code = clean_code(candidate.unit_code)

                                if candidate_code == source_unit_code:

                                    unit = candidate
                                    break

                        # -------------------------------------
                        # Source unit not found
                        # -------------------------------------

                        if unit is None:

                            failed += 1

                            if source_unit_code not in missing_unit_codes:

                                missing_unit_codes.add(source_unit_code)

                                missing_units.append(
                                    {
                                        "row": excel_row,
                                        "unit_code": source_unit_code,
                                        "unit_name": source_unit_name,
                                        "message": (
                                            "واحد اپیدمیولوژیک "
                                            "با این کد در جدول "
                                            "gis_epidemiology_units "
                                            "ثبت نشده است."
                                        ),
                                    }
                                )

                            warnings.append(
                                f"ردیف {excel_row}: "
                                f"واحد اپیدمیولوژیک با کد "
                                f"«{source_unit_code}» "
                                "در سامانه پیدا نشد."
                            )

                            print(
                                f"Row {excel_row}: "
                                f"FAILED - Source Unit Not Found: "
                                f"{source_unit_code}"
                            )

                            # فقط همین SAVEPOINT rollback می‌شود
                            continue

                        # -------------------------------------
                        # Cache
                        # -------------------------------------

                        unit_cache[source_unit_key] = unit

                    # =========================================
                    # Create record
                    # =========================================

                    vaccine_status = clean_string(row["وضعیت"])

                    item = GISVaccineDisposal(
                        # -------------------------------------
                        # Distribution
                        # -------------------------------------
                        distribution_vaccine_center_vcode=code,
                        distribution_no=clean_string(row["شماره توزیع"]),
                        distribution_date=convert_date(row["تاریخ توزیع"]),
                        distribution_type=normalize_text(row["نوع توزیع"]),
                        distribution_status_id=clean_int(row["DistributionStatusId"]),
                        # -------------------------------------
                        # Source / Epidemiology Unit
                        # -------------------------------------
                        epidemiology_unit_id=unit.id,
                        province_name=normalize_text(row["استان"]),
                        county_name=normalize_text(row["شهرستان"]),
                        epidemiology_unit_code=source_unit_code,
                        epidemiology_unit_name=source_unit_name,
                        epidemiology_unit_type=normalize_text(
                            row["نوع واحد اپیدمیولوژیک"]
                        ),
                        # -------------------------------------
                        # Destination
                        # -------------------------------------
                        destination_province=normalize_text(row["استان واحد مقصد"]),
                        destination_county=normalize_text(row["شهر واحد مقصد"]),
                        destination_unit_code=clean_code(row["کد واحد مقصد"]),
                        destination_unit_name=normalize_text(row["نام واحد مقصد"]),
                        destination_unit_type=normalize_text(row["نوع واحد مقصد"]),
                        # -------------------------------------
                        # Vaccine
                        # -------------------------------------
                        vaccine_type=normalize_text(row["نوع واکسن"]),
                        vaccine_brand=normalize_text(row["نام تجاری واکسن"]),
                        manufacturer=normalize_text(row["کارخانه سازنده"]),
                        batch_number=clean_string(row["سری ساخت"]),
                        vaccine_status=vaccine_status,
                        vaccine_shape=normalize_text(row["شکل واکسن"]),
                        # -------------------------------------
                        # Quantity
                        # -------------------------------------
                        package_count=clean_int(row["تعداد بسته"]),
                        dose_volume=clean_float(row["حجم/ دز هر بسته"]),
                        unit_name=normalize_text(row["واحد"]),
                        # -------------------------------------
                        # User
                        # -------------------------------------
                        user_code=clean_code(row["کد کاربر"]),
                        user_name=normalize_text(row["نام کاربر"]),
                        registration_date=convert_date(row["تاریخ ثبت"]),
                        # -------------------------------------
                        # Disposal fields
                        # -------------------------------------
                    )

                    # =========================================
                    # Insert
                    # =========================================

                    db.add(item)

                    db.flush()

                # =================================================
                # SAVEPOINT SUCCESS
                # =================================================

                inserted += 1

                print(
                    f"Row {excel_row}: "
                    f"INSERTED - "
                    f"Distribution Code: {code} - "
                    f"Source Unit: {source_unit_code}"
                )

            except Exception as exc:

                # =================================================
                # SAVEPOINT ERROR
                # =================================================

                failed += 1

                warning_message = f"خطا در Import ردیف " f"{excel_row}: {str(exc)}"

                warnings.append(warning_message)

                print(f"Row {excel_row}: " f"FAILED - {str(exc)}")

                traceback.print_exc()

                # -----------------------------------------------
                # بسیار مهم:
                #
                # begin_nested() باعث شده rollback فقط روی
                # همین ردیف اعمال شود.
                #
                # Transaction اصلی سالم می‌ماند.
                # -----------------------------------------------

                continue

        except Exception as exc:

            # =================================================
            # Unexpected row-level error
            # =================================================

            failed += 1

            warning_message = (
                f"خطای غیرمنتظره در Import ردیف " f"{excel_row}: {str(exc)}"
            )

            warnings.append(warning_message)

            print(f"Row {excel_row}: " f"UNEXPECTED FAILURE - {str(exc)}")

            traceback.print_exc()

            continue
    # ========================================================
    # Final Commit
    # ========================================================

    try:

        db.commit()

    except Exception as exc:

        db.rollback()

        print("=" * 80)
        print("FINAL COMMIT FAILED")
        print("=" * 80)

        traceback.print_exc()

        warnings.append(("خطا در ثبت نهایی اطلاعات " f"در دیتابیس: {str(exc)}"))

        return {
            "inserted": inserted,
            "skipped": skipped,
            "failed": failed,
            "missing_units": missing_units,
            "missing_epidemiology_units": missing_units,
            "warnings": normalize_warnings(warnings),
        }

    # ========================================================
    # Final Result
    # ========================================================

    print("=" * 80)
    print("VACCINE DISPOSAL IMPORT RESULT")
    print("=" * 80)

    print(f"Inserted={inserted}")

    print(f"Skipped={skipped}")

    print(f"Failed={failed}")

    print(f"Warnings={len(warnings)}")

    print(f"Missing Source Units={len(missing_units)}")

    if missing_units:

        print("-" * 80)
        print("MISSING SOURCE / EPIDEMIOLOGY UNITS")

        for unit_info in missing_units:

            print(
                f"Code={unit_info.get('unit_code')} | "
                f"Name={unit_info.get('unit_name')} | "
                f"Row={unit_info.get('row')}"
            )

    print("=" * 80)

    return {
        "inserted": inserted,
        "skipped": skipped,
        "failed": failed,
        "missing_units": missing_units,
        "missing_epidemiology_units": missing_units,
        "warnings": normalize_warnings(warnings),
    }
