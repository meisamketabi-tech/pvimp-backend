import math
from datetime import date, datetime
from typing import Any

import pandas as pd
from convertdate import persian
from sqlalchemy.orm import Session

from app.db.models.gis_disease import GISDisease
from app.db.models.gis_disease_occurrence import GISDiseaseOccurrence
from app.db.models.gis_epidemiology_unit import GISEpidemiologyUnit

# =========================================================
# Excel column mapping
# =========================================================

COLUMN_MAP = {
    # شناسه فرم
    "ObservationDetailVCode": "observation_detail_vcode",
    "ObservationVCode": "observation_vcode",
    # واحد اپیدمیولوژیک
    "کد واحد اپیدمیولوژیک": "epidemiology_unit_code",
    "نام واحد اپیدمیولوژیک": "epidemiology_unit_name",
    "نوع واحد اپیدمیولوژیک": "epidemiology_unit_type",
    # جغرافیا
    "کد استان": "province_code",
    "استان": "province_name",
    "کد شهرستان": "county_code",
    "شهرستان": "county_name",
    # بیماری
    "نام بیماری": "disease_name",
    # دام
    "نوع دام": "animal_type",
    # تاریخ‌ها
    "تاریخ شروع بیماری": "start_date",
    "ReportDate": "report_date",
    "تاریخ ثبت": "registration_date",
    # آمار دام
    "تعداد دام در معرض خطر": "exposed_count",
    "تعداد دام": "animal_count",
    "تعداد دام کشتار شده": "slaughtered_count",
    "تعداد دام مبتلا": "infected_count",
    "تعداد دام تلف شده": "dead_count",
    "تعداد کل دام": "total_animals",
    # گزارش
    "شماره گزارش بیماری": "report_number",
    "ReportInfo": "report_info",
    # مختصات
    "X": "longitude",
    "Y": "latitude",
    # کاربر
    "عنوان کاربر": "user_name",
    "کد کاربر": "user_code",
    "ExperterNames": "expert_names",
    # وضعیت
    "وضعیت": "status",
    # سیستم قدیم
    "کد پنجره": "window_code",
    "نوع پروانه بهره برداری": "operation_license_type",
    "شناسه اطلاعات قدیم": "old_system_id",
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


def clean_float(value: Any) -> float | None:
    """Convert Excel numeric value to float."""

    value = clean_value(value)

    if value is None:
        return None

    try:
        if isinstance(value, str):
            value = normalize_digits(value)
            value = value.replace(",", "")
            value = value.replace("٬", "")
            value = value.strip()

        return float(value)

    except (TypeError, ValueError):
        return None


def convert_jalali_date(value: Any) -> date | None:
    """
    Convert Excel date value to Gregorian date.

    Supported:
    - datetime
    - pandas.Timestamp
    - date
    - Jalali dates
    - Gregorian dates
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

    # Remove time part.
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
    """Find an existing disease or create it."""

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


def import_disease_occurrences(
    db: Session,
    file_path: str,
) -> dict[str, Any]:

    df = pd.read_excel(file_path)

    # Normalize Excel headers.
    df.columns = [str(column).strip() for column in df.columns]

    # Rename according to mapping.
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

        # Important:
        # Each row gets its own SAVEPOINT.
        # A bad row must NOT rollback previous successful rows.
        try:
            with db.begin_nested():

                row = excel_row.apply(clean_value)

                observation_detail_vcode = clean_string(
                    row.get("observation_detail_vcode")
                )

                observation_vcode = clean_string(row.get("observation_vcode"))

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
                    db.query(GISDiseaseOccurrence)
                    .filter(
                        GISDiseaseOccurrence.observation_detail_vcode
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
                # Missing epidemiology unit
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
                # Create occurrence
                # -------------------------------------------------

                occurrence = GISDiseaseOccurrence(
                    # شناسه فرم
                    observation_detail_vcode=(observation_detail_vcode),
                    observation_vcode=(observation_vcode),
                    # -------------------------------------------------
                    # Geography
                    # -------------------------------------------------
                    province_code=clean_string(row.get("province_code")),
                    province_name=clean_string(row.get("province_name")),
                    county_code=clean_string(row.get("county_code")),
                    county_name=clean_string(row.get("county_name")),
                    # -------------------------------------------------
                    # Epidemiology unit
                    # -------------------------------------------------
                    epidemiology_unit_id=unit.id,
                    epidemiology_unit_code=(unit_code),
                    epidemiology_unit_name=clean_string(
                        row.get("epidemiology_unit_name")
                    ),
                    epidemiology_unit_type=clean_string(
                        row.get("epidemiology_unit_type")
                    ),
                    # -------------------------------------------------
                    # Disease
                    # -------------------------------------------------
                    disease_id=(disease.id if disease else None),
                    disease_name=disease_name,
                    # -------------------------------------------------
                    # Animal
                    # -------------------------------------------------
                    animal_type=clean_string(row.get("animal_type")),
                    # -------------------------------------------------
                    # Dates
                    # -------------------------------------------------
                    start_date=convert_jalali_date(row.get("start_date")),
                    report_date=convert_jalali_date(row.get("report_date")),
                    registration_date=convert_jalali_date(row.get("registration_date")),
                    # -------------------------------------------------
                    # Animal statistics
                    # -------------------------------------------------
                    exposed_count=clean_int(row.get("exposed_count")),
                    animal_count=clean_int(row.get("animal_count")),
                    infected_count=clean_int(row.get("infected_count")),
                    dead_count=clean_int(row.get("dead_count")),
                    slaughtered_count=clean_int(row.get("slaughtered_count")),
                    total_animals=clean_int(row.get("total_animals")),
                    # -------------------------------------------------
                    # Sampling
                    # -------------------------------------------------
                    sample_taken=False,
                    # -------------------------------------------------
                    # Report
                    # -------------------------------------------------
                    report_number=clean_string(row.get("report_number")),
                    report_info=clean_string(row.get("report_info")),
                    # -------------------------------------------------
                    # Coordinates
                    # -------------------------------------------------
                    longitude=clean_float(row.get("longitude")),
                    latitude=clean_float(row.get("latitude")),
                    # -------------------------------------------------
                    # User
                    # -------------------------------------------------
                    user_name=clean_string(row.get("user_name")),
                    user_code=clean_string(row.get("user_code")),
                    expert_names=clean_string(row.get("expert_names")),
                    # -------------------------------------------------
                    # Status
                    # -------------------------------------------------
                    status=clean_string(row.get("status")),
                    # -------------------------------------------------
                    # Old system
                    # -------------------------------------------------
                    window_code=clean_string(row.get("window_code")),
                    operation_license_type=clean_string(
                        row.get("operation_license_type")
                    ),
                    old_system_id=clean_string(row.get("old_system_id")),
                )

                db.add(occurrence)

                # Flush inside SAVEPOINT so DB constraint
                # errors are caught for this row only.
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
    # Summary warning
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
