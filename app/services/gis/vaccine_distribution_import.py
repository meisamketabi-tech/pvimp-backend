print("=" * 80)
print("VACCINE DISTRIBUTION IMPORT MODULE LOADED")
print("=" * 80)

import traceback

import pandas as pd
from sqlalchemy.orm import Session

from app.db.models.gis_epidemiology_unit import GISEpidemiologyUnit
from app.db.models.gis_vaccine_distribution import GISVaccineDistribution

# ============================================================
# Helpers
# ============================================================


def clean_string(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value in ("", "'"):
        return None

    return value


def clean_int(value):
    if pd.isna(value):
        return None

    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None


def clean_float(value):
    if pd.isna(value):
        return None

    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def convert_date(value):
    if pd.isna(value):
        return None

    try:
        return pd.to_datetime(value).date()
    except (ValueError, TypeError):
        return None


# ============================================================
# Import Vaccine Distribution
# ============================================================


def import_vaccine_distribution(
    db: Session,
    file_path: str,
):
    print("=" * 80)
    print("VACCINE DISTRIBUTION IMPORT")
    print(f"FILE: {file_path}")
    print("=" * 80)

    inserted = 0
    skipped = 0
    failed = 0

    warnings = []

    # نگهداری واحدهای مقصد پیدا نشده
    # ساختار:
    # {
    #     "19041050014": {
    #         "unit_code": "...",
    #         "unit_name": "...",
    #         "rows": [2, 3, 4]
    #     }
    # }
    missing_units = {}

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
            "warnings": [f"امکان خواندن فایل Excel وجود ندارد: {exc}"],
        }

    print(f"Rows found: {len(df)}")

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

        message = "ستون‌های زیر در فایل Excel وجود ندارند: " + ", ".join(
            missing_columns
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
            "warnings": [message],
        }

    # --------------------------------------------------------
    # Rows
    # --------------------------------------------------------

    for index, row in df.iterrows():

        excel_row = index + 2

        try:

            # =================================================
            # Distribution Code
            # =================================================

            code = clean_string(row["DistributionVaccineCenterVCode"])

            if code is None:

                skipped += 1

                warnings.append(
                    f"ردیف {excel_row}: "
                    "کد توزیع واکسن وجود ندارد و این ردیف وارد نشد."
                )

                print(f"Row {excel_row}: " "SKIPPED - Distribution code is empty")

                continue

            # =================================================
            # Duplicate
            # =================================================

            exists = (
                db.query(GISVaccineDistribution)
                .filter(
                    GISVaccineDistribution.distribution_vaccine_center_vcode == code
                )
                .first()
            )

            if exists:

                skipped += 1

                print(f"Row {excel_row}: " f"SKIPPED - Already exists: {code}")

                continue

            # =================================================
            # IMPORTANT:
            # Epidemiology validation MUST use DESTINATION UNIT
            # =================================================

            destination_unit_code = clean_string(row["کد واحد مقصد"])

            destination_unit_name = clean_string(row["نام واحد مقصد"])

            # -------------------------------------------------
            # Destination code missing
            # -------------------------------------------------

            if destination_unit_code is None:

                failed += 1

                warnings.append(
                    f"ردیف {excel_row}: "
                    "کد واحد مقصد وجود ندارد؛ "
                    "این ردیف وارد سیستم نشد."
                )

                print(f"Row {excel_row}: " "FAILED - Destination unit code is empty")

                continue

            # =================================================
            # Find DESTINATION epidemiology unit
            # =================================================

            destination_unit = (
                db.query(GISEpidemiologyUnit)
                .filter(GISEpidemiologyUnit.unit_code == destination_unit_code)
                .first()
            )

            # -------------------------------------------------
            # Destination unit not found
            # -------------------------------------------------

            if destination_unit is None:

                failed += 1

                if destination_unit_code not in missing_units:

                    missing_units[destination_unit_code] = {
                        "unit_code": destination_unit_code,
                        "unit_name": destination_unit_name,
                        "rows": [],
                    }

                missing_units[destination_unit_code]["rows"].append(excel_row)

                print(
                    f"Row {excel_row}: "
                    f"Destination Unit Not Found: "
                    f"{destination_unit_code}"
                )

                continue

            # =================================================
            # Source / Sender information
            #
            # IMPORTANT:
            # این اطلاعات فقط از فایل خوانده می‌شوند.
            # برای Validation استفاده نمی‌شوند.
            # =================================================

            source_unit_code = clean_string(row["کد واحد اپیدمیولوژیک"])

            source_unit_name = clean_string(row["نام واحد اپیدمیولوژیک"])

            source_unit_type = clean_string(row["نوع واحد اپیدمیولوژیک"])

            # =================================================
            # Create item
            # =================================================

            item = GISVaccineDistribution(
                distribution_vaccine_center_vcode=code,
                distribution_no=clean_string(row["شماره توزیع"]),
                # ---------------------------------------------
                # IMPORTANT:
                # FK points to DESTINATION epidemiology unit
                # ---------------------------------------------
                epidemiology_unit_id=destination_unit.id,
                province_name=clean_string(row["استان"]),
                county_name=clean_string(row["شهرستان"]),
                # ---------------------------------------------
                # Source / Sender information
                # ---------------------------------------------
                epidemiology_unit_code=source_unit_code,
                epidemiology_unit_name=source_unit_name,
                epidemiology_unit_type=source_unit_type,
                # ---------------------------------------------
                # Distribution
                # ---------------------------------------------
                distribution_type=clean_string(row["نوع توزیع"]),
                distribution_status_id=clean_int(row["DistributionStatusId"]),
                distribution_date=convert_date(row["تاریخ توزیع"]),
                # ---------------------------------------------
                # Destination
                # ---------------------------------------------
                destination_province=clean_string(row["استان واحد مقصد"]),
                destination_county=clean_string(row["شهر واحد مقصد"]),
                destination_unit_code=destination_unit_code,
                destination_unit_name=destination_unit_name,
                destination_unit_type=clean_string(row["نوع واحد مقصد"]),
                # ---------------------------------------------
                # Vaccine
                # ---------------------------------------------
                vaccine_type=clean_string(row["نوع واکسن"]),
                vaccine_brand=clean_string(row["نام تجاری واکسن"]),
                manufacturer=clean_string(row["کارخانه سازنده"]),
                batch_number=clean_string(row["سری ساخت"]),
                vaccine_status=clean_string(row["وضعیت"]),
                vaccine_shape=clean_string(row["شکل واکسن"]),
                package_count=clean_int(row["تعداد بسته"]),
                dose_volume=clean_float(row["حجم/ دز هر بسته"]),
                unit_name=clean_string(row["واحد"]),
                # ---------------------------------------------
                # User
                # ---------------------------------------------
                user_code=clean_string(row["کد کاربر"]),
                user_name=clean_string(row["نام کاربر"]),
                registration_date=convert_date(row["تاریخ ثبت"]),
            )

            # =================================================
            # Save row
            # =================================================

            with db.begin_nested():

                db.add(item)
                db.flush()

            inserted += 1

            print(
                f"Row {excel_row}: "
                f"INSERTED - Code: {code} "
                f"- Destination: {destination_unit_code}"
            )

        except Exception as exc:

            failed += 1

            error_message = f"خطا در Import ردیف {excel_row}: {str(exc)}"

            warnings.append(error_message)

            print(f"Row {excel_row}: FAILED - {str(exc)}")

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

        warnings.append(f"خطا در ثبت نهایی اطلاعات: {exc}")

        return {
            "inserted": inserted,
            "skipped": skipped,
            "failed": failed,
            "missing_units": list(missing_units.values()),
            "warnings": warnings,
        }

    # ========================================================
    # Missing Units
    # ========================================================

    missing_unit_list = list(missing_units.values())

    # ========================================================
    # Add readable warnings
    # ========================================================

    for unit_info in missing_unit_list:

        unit_code = str(unit_info.get("unit_code", "")).strip()

        unit_name = str(unit_info.get("unit_name") or "").strip()

        rows = unit_info.get("rows", [])

        if isinstance(rows, list):

            row_text = ", ".join(str(row) for row in rows)

        else:

            row_text = str(rows)

        message = (
            f"واحد مقصد با کد «{unit_code}» "
            "در بخش واحدهای اپیدمیولوژیک سامانه ثبت نشده است."
        )

        if unit_name:

            message += f" نام واحد: «{unit_name}»."

        if row_text:

            message += f" ردیف‌های فایل: {row_text}."

        warnings.append(message)

    # ========================================================
    # Result
    # ========================================================

    print("=" * 80)
    print("VACCINE DISTRIBUTION IMPORT RESULT")
    print("=" * 80)

    print(f"Inserted={inserted}")
    print(f"Skipped={skipped}")
    print(f"Failed={failed}")
    print(f"Warnings={len(warnings)}")
    print(f"Missing Destination Epidemiology Units=" f"{len(missing_unit_list)}")

    if missing_unit_list:

        print("-" * 80)
        print("MISSING DESTINATION EPIDEMIOLOGY UNITS")

        for unit_info in missing_unit_list:

            print(
                f"Code={unit_info.get('unit_code')} "
                f"Name={unit_info.get('unit_name')} "
                f"Rows={unit_info.get('rows')}"
            )

    print("=" * 80)

    # ========================================================
    # IMPORTANT:
    # missing_units contains objects,
    # warnings contains strings only.
    # ========================================================

    return {
        "inserted": inserted,
        "skipped": skipped,
        "failed": failed,
        "missing_units": missing_unit_list,
        "warnings": warnings,
    }
