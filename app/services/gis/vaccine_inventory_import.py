# ============================================================
# VACCINE INVENTORY IMPORT MODULE
# ============================================================

print("=" * 80)
print("VACCINE INVENTORY IMPORT MODULE LOADED")
print("=" * 80)

import traceback
import pandas as pd

from sqlalchemy.orm import Session

from app.db.models.gis_vaccine_inventory import GISVaccineInventory
from app.db.models.gis_epidemiology_unit import GISEpidemiologyUnit

# ============================================================
# HELPERS
# ============================================================


def clean_string(value):
    """
    Normalize Excel cell to string.
    Empty / NaN / "'" values become None.
    """

    if pd.isna(value):
        return None

    value = str(value).strip()

    if value in ("", "'"):
        return None

    # Remove Excel-style trailing .0 for numeric codes
    if value.endswith(".0"):
        value = value[:-2]

    return value


def clean_int(value):
    """
    Convert Excel value to integer.
    """

    if pd.isna(value):
        return None

    try:
        if isinstance(value, float):
            return int(value)

        value = str(value).strip()

        if value.endswith(".0"):
            value = value[:-2]

        return int(value)

    except Exception:
        return None


def clean_float(value):
    """
    Convert Excel value to float.
    """

    if pd.isna(value):
        return None

    try:
        return float(value)

    except Exception:
        return None


def convert_date(value):
    """
    Convert Excel date to Python date.
    """

    if pd.isna(value):
        return None

    try:
        return pd.to_datetime(value).date()

    except Exception:
        return None


# ============================================================
# REQUIRED EXCEL COLUMNS
# ============================================================

REQUIRED_COLUMNS = [
    "DistributionVaccineCenterVCode",
    "استان",
    "شهرستان",
    "نوع واحد اپیدمیولوژیک",
    "کد واحد اپیدمیولوژیک",
    "نام واحد اپیدمیولوژیک",
    "کد کاربر",
    "نام کاربر",
    "شماره توزیع",
    "تاریخ توزیع",
    "نوع واکسن",
    "نام تجاری واکسن",
    "کارخانه سازنده",
    "سری ساخت",
    "شکل واکسن",
    "تعداد بسته",
    "حجم/ دز هر بسته",
    "واحد",
    "تاریخ ثبت",
    "تاریخ تولید/واردات",
    "تاریخ انقضا",
]


# ============================================================
# IMPORT
# ============================================================


