import pandas as pd

from sqlalchemy.orm import Session

from app.db.models.gis_spraying import GISSpraying
from app.db.models.gis_epidemiology_unit import (
    GISEpidemiologyUnit,
)


def import_spraying(
    db: Session,
    file_path: str,
):

    print("=" * 80)
    print("SPRAYING IMPORT START")
    print("FILE:", file_path)

    df = pd.read_excel(file_path)

    print("ROWS:", len(df))
    print("COLUMNS:")
    print(df.columns.tolist())
    print("=" * 80)

    inserted = 0
    skipped = 0
    failed = 0

    for index, row in df.iterrows():

        try:

            spraying_vcode = str(row["SprayingVCode"]).strip()

            exists = (
                db.query(GISSpraying)
                .filter(GISSpraying.spraying_vcode == spraying_vcode)
                .first()
            )

            if exists:
                skipped += 1
                continue

            unit_code = str(row["کد واحد اپیدمیولوژیک"]).strip()

            unit = (
                db.query(GISEpidemiologyUnit)
                .filter(GISEpidemiologyUnit.unit_code == unit_code)
                .first()
            )

            if unit is None:

                print(f"ROW {index}: Epidemiology Unit Not Found -> {unit_code}")

                failed += 1
                continue

            spraying_date = None

            if pd.notna(row["تاریخ سمپاشی"]):
                spraying_date = pd.to_datetime(row["تاریخ سمپاشی"]).date()

            item = GISSpraying(
                spraying_vcode=spraying_vcode,
                province_name=row["استان"],
                county_name=row["شهرستان"],
                epidemiology_unit_id=unit.id,
                epidemiology_unit_code=unit.unit_code,
                epidemiology_unit_name=unit.unit_name,
                epidemiology_unit_type=row["نوع واحد اپیدمیولوژیک"],
                spraying_date=spraying_date,
                plan_type=row["نوع طرح"],
                operation_type=row["نوع عمیات سمپاشی"],
                poison_type=row["نوع سم"],
                sprayed_area=row["مساحت سمپاشی شده"],
                sprayed_animal_count=row["تعداد دام سمپاشی شده"],
                animal_type=row["نوع دام"],
                total_animals=row["تعداد دام موجود"],
            )

            db.add(item)

            inserted += 1

        except Exception as e:

            print(f"ROW {index} ERROR:")
            print(e)

            failed += 1

    db.commit()

    print("=" * 80)
    print(f"FINAL => Inserted: {inserted}  Skipped: {skipped}  Failed: {failed}")
    print("=" * 80)

    return {
        "inserted": inserted,
        "skipped": skipped,
        "failed": failed,
    }
