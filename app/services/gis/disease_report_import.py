import math
from datetime import date, datetime
from typing import Any

import pandas as pd
from convertdate import persian
from sqlalchemy.orm import Session

from app.db.models.gis_disease import GISDisease
from app.db.models.gis_disease_report import GISDiseaseReport
from app.db.models.gis_epidemiology_unit import GISEpidemiologyUnit

# =========================================================
# Excel column mapping
# =========================================================

COLUMN_MAP = {
    # شناسه فرم
    "ObservationDetailVCode": "observation_detail_vcode",
    "ObservationVCode": "observation_vcode",
    # جغرافیا
    "کد استان": "province_code",
    "استان": "province_name",
    "کد شهرستان": "county_code",
    "شهرستان": "county_name",
    # واحد اپیدمیولوژیک
    "نام واحد اپیدمیولوژیک": "epidemiology_unit_name",
    "کد واحد اپیدمیولوژیک": "epidemiology_unit_code",
    "نوع واحد اپیدمیولوژیک": "epidemiology_unit_type",
    # بیماری
    "نام بیماری": "disease_name",
    # دام
    "نوع دام": "animal_type",
    # تاریخ
    "تاریخ شروع بیماری": "disease_start_date",
    # آمار
    "تعداد کل دام": "total_animals",
    "تعداد دام مبتلا": "infected_count",
    "تعداد تلفات": "death_count",
    "تعداد دام کشتار شده": "slaughtered_count",
    "تعداد دام معدوم شده": "destroyed_count",
    # نمونه
    "نمونه برداری": "sampling",
    # سیستم قدیم
    "شناسه اطلاعات قدیم": "old_system_id",
    "کد واحد قدیم": "old_unit_code",
    # سایر
    "گروه سنی": "age_group",
    "حیوان گزنده": "biting_animal",
    "نوع پروانه بهره برداری": "operation_license_type",
    # کاربر
    "کد کاربر ثبت کننده": "creator_user_code",
    "کاربر ثبت کننده": "creator_user_name",
    # واحد مبدا
    "کد واحد مبدا": "source_unit_code",
    "نام واحد مبدا": "source_unit_name",
    "نوع واحد مبدا": "source_unit_type",
}


# =========================================================
# Helpers
# =========================================================


def clean_value(value: Any) -> Any:
    """Convert Excel empty/NaN values to None."""

    if value is None:
        return None

    if isinstance(value, float) and math.isnan(value):
        return None

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    if isinstance(value, str):
        value = value.strip()

        if not value:
            return None

    return value


def normalize_digits(value: Any) -> str:
    """Convert Persian/Arabic digits to English digits."""

    translation = str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
        "01234567890123456789",
    )

    return str(value).translate(translation)


def clean_string(value: Any) -> str | None:
    """Return a cleaned string or None."""

    value = clean_value(value)

    if value is None:
        return None

    value = normalize_digits(value).strip()

    return value or None


def clean_int(value: Any) -> int | None:
    """Convert Excel numeric value to int."""

    value = clean_value(value)

    if value is None:
        return None

    try:
        if isinstance(value, str):
            value = normalize_digits(value)
            value = value.replace(",", "")
            value = value.replace("٬", "")
            value = value.strip()

        return int(float(value))

    except (TypeError, ValueError):
        return None


def convert_jalali_date(value: Any) -> date | None:
    """
    Convert Excel date value to Gregorian date.

    Supports:
    - datetime
    - pandas.Timestamp
    - date
    - Jalali date
    - Gregorian date
    - Persian/Arabic digits
    - /, -, . separators
    """

    value = clean_value(value)

    if value is None:
        return None

    if isinstance(value, pd.Timestamp):
        return value.date()

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    value = normalize_digits(value)

    if not value:
        return None

    if " " in value:
        value = value.split(" ", 1)[0]

    value = value.replace("-", "/")
    value = value.replace(".", "/")

    parts = [part.strip() for part in value.split("/")]

    if len(parts) != 3:
        return None

    try:
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
    except (TypeError, ValueError):
        return None

    try:

        # Jalali
        if 1200 <= year <= 1600:
            gy, gm, gd = persian.to_gregorian(
                year,
                month,
                day,
            )

            return date(
                gy,
                gm,
                gd,
            )

        # Gregorian
        if 1900 <= year <= 2200:
            return date(
                year,
                month,
                day,
            )

    except (TypeError, ValueError, OverflowError):
        return None

    return None


# =========================================================
# Disease
# =========================================================


def get_or_create_disease(
    db: Session,
    disease_name: Any,
) -> GISDisease | None:

    disease_name = clean_string(disease_name)

    if not disease_name:
        return None

    disease = (
        db.query(GISDisease).filter(GISDisease.disease_name == disease_name).first()
    )

    if disease:
        return disease

    disease = GISDisease(
        disease_name=disease_name,
    )

    db.add(disease)
    db.flush()

    return disease


# =========================================================
# Import
# =========================================================


