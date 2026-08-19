print("=" * 80)
print("LAB RESULT IMPORT MODULE LOADED")
print("=" * 80)

import pandas as pd

from sqlalchemy.orm import Session

from app.db.models.gis_laboratory_result import GISLaboratoryResult
from app.db.models.gis_epidemiology_unit import GISEpidemiologyUnit
from app.db.models.gis_disease import GISDisease


def clean_string(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value in ("", "'", "''", "nan", "None"):
        return None

    return value


def clean_float(value):
    if pd.isna(value):
        return None

    try:
        value = str(value).strip()

        if value in ("", "'", "''", "nan", "None"):
            return None

        return float(value)

    except Exception:
        return None


def get_or_create_disease(
    db: Session,
    disease_name: str,
):

    if disease_name is None:
        return None

    disease_name = str(disease_name).strip()

    if disease_name == "":
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


def convert_date(value):

    if pd.isna(value):
        return None

    try:
        return pd.to_datetime(value).date()
    except Exception:
        return None


def import_laboratory_result(
    db: Session,
    file_path: str,
):

    print("=" * 80)
    print("LABORATORY RESULT IMPORT START")
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

            send_sample_vcode = str(row["SendSampleVCode"]).strip()

            exists = (
                db.query(GISLaboratoryResult)
                .filter(GISLaboratoryResult.send_sample_vcode == send_sample_vcode)
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

                print(f"ROW {index}: Unit Not Found -> {unit_code}")

                failed += 1
                continue

            disease = get_or_create_disease(
                db,
                row["نام بیماری"],
            )

            item = GISLaboratoryResult(
                send_sample_vcode=send_sample_vcode,
                answer_no=row["شماره جواب"],
                answer_date=convert_date(row["تاریخ جواب"]),
                sampling_date=convert_date(row["تاریخ نمونه برداری"]),
                register_date=convert_date(row["تاریخ ثبت"]),
                epidemiology_unit_id=unit.id,
                epidemiology_unit_code=unit.unit_code,
                epidemiology_unit_name=unit.unit_name,
                epidemiology_unit_type=row["نوع واحد اپیدمیولوژیک"],
                province_name=row["استان"],
                county_name=row["شهرستان"],
                laboratory_code=row["کد آزمایشگاه"],
                sample_type=row["نوع نمونه"],
                sample_count=row["تعداد نمونه"],
                laboratory_name=row["نام آزمایشگاه"],
                laboratory_type=row["نوع آزمایشگاه"],
                laboratory_owner=row["مالک آزمایشگاه"],
                animal_type=row["نوع دام"],
                disease_id=(disease.id if disease else None),
                disease_name=row["نام بیماری"],
                result_status=row["وضعیت جواب"],
                latitude=clean_float(row["X"]),
                longitude=clean_float(row["Y"]),
                isolate_name_1=clean_string(row["نام عامل جداشونده اول"]),
                isolate_name_2=clean_string(row["نام عامل جداشونده دوم"]),
                serotype_a=clean_string(row["A"]),
                serotype_o=clean_string(row["O"]),
                serotype_asia1=clean_string(row["Asia1"]),
                unacceptable_cases=clean_string(row["موارد غیر قابل قبول"]),
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