def import_vaccine_inventory(
    db: Session,
    file_path: str,
):
    """
    Import Vaccine Inventory Excel file.

    Important:
    This form is specifically for Zanjan province.
    Therefore NO '190' unit-code filtering is performed.
    """

    print("=" * 80)
    print("VACCINE INVENTORY IMPORT")
    print(file_path)
    print("=" * 80)

    inserted = 0
    skipped = 0
    failed = 0
    warnings = []

    # --------------------------------------------------------
    # READ EXCEL
    # --------------------------------------------------------

    try:
        df = pd.read_excel(file_path)

    except Exception as exc:
        print("=" * 80)
        print("FAILED TO READ EXCEL FILE")
        traceback.print_exc()
        print("=" * 80)

        return {
            "inserted": 0,
            "skipped": 0,
            "failed": 1,
            "warnings": [f"خطا در خواندن فایل Excel: {exc}"],
        }

    print(f"ROWS: {len(df)}")

    # --------------------------------------------------------
    # NORMALIZE COLUMN NAMES
    # --------------------------------------------------------

    df.columns = [str(column).strip() for column in df.columns]

    # --------------------------------------------------------
    # CHECK REQUIRED COLUMNS
    # --------------------------------------------------------

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in df.columns
    ]

    if missing_columns:

        message = "ستون‌های زیر در فایل Excel وجود ندارند: " + ", ".join(
            missing_columns
        )

        print("=" * 80)
        print("INVALID EXCEL STRUCTURE")
        print(message)
        print("=" * 80)

        return {
            "inserted": 0,
            "skipped": 0,
            "failed": len(df),
            "warnings": [message],
        }

    # ========================================================
    # PROCESS ROWS
    # ========================================================

    for index, row in df.iterrows():

        excel_row = index + 2

        try:

            # ------------------------------------------------
            # DISTRIBUTION CENTER CODE
            # ------------------------------------------------

            code = clean_string(row["DistributionVaccineCenterVCode"])

            if code is None:

                skipped += 1

                warnings.append(
                    f"ردیف {excel_row}: " "کد DistributionVaccineCenterVCode خالی است."
                )

                continue

            # ------------------------------------------------
            # DUPLICATE CHECK
            # ------------------------------------------------

            exists = (
                db.query(GISVaccineInventory)
                .filter(GISVaccineInventory.distribution_vaccine_center_vcode == code)
                .first()
            )

            if exists:

                skipped += 1

                warnings.append(
                    f"ردیف {excel_row}: " f"رکورد با کد «{code}» قبلاً ثبت شده است."
                )

                continue

            # ------------------------------------------------
            # EPIDEMIOLOGY UNIT CODE
            # ------------------------------------------------

            unit_code = clean_string(row["کد واحد اپیدمیولوژیک"])

            if unit_code is None:

                skipped += 1

                warnings.append(f"ردیف {excel_row}: " "کد واحد اپیدمیولوژیک خالی است.")

                continue

            # ------------------------------------------------
            # FIND EPIDEMIOLOGY UNIT
            # ------------------------------------------------

            unit = (
                db.query(GISEpidemiologyUnit)
                .filter(GISEpidemiologyUnit.unit_code == unit_code)
                .first()
            )

            if unit is None:

                failed += 1

                warnings.append(
                    f"ردیف {excel_row}: "
                    f"واحد اپیدمیولوژیک با کد "
                    f"«{unit_code}» پیدا نشد."
                )

                print(f"ROW {excel_row}: " f"Unit Not Found: {unit_code}")

                continue

            # ------------------------------------------------
            # CREATE SAVEPOINT
            # ------------------------------------------------

            # خطای یک ردیف نباید transaction کل import
            # را خراب کند.

            with db.begin_nested():

                item = GISVaccineInventory(
                    distribution_vaccine_center_vcode=code,
                    epidemiology_unit_id=unit.id,
                    province_name=clean_string(row["استان"]),
                    county_name=clean_string(row["شهرستان"]),
                    epidemiology_unit_type=clean_string(row["نوع واحد اپیدمیولوژیک"]),
                    epidemiology_unit_code=unit_code,
                    epidemiology_unit_name=clean_string(row["نام واحد اپیدمیولوژیک"]),
                    user_code=clean_string(row["کد کاربر"]),
                    user_name=clean_string(row["نام کاربر"]),
                    distribution_no=clean_string(row["شماره توزیع"]),
                    distribution_date=convert_date(row["تاریخ توزیع"]),
                    vaccine_type=clean_string(row["نوع واکسن"]),
                    vaccine_brand=clean_string(row["نام تجاری واکسن"]),
                    manufacturer=clean_string(row["کارخانه سازنده"]),
                    batch_number=clean_string(row["سری ساخت"]),
                    vaccine_shape=clean_string(row["شکل واکسن"]),
                    package_count=clean_int(row["تعداد بسته"]),
                    dose_volume=clean_float(row["حجم/ دز هر بسته"]),
                    unit_name=clean_string(row["واحد"]),
                    registration_date=convert_date(row["تاریخ ثبت"]),
                    production_import_date=convert_date(row["تاریخ تولید/واردات"]),
                    expiration_date=convert_date(row["تاریخ انقضا"]),
                )

                db.add(item)

                db.flush()

            inserted += 1

            print(f"Row {excel_row}: INSERTED - {code}")

        # ====================================================
        # ROW ERROR
        # ====================================================

        except Exception as exc:

            failed += 1

            message = f"خطا در Import ردیف {excel_row}: {exc}"

            warnings.append(message)

            print("=" * 80)
            print(f"ROW {excel_row} ERROR")
            print("=" * 80)

            traceback.print_exc()

            try:
                print(row.to_dict())
            except Exception:
                pass

            print("=" * 80)

            # begin_nested() باعث می‌شود خطای این ردیف
            # transaction اصلی را خراب نکند.
            continue

    # ========================================================
    # FINAL COMMIT
    # ========================================================

    try:

        db.commit()

    except Exception as exc:

        db.rollback()

        print("=" * 80)
        print("FINAL COMMIT FAILED")
        traceback.print_exc()
        print("=" * 80)

        failed += inserted
        inserted = 0

        warnings.append(f"خطا در ثبت نهایی اطلاعات: {exc}")

    # ========================================================
    # RESULT
    # ========================================================

    print("=" * 80)
    print("VACCINE INVENTORY IMPORT RESULT")
    print("=" * 80)

    print(f"Inserted={inserted}")
    print(f"Skipped={skipped}")
    print(f"Failed={failed}")
    print(f"Warnings={len(warnings)}")

    print("=" * 80)

    return {
        "inserted": inserted,
        "skipped": skipped,
        "failed": failed,
        "warnings": warnings,
    }
