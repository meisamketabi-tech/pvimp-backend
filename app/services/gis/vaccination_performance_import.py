print("=" * 80)
print("VACCINATION PERFORMANCE IMPORT MODULE LOADED")
print("=" * 80)

import traceback

import pandas as pd
from sqlalchemy.orm import Session

from app.db.models.gis_vaccination_performance import (
    GISVaccinationPerformance,
)
from app.db.models.gis_epidemiology_unit import GISEpidemiologyUnit


# ============================================================
# Helpers
# ============================================================

def clean_string(value):
    """
    Convert Excel/pandas values to a clean string or None.

    Examples:
        NaN        -> None
        ""         -> None
        "  abc  "  -> "abc"
        "'"        -> None
    """
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except Exception:
        pass

    value = str(value).strip()

    if not value:
        return None

    if value == "'":
        return None

    # Handle values coming from Excel as numeric floats.
    # Example:
    #   12086460.0 -> "12086460"
    if value.endswith(".0"):
        try:
            numeric_value = float(value)

            if numeric_value.is_integer():
                return str(int(numeric_value))
        except Exception:
            pass

    return value


def clean_int(value):
    """
    Convert Excel/pandas value to integer or None.
    """
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except Exception:
        pass

    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def clean_float(value):
    """
    Convert Excel/pandas value to float or None.
    """
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except Exception:
        pass

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def clean_bool(value):
    """
    Convert Persian/English Excel boolean values to Python bool.

    Supported examples:

        دارد / بله / بلی / yes / true / 1 -> True
        ندارد / خیر / no / false / 0      -> False

    Empty/unknown values -> None
    """

    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except Exception:
        pass

    # Already a real Python bool
    if isinstance(value, bool):
        return value

    # Numeric boolean values
    if isinstance(value, (int, float)):
        if value == 1:
            return True

        if value == 0:
            return False

    value = str(value).strip().lower()

    if not value:
        return None

    true_values = {
        "دارد",
        "بله",
        "بلی",
        "yes",
        "true",
        "1",
        "y",
    }

    false_values = {
        "ندارد",
        "خیر",
        "no",
        "false",
        "0",
        "n",
    }

    if value in true_values:
        return True

    if value in false_values:
        return False

    # Unknown value
    print(f"WARNING: Unknown boolean value: {value!r}")

    return None


def convert_date(value):
    """
    Convert Excel date value to Python date.

    Important:
    This only performs a safe pandas datetime conversion.
    """
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except Exception:
        pass

    try:
        return pd.to_datetime(value).date()
    except Exception:
        return None


# ============================================================
# Import
# ============================================================

