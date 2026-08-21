print("=" * 80)
print("SURVEILLANCE IMPORT MODULE LOADED")
print("=" * 80)

import traceback
from datetime import datetime

import pandas as pd
from sqlalchemy.orm import Session

from app.db.models.gis_enable_care import GISEnableCare
from app.db.models.gis_epidemiology_unit import GISEpidemiologyUnit


# ============================================================
# Helpers
# ============================================================

def convert_date(value):
    if pd.isna(value):
        return None

    try:
        if isinstance(value, datetime):
            return value.date()

        value = str(value).replace("/", "-")
        return pd.to_datetime(value).date()

    except Exception:
        return None


def clean_string(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value in ("", "'", "nan", "None"):
        return None

    if value.endswith(".0"):
        value = value[:-2]

    return value


def clean_int(value):
    if pd.isna(value):
        return None

    try:
        return int(float(value))
    except Exception:
        return None


# ============================================================
# Main Import
# ============================================================

def import_surveillance(
    db: Session,
    file_path: str,
):

    print("=" * 80)
    print("SURVEILLANCE IMPORT START")
    print(file_path)
    print("=" * 80)

    df = pd.read_excel(file_path)

    inserted = 0
    skipped = 0
    failed = 0

    for index, row in df.iterrows():

        try:

            detail_code = clean_string(
                row.get("EnableCareDetailVCode")
            )

            if not detail_code:
                skipped += 1
                continue

            exists = (
                db.query(GISEnableCare)
                .filter(
                    GISEnableCare.enable_care_detail_vcode
                    == detail_code
                )
                .first()
            )

            if exists:
                skipped += 1
                continue

            unit_code = clean_string(
                row.get("کد واحد اپیدمیولوژیک")
            )

            unit = (
                db.query(GISEpidemiologyUnit)
                .filter(
                    GISEpidemiologyUnit.unit_code
                    == unit_code
                )
                .first()
            )

            if not unit:

                print(
                    f"[ROW {index}] "
                    f"Unit Not Found : {unit_code}"
                )

                failed += 1
                continue

            item = GISEnableCare(

                enable_care_detail_vcode=detail_code,
                enable_care_vcode=clean_string(
                    row.get("EnableCareVCode")
                ),

                province_code=clean_string(
                    row.get("کد استان")
                ),
                province_name=clean_string(
                    row.get("استان")
                ),

                county_code=clean_string(
                    row.get("کد شهرستان")
                ),
                county_name=clean_string(
                    row.get("شهرستان")
                ),

                epidemiology_unit_id=unit.id,
                epidemiology_unit_code=unit.unit_code,
                epidemiology_unit_name=unit.unit_name,
                epidemiology_unit_type=clean_string(
                    row.get("نوع واحد اپیدمیولوژیک")
                ),

                care_type=clean_string(
                    row.get("نوع مراقبت")
                ),

                animal_type=clean_string(
                    row.get("نوع دام")
                ),

                care_date=convert_date(
                    row.get("تاریخ مراقبت")
                ),

                total_animals=clean_int(
                    row.get("تعداد کل دام")
                ),

                positive_count=clean_int(
                    row.get("تعداد مثبت")
                ),

                negative_count=clean_int(
                    row.get("تعداد منفی")
                ),

                suspicious_count=clean_int(
                    row.get("تعداد مشکوک")
                ),

                old_system_id=clean_string(
                    row.get("OldSystemId")
                ),

                age_group=clean_string(
                    row.get("گروه سنی")
                ),

                old_unit_code=clean_string(
                    row.get("کد واحد قدیم")
                ),

                window_code=clean_string(
                    row.get("کد پنجره")
                ),

                operation_license_type=clean_string(
                    row.get("نوع پروانه بهره برداری")
                ),
            )

            db.add(item)

            inserted += 1

            if inserted % 500 == 0:
                db.flush()

        except Exception:

            failed += 1

            print("=" * 80)
            print(f"ROW {index} ERROR")
            traceback.print_exc()
            print(row.to_dict())
            print("=" * 80)

            db.rollback()

    db.commit()

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
