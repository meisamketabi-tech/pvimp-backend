from __future__ import annotations

from datetime import date
from typing import Any

import pandas as pd
from sqlalchemy.orm import Session

from app.db.models.gis_slaughter_disposal import GISSlaughterDisposal
from app.db.models.gis_epidemiology_unit import GISEpidemiologyUnit
from app.db.models.gis_disease import GISDisease


def is_empty(value: Any) -> bool:
    """Return True for None, NaN/NaT and empty strings."""
    if value is None:
        return True

    try:
        if pd.isna(value):
            return True
    except Exception:
        pass

    if isinstance(value, str) and not value.strip():
        return True

    return False


def clean_text(value: Any) -> str | None:
    """Normalize Excel text values without converting NaN to 'nan'."""
    if is_empty(value):
        return None

    text = str(value).replace("\u200f", "").replace("\u200e", "")
    text = text.strip()

    return text or None


def clean_code(value: Any) -> str | None:
    """
    Normalize codes coming from Excel.

    Examples:
        11010187.0 -> '11010187'
        191111175609.0 -> '191111175609'
    """
    if is_empty(value):
        return None

    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))

    text = str(value).strip()

    # Remove Excel-style trailing .0 from numeric codes.
    if text.endswith(".0"):
        numeric_part = text[:-2]
        if numeric_part.isdigit():
            return numeric_part

    return text or None


def clean_int(value: Any) -> int | None:
    """Convert numeric Excel values safely to integer."""
    if is_empty(value):
        return None

    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def clean_float(value: Any) -> float | None:
    """Convert numeric Excel values safely to float."""
    if is_empty(value):
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def clean_date(value: Any) -> date | None:
    """Convert Excel date values safely."""
    if is_empty(value):
        return None

    if isinstance(value, date):
        return value

    try:
        return pd.to_datetime(value).date()
    except (TypeError, ValueError):
        return None


def get_or_create_disease(
    db: Session,
    disease_name: Any,
) -> GISDisease | None:
    """Find or create disease by normalized name."""
    name = clean_text(disease_name)

    if not name:
        return None

    disease = db.query(GISDisease).filter(GISDisease.disease_name == name).first()

    if disease:
        return disease

    disease = GISDisease(
        disease_name=name,
    )

    db.add(disease)
    db.flush()

    return disease