def import_vaccination_performance(
    db: Session,
    file_path: str,
):
    """
    Import vaccination performance records from Excel.

    Returns:
        {
            "inserted": int,
            "skipped": int,
            "failed": int,
        }
    """

    df = pd.read_excel(file_path)

    inserted = 0
    skipped = 0
    failed = 0

    print("=" * 80)
    print("Vaccination Performance Import")
    print("=" * 80)

    print("Columns:")
    print(df.columns.tolist())

    if not df.empty:
        print("First row:")
        print(df.iloc[0].to_dict())

    print("=" * 80)

    # --------------------------------------------------------
    # Validate required columns
    # --------------------------------------------------------

    required_columns = [
        "ControlActionVaccineVCode",
        "کد واحد اپیدمیولوژیک",
        "شماره واکسیناسیون",
        "تاریخ ثبت",
        "کد استان",
        "استان",
        "کد شهرستان",
        "شهرستان",
        "نام واحد اپیدمیولوژیک",
        "کد واحد اپیدمیولوژیک",
        "نوع واحد اپیدمیولوژیک",
        "X",
        "Y",
        "نام مرکز واکسیناسیون",
        "کد مرکز واکسیناسیون",
        "نوع واکسن",
        "نوع دام",
        "تاریخ واکسیناسیون",
        "واکسیناسیون راپل",
        "نوع عملیات",
        "نام تجاری واکسن",
        "کارخانه سازنده",
        "نوع واکسن.1",
        "سری ساخت",
        "تعداد کل دام",
        "تعداد دام",
        "تعداد دام واجد شرایط واکسیناسیون",
        "تعداد دام واکسینه شده",
        "گروه سنی",
        "تعداد دز هر ویال",
        "تعداد بسته",
        "نام بیماری",
        "شوک پس از تزریق؟",
        "تعداد شوک پس از تزریق",
        "تعداد تلفات / کشتار شده",
        "سقط جنین؟",
        "تعداد سقط جنین",
        "ازدیاد حساسیت؟",
        "تعداد ازدیاد حساسیت",
        "عوارض موضعی؟",
        "تعداد عوارض موضعی",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required Excel columns: "
            + ", ".join(missing_columns)
        )

    # --------------------------------------------------------
    # Process rows
    # --------------------------------------------------------

    for index, row in df.iterrows():

        row_number = index + 2

        try:

            # =================================================
            # 1. ControlActionVaccineVCode
            # =================================================

            code = clean_string(
                row["ControlActionVaccineVCode"]
            )

            if code is None:
                skipped += 1

                print(
                    f"SKIPPED row {row_number}: "
                    "ControlActionVaccineVCode is empty"
                )

                continue

            # =================================================
            # 2. Duplicate check
            # =================================================

            exists = (
                db.query(GISVaccinationPerformance)
                .filter(
                    GISVaccinationPerformance.control_action_vaccine_vcode
                    == code
                )
                .first()
            )

            if exists:
                skipped += 1

                print(
                    f"SKIPPED row {row_number}: "
                    f"Record already exists: {code}"
                )

                continue

            # =================================================
            # 3. Epidemiology Unit
            # =================================================

            unit_code = clean_string(
                row["کد واحد اپیدمیولوژیک"]
            )

            if unit_code is None:
                failed += 1

                print(
                    f"FAILED row {row_number}: "
                    "Epidemiology unit code is empty"
                )

                continue

            unit = (
                db.query(GISEpidemiologyUnit)
                .filter(
                    GISEpidemiologyUnit.unit_code
                    == unit_code
                )
                .first()
            )

            if unit is None:
                failed += 1

                print(
                    f"FAILED row {row_number}: "
                    f"Unit Not Found: {unit_code}"
                )

                continue

            # =================================================
            # 4. Build model
            # =================================================

            item = GISVaccinationPerformance(

                # ------------------------------------------------
                # Keys
                # ------------------------------------------------

                control_action_vaccine_vcode=code,

                vaccination_no=clean_string(
                    row["شماره واکسیناسیون"]
                ),

                epidemiology_unit_id=unit.id,

                # ------------------------------------------------
                # Province / County
                # ------------------------------------------------

                province_code=clean_string(
                    row["کد استان"]
                ),

                province_name=clean_string(
                    row["استان"]
                ),

                county_code=clean_string(
                    row["کد شهرستان"]
                ),

                county_name=clean_string(
                    row["شهرستان"]
                ),

                # ------------------------------------------------
                # Epidemiology Unit
                # ------------------------------------------------

                epidemiology_unit_name=clean_string(
                    row["نام واحد اپیدمیولوژیک"]
                ),

                epidemiology_unit_code=clean_string(
                    row["کد واحد اپیدمیولوژیک"]
                ),

                epidemiology_unit_type=clean_string(
                    row["نوع واحد اپیدمیولوژیک"]
                ),

                latitude=clean_float(
                    row["X"]
                ),

                longitude=clean_float(
                    row["Y"]
                ),

                # ------------------------------------------------
                # Vaccination Center
                # ------------------------------------------------

                vaccination_center_name=clean_string(
                    row["نام مرکز واکسیناسیون"]
                ),

                vaccination_center_code=clean_string(
                    row["کد مرکز واکسیناسیون"]
                ),

                # ------------------------------------------------
                # Vaccine
                # ------------------------------------------------

                vaccine_type=clean_string(
                    row["نوع واکسن"]
                ),

                vaccine_brand=clean_string(
                    row["نام تجاری واکسن"]
                ),

                manufacturer=clean_string(
                    row["کارخانه سازنده"]
                ),

                vaccine_category=clean_string(
                    row["نوع واکسن.1"]
                ),

                batch_number=clean_string(
                    row["سری ساخت"]
                ),

                # ------------------------------------------------
                # Animal
                # ------------------------------------------------

                animal_type=clean_string(
                    row["نوع دام"]
                ),

                # ------------------------------------------------
                # Dates
                # ------------------------------------------------

                vaccination_date=convert_date(
                    row["تاریخ واکسیناسیون"]
                ),

                registration_date=convert_date(
                    row["تاریخ ثبت"]
                ),

                # ------------------------------------------------
                # Vaccination
                # ------------------------------------------------

                rappel_vaccination=clean_string(
                    row["واکسیناسیون راپل"]
                ),

                operation_type=clean_string(
                    row["نوع عملیات"]
                ),

                # ------------------------------------------------
                # Counts
                # ------------------------------------------------

                total_animals=clean_int(
                    row["تعداد کل دام"]
                ),

                animal_count=clean_int(
                    row["تعداد دام"]
                ),

                eligible_animals=clean_int(
                    row["تعداد دام واجد شرایط واکسیناسیون"]
                ),

                vaccinated_animals=clean_int(
                    row["تعداد دام واکسینه شده"]
                ),

                age_group=clean_string(
                    row["گروه سنی"]
                ),

                dose_per_vial=clean_float(
                    row["تعداد دز هر ویال"]
                ),

                package_count=clean_int(
                    row["تعداد بسته"]
                ),

                disease_name=clean_string(
                    row["نام بیماری"]
                ),

                # ------------------------------------------------
                # Shock
                # ------------------------------------------------

                shock_after_injection=clean_bool(
                    row["شوک پس از تزریق؟"]
                ),

                shock_count=clean_int(
                    row["تعداد شوک پس از تزریق"]
                ),

                # ------------------------------------------------
                # Death
                # ------------------------------------------------

                death_count=clean_int(
                    row["تعداد تلفات / کشتار شده"]
                ),

                # ------------------------------------------------
                # Abortion
                # ------------------------------------------------

                abortion=clean_bool(
                    row["سقط جنین؟"]
                ),

                abortion_count=clean_int(
                    row["تعداد سقط جنین"]
                ),

                # ------------------------------------------------
                # Hypersensitivity
                # ------------------------------------------------

                hypersensitivity=clean_bool(
                    row["ازدیاد حساسیت؟"]
                ),

                hypersensitivity_count=clean_int(
                    row["تعداد ازدیاد حساسیت"]
                ),

                # ------------------------------------------------
                # Local Complication
                # ------------------------------------------------

                local_complication=clean_bool(
                    row["عوارض موضعی؟"]
                ),

                local_complication_count=clean_int(
                    row["تعداد عوارض موضعی"]
                ),
            )

            # =================================================
            # 5. Insert
            # =================================================

            db.add(item)

            db.flush()

            inserted += 1

            print(
                f"INSERTED row {row_number}: {code}"
            )

        except Exception:

            db.rollback()

            failed += 1

            print("=" * 80)
            print(
                f"FAILED row {row_number}"
            )
            print(
                f"ControlActionVaccineVCode: {row.get('ControlActionVaccineVCode')}"
            )
            print("=" * 80)

            traceback.print_exc()

            continue

    # ========================================================
    # Final commit
    # ========================================================

    try:

        db.commit()

    except Exception:

        db.rollback()

        print("=" * 80)
        print("FINAL COMMIT FAILED")
        print("=" * 80)

        traceback.print_exc()

        raise

    # ========================================================
    # Result
    # ========================================================

    print("=" * 80)
    print(
        f"Inserted={inserted}  "
        f"Skipped={skipped}  "
        f"Failed={failed}"
    )
    print("=" * 80)

    return {
        "inserted": inserted,
        "skipped": skipped,
        "failed": failed,
    }

