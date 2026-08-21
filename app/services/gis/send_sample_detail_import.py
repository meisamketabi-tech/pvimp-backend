print("=" * 80)
print("SEND SAMPLE DETAIL IMPORT MODULE LOADED")
print("=" * 80)

import pandas as pd

from sqlalchemy.orm import Session

from app.db.models.gis_send_sample_detail import GISSendSampleDetail
from app.db.models.gis_epidemiology_unit import GISEpidemiologyUnit
from app.db.models.gis_disease import GISDisease


def clean_string(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    if value == "'":
        return None

    return value


def convert_date(value):
    if pd.isna(value):
        return None

    try:
        return pd.to_datetime(value).date()
    except Exception:
        return None


def get_or_create_disease(db: Session, disease_name: str):

    disease_name = clean_string(disease_name)

    if disease_name is None:
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


def import_send_sample_detail(
    db: Session,
    file_path: str,
):

    print("=" * 80)
    print("SEND SAMPLE DETAIL IMPORT START")
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

            detail_vcode = clean_string(row["SendSampleDetailVCode"])

            exists = (
                db.query(GISSendSampleDetail)
                .filter(GISSendSampleDetail.send_sample_detail_vcode == detail_vcode)
                .first()
            )

            if exists:
                skipped += 1
                continue

            unit_code = clean_string(row["کد واحد اپیدمیولوژیک"])

            unit = (
                db.query(GISEpidemiologyUnit)
                .filter(GISEpidemiologyUnit.unit_code == unit_code)
                .first()
            )

            if unit is None:

                print(f"ROW {index}: Unit Not Found -> {unit_code}")

                failed += 1
                continue

            disease = get_or_create_disease(
                db,
                row["نوع بیماری / مراقبت"],
            )

            item = GISSendSampleDetail(
                send_sample_detail_vcode=detail_vcode,
                send_sample_vcode=clean_string(row["SendSampleVCode"]),
                province_code=clean_string(row["کد استان"]),
                province_name=clean_string(row["استان"]),
                county_code=clean_string(row["کد شهرستان"]),
                county_name=clean_string(row["شهرستان"]),
                epidemiology_unit_id=unit.id,
                epidemiology_unit_code=unit.unit_code,
                epidemiology_unit_name=unit.unit_name,
                epidemiology_unit_type=clean_string(row["نوع واحد اپیدمیولوژیک"]),
                disease_id=disease.id if disease else None,
                disease_name=clean_string(row["نوع بیماری / مراقبت"]),
                animal_type=clean_string(row["نوع دام"]),
                sample_type=clean_string(row["نوع نمونه"]),
                sample_count=row["تعداد نمونه"],
                sampling_date=convert_date(row["تاریخ نمونه برداری"]),
                result_status=clean_string(row["وضعیت جواب"]),
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
