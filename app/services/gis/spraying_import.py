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

    df = pd.read_excel(file_path)

    inserted = 0
    skipped = 0
    failed = 0

    for _, row in df.iterrows():

        try:

            spraying_no = str(
                row["SprayingVCode"]
            ).strip()

            exists = (
                db.query(GISSpraying)
                .filter(
                    GISSpraying.spraying_no
                    == spraying_no
                )
                .first()
            )

            if exists:

                skipped += 1

                continue

            unit_code = str(
                row["کد واحد اپیدمیولوژیک"]
            ).strip()

            unit = (
                db.query(GISEpidemiologyUnit)
                .filter(
                    GISEpidemiologyUnit.unit_code
                    == unit_code
                )
                .first()
            )

            if not unit:

                failed += 1

                continue

            item = GISSpraying(

                spraying_no=spraying_no,

                epidemiology_unit_id=unit.id,

                province_name=row["استان"],

                county_name=row["شهرستان"],

                spraying_date=pd.to_datetime(
                    row["تاریخ سمپاشی"]
                ).date()
                if pd.notna(
                    row["تاریخ سمپاشی"]
                )
                else None,

                project_type=row["نوع طرح"],

                spraying_operation_type=row[
                    "نوع عمیات سمپاشی"
                ],

                pesticide_type=row["نوع سم"],

                sprayed_area=row[
                    "مساحت سمپاشی شده"
                ],

                sprayed_animals=row[
                    "تعداد دام سمپاشی شده"
                ],

                current_animals=row[
                    "تعداد دام موجود"
                ],

                animal_type=row["نوع دام"],

            )

            db.add(item)

            inserted += 1

        except Exception:

            failed += 1

    db.commit()

    return {

        "inserted": inserted,

        "skipped": skipped,

        "failed": failed,

    }