def import_disease_reports(
    db: Session,
    file_path: str,
) -> dict[str, Any]:

    df = pd.read_excel(file_path)

    # Normalize headers.
    df.columns = [str(column).strip() for column in df.columns]

    df.rename(
        columns=COLUMN_MAP,
        inplace=True,
    )

    inserted = 0
    skipped = 0
    failed = 0

    missing_units: list[dict[str, Any]] = []
    warnings: list[str] = []

    # -----------------------------------------------------
    # Process rows
    # -----------------------------------------------------

    for excel_index, excel_row in df.iterrows():

        row_number = excel_index + 2

        try:

            # Every row has its own SAVEPOINT.
            with db.begin_nested():

                row = excel_row.apply(clean_value)

                observation_detail_vcode = clean_string(
                    row.get("observation_detail_vcode")
                )

                # -------------------------------------------------
                # Required identifier
                # -------------------------------------------------

                if not observation_detail_vcode:

                    failed += 1

                    warnings.append(
                        f"ردیف {row_number}: " "ObservationDetailVCode خالی است."
                    )

                    continue

                # -------------------------------------------------
                # Duplicate
                # -------------------------------------------------

                existing = (
                    db.query(GISDiseaseReport)
                    .filter(
                        GISDiseaseReport.observation_detail_vcode
                        == observation_detail_vcode
                    )
                    .first()
                )

                if existing:

                    skipped += 1

                    continue

                # -------------------------------------------------
                # Epidemiology unit
                # -------------------------------------------------

                unit_code = clean_string(row.get("epidemiology_unit_code"))

                unit = None

                if unit_code:

                    unit = (
                        db.query(GISEpidemiologyUnit)
                        .filter(GISEpidemiologyUnit.unit_code == unit_code)
                        .first()
                    )

                # -------------------------------------------------
                # Missing unit
                # -------------------------------------------------

                if unit is None:

                    missing_units.append(
                        {
                            "row": row_number,
                            "unit_code": unit_code,
                            "unit_name": clean_string(
                                row.get("epidemiology_unit_name")
                            ),
                            "message": ("واحد اپیدمیولوژیک " "در سیستم ثبت نشده است."),
                        }
                    )

                    skipped += 1

                    continue

                # -------------------------------------------------
                # Disease
                # -------------------------------------------------

                disease_name = clean_string(row.get("disease_name"))

                disease = get_or_create_disease(
                    db=db,
                    disease_name=disease_name,
                )

                # -------------------------------------------------
                # Create report
                # -------------------------------------------------

                report = GISDiseaseReport(
                    # شناسه فرم
                    observation_detail_vcode=(observation_detail_vcode),
                    observation_vcode=clean_string(row.get("observation_vcode")),
                    # جغرافیا
                    province_code=clean_string(row.get("province_code")),
                    province_name=clean_string(row.get("province_name")),
                    county_code=clean_string(row.get("county_code")),
                    county_name=clean_string(row.get("county_name")),
                    # واحد اپیدمیولوژیک
                    epidemiology_unit_id=unit.id,
                    epidemiology_unit_code=clean_string(
                        row.get("epidemiology_unit_code")
                    ),
                    epidemiology_unit_name=clean_string(
                        row.get("epidemiology_unit_name")
                    ),
                    epidemiology_unit_type=clean_string(
                        row.get("epidemiology_unit_type")
                    ),
                    # بیماری
                    disease_id=(disease.id if disease else None),
                    disease_name=disease_name,
                    # دام
                    animal_type=clean_string(row.get("animal_type")),
                    # تاریخ
                    disease_start_date=(
                        convert_jalali_date(row.get("disease_start_date"))
                    ),
                    # آمار
                    total_animals=clean_int(row.get("total_animals")),
                    infected_count=clean_int(row.get("infected_count")),
                    death_count=clean_int(row.get("death_count")),
                    slaughtered_count=clean_int(row.get("slaughtered_count")),
                    destroyed_count=clean_int(row.get("destroyed_count")),
                    # نمونه
                    sampling=clean_string(row.get("sampling")),
                    # سیستم قدیم
                    old_system_id=clean_string(row.get("old_system_id")),
                    age_group=clean_string(row.get("age_group")),
                    old_unit_code=clean_string(row.get("old_unit_code")),
                    # سایر
                    biting_animal=clean_string(row.get("biting_animal")),
                    operation_license_type=clean_string(
                        row.get("operation_license_type")
                    ),
                    # کاربر
                    creator_user_code=clean_string(row.get("creator_user_code")),
                    creator_user_name=clean_string(row.get("creator_user_name")),
                    # واحد مبدا
                    source_unit_code=clean_string(row.get("source_unit_code")),
                    source_unit_name=clean_string(row.get("source_unit_name")),
                    source_unit_type=clean_string(row.get("source_unit_type")),
                )

                db.add(report)

                # Force DB constraints now.
                db.flush()

                inserted += 1

        except Exception as exc:

            failed += 1

            warnings.append(f"ردیف {row_number}: {exc}")

    # -----------------------------------------------------
    # Final commit
    # -----------------------------------------------------

    try:

        db.commit()

    except Exception:

        db.rollback()
        raise

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    if missing_units:

        warnings.append(
            "برخی رکوردها به دلیل ثبت نبودن " "واحد اپیدمیولوژیک وارد نشدند."
        )

    return {
        "inserted": inserted,
        "skipped": skipped,
        "failed": failed,
        "missing_units": missing_units,
        "warnings": warnings,
    }