def import_slaughter_disposal(
    db: Session,
    file_path: str,
) -> dict[str, int]:
    """
    Import slaughter/disposal Excel data.

    Each row is processed inside a nested transaction/savepoint so a
    single bad row does not rollback successfully processed rows.
    """

    print("=" * 80)
    print("SLAUGHTER IMPORT START")
    print("FILE:", file_path)

    df = pd.read_excel(file_path)

    print("ROWS:", len(df))
    print("COLUMNS:")
    print(df.columns.tolist())
    print("=" * 80)

    inserted = 0
    skipped = 0
    failed = 0

    # Keep a lightweight cache for units.
    unit_cache: dict[str, GISEpidemiologyUnit | None] = {}

    # Keep a cache for diseases.
    disease_cache: dict[str, GISDisease | None] = {}

    try:
        for index, row in df.iterrows():
            excel_row = index + 2

            try:
                # ---------------------------------------------------------
                # 1) Detail/control codes
                # ---------------------------------------------------------
                detail_vcode = clean_code(row.get("ControlActionEmhaDetailVCode"))

                control_vcode = clean_code(row.get("ControlActionEmhaVCode"))

                if not detail_vcode:
                    print(f"ROW {excel_row}: " "ControlActionEmhaDetailVCode is empty")
                    failed += 1
                    continue

                # ---------------------------------------------------------
                # 2) Duplicate check
                # ---------------------------------------------------------
                exists = (
                    db.query(GISSlaughterDisposal)
                    .filter(
                        GISSlaughterDisposal.control_action_emha_detail_vcode
                        == detail_vcode
                    )
                    .first()
                )

                if exists:
                    skipped += 1
                    continue

                # ---------------------------------------------------------
                # 3) Epidemiology unit
                # ---------------------------------------------------------
                unit_code = clean_code(row.get("کد واحد اپیدمیولوژیک"))

                if not unit_code:
                    print(f"ROW {excel_row}: " "کد واحد اپیدمیولوژیک خالی است")
                    failed += 1
                    continue

                if unit_code in unit_cache:
                    unit = unit_cache[unit_code]
                else:
                    unit = (
                        db.query(GISEpidemiologyUnit)
                        .filter(GISEpidemiologyUnit.unit_code == unit_code)
                        .first()
                    )
                    unit_cache[unit_code] = unit

                if unit is None:
                    print(f"ROW {excel_row}: " f"Unit Not Found -> {unit_code}")
                    failed += 1
                    continue

                # ---------------------------------------------------------
                # 4) Disease
                # ---------------------------------------------------------
                disease_name = clean_text(row.get("نوع بیماری / مراقبت"))

                if disease_name in disease_cache:
                    disease = disease_cache[disease_name]
                else:
                    disease = get_or_create_disease(
                        db,
                        disease_name,
                    )
                    disease_cache[disease_name] = disease

                # ---------------------------------------------------------
                # 5) Prepare values
                # ---------------------------------------------------------
                action_date = clean_date(row.get("تاریخ کشتار/معدوم سازی"))

                province_code = clean_code(row.get("کد استان"))

                province_name = clean_text(row.get("استان"))

                county_code = clean_code(row.get("کد شهرستان"))

                county_name = clean_text(row.get("شهرستان"))

                epidemiology_unit_name = clean_text(unit.unit_name)

                old_unit_code = clean_code(row.get("کد واحد قدیم"))

                epidemiology_unit_type = clean_text(row.get("نوع واحد اپیدمیولوژیک"))

                animal_type = clean_text(row.get("نوع دام"))

                total_animals = clean_int(row.get("تعداد دام موجود"))

                positive_count = clean_int(row.get("تعداد مثبت"))

                slaughtered_count = clean_int(row.get("تعداد دام کشتار شده"))

                destroyed_count = clean_int(row.get("تعداد دام معدوم شده"))

                dead_count = clean_int(row.get("تعداد تلفات"))

                estimated_compensation = clean_float(row.get("مبلغ غرامت پیش بینی شده"))

                window_code = clean_code(row.get("کد پنجره"))

                operation_license_type = clean_text(row.get("نوع پروانه بهره برداری"))

                # ---------------------------------------------------------
                # 6) Savepoint per row
                # ---------------------------------------------------------
                with db.begin_nested():

                    item = GISSlaughterDisposal(
                        control_action_emha_detail_vcode=detail_vcode,
                        control_action_emha_vcode=control_vcode,
                        province_code=province_code,
                        province_name=province_name,
                        county_code=county_code,
                        county_name=county_name,
                        epidemiology_unit_id=unit.id,
                        epidemiology_unit_code=unit.unit_code,
                        epidemiology_unit_name=epidemiology_unit_name,
                        old_unit_code=old_unit_code,
                        epidemiology_unit_type=epidemiology_unit_type,
                        animal_type=animal_type,
                        action_date=action_date,
                        total_animals=total_animals,
                        positive_count=positive_count,
                        slaughtered_count=slaughtered_count,
                        destroyed_count=destroyed_count,
                        dead_count=dead_count,
                        estimated_compensation=(estimated_compensation),
                        disease_id=(disease.id if disease else None),
                        disease_name=disease_name,
                        window_code=window_code,
                        operation_license_type=(operation_license_type),
                    )

                    db.add(item)

                    # Important:
                    # Flush only this row inside its savepoint.
                    db.flush()

                inserted += 1

            except Exception as row_error:
                failed += 1

                print("=" * 80)
                print("SLAUGHTER IMPORT ROW ERROR")
                print("EXCEL ROW:", excel_row)
                print("INDEX:", index)
                print(
                    "DETAIL VCODE:",
                    clean_code(row.get("ControlActionEmhaDetailVCode")),
                )
                print(
                    "CONTROL VCODE:",
                    clean_code(row.get("ControlActionEmhaVCode")),
                )
                print(
                    "EPIDEMIOLOGY UNIT CODE:",
                    clean_code(row.get("کد واحد اپیدمیولوژیک")),
                )
                print(
                    "OPERATION LICENSE TYPE:",
                    repr(row.get("نوع پروانه بهره برداری")),
                )
                print(
                    "WINDOW CODE:",
                    repr(row.get("کد پنجره")),
                )
                print(
                    "OLD UNIT CODE:",
                    repr(row.get("کد واحد قدیم")),
                )
                print(
                    "ERROR TYPE:",
                    type(row_error).__name__,
                )
                print("ERROR:", row_error)
                print("=" * 80)

                # Do NOT call db.rollback() here.
                # begin_nested() already rolls this row back.

        # Commit all successful rows.
        db.commit()

    except Exception:
        # Only rollback if there is a fatal error outside the
        # per-row savepoint handling.
        db.rollback()
        raise

    print("=" * 80)
    print(
        f"FINAL => Inserted: {inserted}  " f"Skipped: {skipped}  " f"Failed: {failed}"
    )
    print("=" * 80)

    return {
        "inserted": inserted,
        "skipped": skipped,
        "failed": failed,
    }
