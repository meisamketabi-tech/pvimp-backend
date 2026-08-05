import math
import pandas as pd

from datetime import date
from convertdate import persian

from sqlalchemy.orm import Session

from app.db.models.gis_disease_occurrence import GISDiseaseOccurrence
from app.db.models.gis_epidemiology_unit import GISEpidemiologyUnit
from app.db.models.gis_disease import GISDisease


def clean_value(value):

    if value is None:
        return None

    if isinstance(value, float) and math.isnan(value):
        return None

    return value


def convert_jalali_date(value):

    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    try:
        parts = value.split("/")

        if len(parts) != 3:
            return None

        y = int(parts[0])
        m = int(parts[1])
        d = int(parts[2])

        gy, gm, gd = persian.to_gregorian(y, m, d)

        return date(gy, gm, gd)

    except Exception:
        return None


COLUMN_MAP = {
    "ObservationDetailVCode": "observation_detail_vcode",
    "کد واحد اپیدمیولوژیک": "unit_code",
    "نام واحد اپیدمیولوژیک": "unit_name",
    "نام بیماری": "disease_name",
    "نوع دام": "animal_type",
    "تاریخ شروع بیماری": "start_date",
    "تعداد دام در معرض خطر": "exposed_count",
    "تعداد دام": "animal_count",
    "تعداد دام کشتار شده": "slaughtered_count",
    "تعداد دام مبتلا": "infected_count",
    "تعداد دام تلف شده": "dead_count",
    "ReportDate": "report_date",
    "شماره گزارش بیماری": "report_number",
    "X": "longitude",
    "Y": "latitude",
    "عنوان کاربر": "user_name",
    "کد کاربر": "user_code",
    "کد پنجره": "window_code",
    "نوع پروانه بهره برداری": "operation_license_type",
    "وضعیت": "status",
    "ReportInfo": "description",
}


def get_or_create_disease(db, disease_name):

    if not disease_name:
        return None

    disease_name = str(disease_name).strip()

    disease = (
        db.query(GISDisease).filter(GISDisease.disease_name == disease_name).first()
    )

    if disease:
        return disease

    disease = GISDisease(disease_name=disease_name)

    db.add(disease)
    db.flush()

    print("NEW DISEASE CREATED:", disease_name)

    return disease


def import_disease_occurrences(db: Session, file_path: str):

    df = pd.read_excel(file_path)

    df.rename(columns=COLUMN_MAP, inplace=True)

    inserted = 0
    failed = 0

    for _, row in df.iterrows():

        try:

            row = row.apply(clean_value)

            existing = (
                db.query(GISDiseaseOccurrence)
                .filter(
                    GISDiseaseOccurrence.observation_detail_vcode
                    == str(row.get("observation_detail_vcode"))
                )
                .first()
            )

            if existing:
                print("SKIP DUPLICATE:", row.get("observation_detail_vcode"))
                continue

            unit = None

            if row.get("unit_code"):

                unit = (
                    db.query(GISEpidemiologyUnit)
                    .filter(GISEpidemiologyUnit.unit_code == str(row.get("unit_code")))
                    .first()
                )

            disease = get_or_create_disease(db, row.get("disease_name"))

            print("UNIT:", row.get("unit_code"), "FOUND:", bool(unit))

            print("DISEASE:", row.get("disease_name"), "FOUND:", bool(disease))

            occurrence = GISDiseaseOccurrence(
                observation_detail_vcode=str(row.get("observation_detail_vcode")),
                epidemiology_unit_id=(unit.id if unit else None),
                disease_id=(disease.id if disease else None),
                animal_type=row.get("animal_type"),
                start_date=convert_jalali_date(row.get("start_date")),
                report_date=convert_jalali_date(row.get("report_date")),
                report_number=(
                    str(row.get("report_number")) if row.get("report_number") else None
                ),
                exposed_count=row.get("exposed_count"),
                animal_count=row.get("animal_count"),
                infected_count=row.get("infected_count"),
                dead_count=row.get("dead_count"),
                slaughtered_count=row.get("slaughtered_count"),
                latitude=row.get("latitude"),
                longitude=row.get("longitude"),
                user_name=row.get("user_name"),
                user_code=str(row.get("user_code")) if row.get("user_code") else None,
                window_code=(
                    str(row.get("window_code")) if row.get("window_code") else None
                ),
                operation_license_type=row.get("operation_license_type"),
                status=row.get("status"),
                description=row.get("description"),
            )

            db.add(occurrence)

            inserted += 1

        except Exception as e:

            db.rollback()

            print("IMPORT ERROR:", e)

            failed += 1

    try:
        db.commit()

    except Exception as e:
        db.rollback()
        print("COMMIT ERROR:", e)
        raise

    return {"inserted": inserted, "failed": failed}
