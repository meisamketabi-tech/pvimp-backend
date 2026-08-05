import math
import pandas as pd

from sqlalchemy.orm import Session

from app.db.models.gis_epidemiology_unit import GISEpidemiologyUnit
from app.db.models.gis_province import GISProvince
from app.db.models.gis_county import GISCounty
from app.db.models.gis_epidemiology_unit_type import (
    GISEpidemiologyUnitType,
)


def clean_value(value):

    if value is None:
        return None

    if isinstance(value, float) and math.isnan(value):
        return None

    if isinstance(value, str):

        value = value.strip()

        if value == "":
            return None

    return value


def normalize_text(value):

    value = clean_value(value)

    if value is None:
        return None

    value = str(value)

    # اصلاح حروف عربی
    value = value.replace("ي", "ی")
    value = value.replace("ى", "ی")
    value = value.replace("ك", "ک")
    value = value.replace("ۀ", "ه")

    # حذف کاراکترهای مخفی RTL/LTR و فاصله‌های خاص
    invisible_chars = [
        "\u200c",  # ZWNJ
        "\u200d",  # ZWJ
        "\u200e",  # LTR mark
        "\u200f",  # RTL mark
        "\ufeff",  # BOM
    ]

    for ch in invisible_chars:
        value = value.replace(ch, "")

    # یکسان سازی فاصله
    value = " ".join(value.split())

    return value.strip()


def normalize_compare(value):

    value = normalize_text(value)

    if not value:
        return None

    chars = [
        "\u200c",
        "\u200e",
        "\u200f",
        "\ufeff",
    ]

    for c in chars:
        value = value.replace(c, "")

    value = value.replace(" ", "")
    value = value.replace("‌", "")

    return value


def to_int(value):

    value = clean_value(value)

    if value is None:
        return 0

    try:
        return int(float(value))

    except:
        return 0


def to_bool(value):

    value = normalize_text(value)

    return value in [
        True,
        1,
        "1",
        "True",
        "true",
        "بله",
        "بلی",
        "دارد",
        "دارم",
    ]


COLUMN_MAP = {
    "نام واحد اپیدمیولوژیک": "unit_name",
    "کد واحد اپیدمیولوژیک": "unit_code",
    "کد واحد قدیم": "old_code",
    "کد پنجره": "window_code",
    "کد واحد پدر": "parent_unit_code",
    "استان": "province_name",
    "شهرستان": "county_name",
    "نوع واحد اپیدمیولوژیک": "unit_type_name",
    "X": "longitude",
    "Y": "latitude",
    "نام کاربر": "user_name",
    "کد کاربر": "user_code",
    "تعداد گوسفند": "sheep_count",
    "تعداد گاو": "cattle_count",
    "تعداد بز": "goat_count",
    "تعداد اسب": "horse_count",
    "تعداد سگ": "dog_count",
    "تعداد شتر": "camel_count",
    "تعداد گاومیش": "buffalo_count",
    "کد پستی": "postal_code",
    "شماره پروانه بهداشتی": "sanitary_license_number",
    "شماره پروانه بهره برداری": "operation_license_number",
    "آدرس": "address",
    "نوع پروانه بهره برداری": "license_type",
    "HasSubUnit": "has_sub_unit",
    "وضعیت فعال بودن واحد": "is_active",
}


def get_province(db, name, cache):

    name = normalize_text(name)

    if not name:
        return None

    if name in cache:
        return cache[name]

    province = db.query(GISProvince).filter(GISProvince.province_name == name).first()

    if province:
        cache[name] = province.id
        return province.id

    print("WARNING Province missing:", name)

    return None


def get_county(db, name, province_id, cache):

    name = normalize_compare(name)

    if not name or not province_id:
        return None

    key = (province_id, name)

    if key in cache:
        return cache[key]

    counties = db.query(GISCounty).filter(GISCounty.province_id == province_id).all()

    for county in counties:

        db_name = normalize_compare(county.county_name)

        if db_name == name:

            cache[key] = county.id

            return county.id

    print("WARNING County missing:", name)

    return None

    county_id = get_county(db, row.get("county_name"), province_id, county_cache)


def get_or_create_unit_type(db, name, cache):

    name = normalize_text(name)

    if not name:
        return None

    if name in cache:
        return cache[name]

    obj = (
        db.query(GISEpidemiologyUnitType)
        .filter(GISEpidemiologyUnitType.title == name)
        .first()
    )

    if not obj:

        obj = GISEpidemiologyUnitType(
            title=name,
            code=None,
            description=None,
        )

        db.add(obj)

        db.flush()

    cache[name] = obj.id

    return obj.id


def import_epidemiology_units(
    db: Session,
    file_path: str,
):

    try:

        df = pd.read_excel(file_path)

        df.rename(columns=COLUMN_MAP, inplace=True)

        print("=" * 80)
        print("IMPORT FILE:", file_path)
        print("ROWS:", len(df))
        print("=" * 80)

        inserted = 0
        skipped = 0
        failed = 0

        existing_codes = {x[0] for x in db.query(GISEpidemiologyUnit.unit_code).all()}

        province_cache = {}
        county_cache = {}
        type_cache = {}
        parent_cache = {}

        for index, row in df.iterrows():

            try:

                row = row.apply(clean_value)

                unit_code = normalize_text(row.get("unit_code"))

                if not unit_code:

                    failed += 1
                    continue

                if unit_code in existing_codes:

                    skipped += 1
                    continue

                province_id = get_province(db, row.get("province_name"), province_cache)

                county_id = get_county(
                    db, row.get("county_name"), province_id, county_cache
                )

                unit_type_id = get_or_create_unit_type(
                    db, row.get("unit_type_name"), type_cache
                )

                parent_id = None

                parent_code = normalize_text(row.get("parent_unit_code"))

                if parent_code:

                    if parent_code in parent_cache:

                        parent_id = parent_cache[parent_code]

                    else:

                        parent = (
                            db.query(GISEpidemiologyUnit)
                            .filter(GISEpidemiologyUnit.unit_code == parent_code)
                            .first()
                        )

                        if parent:

                            parent_id = parent.id

                            parent_cache[parent_code] = parent.id

                unit = GISEpidemiologyUnit(
                    unit_name=normalize_text(row.get("unit_name")),
                    unit_code=unit_code,
                    old_code=normalize_text(row.get("old_code")),
                    window_code=normalize_text(row.get("window_code")),
                    province_id=province_id,
                    county_id=county_id,
                    unit_type_id=unit_type_id,
                    parent_unit_id=parent_id,
                    latitude=clean_value(row.get("latitude")),
                    longitude=clean_value(row.get("longitude")),
                    user_name=normalize_text(row.get("user_name")),
                    user_code=normalize_text(row.get("user_code")),
                    sheep_count=to_int(row.get("sheep_count")),
                    cattle_count=to_int(row.get("cattle_count")),
                    goat_count=to_int(row.get("goat_count")),
                    horse_count=to_int(row.get("horse_count")),
                    dog_count=to_int(row.get("dog_count")),
                    camel_count=to_int(row.get("camel_count")),
                    buffalo_count=to_int(row.get("buffalo_count")),
                    postal_code=normalize_text(row.get("postal_code")),
                    address=normalize_text(row.get("address")),
                    license_type=normalize_text(row.get("license_type")),
                    sanitary_license_number=normalize_text(
                        row.get("sanitary_license_number")
                    ),
                    operation_license_number=normalize_text(
                        row.get("operation_license_number")
                    ),
                    has_sub_unit=to_bool(row.get("has_sub_unit")),
                    is_active=to_bool(row.get("is_active")),
                )

                db.add(unit)

                db.flush()

                existing_codes.add(unit_code)

                inserted += 1

            except Exception as e:

                print("IMPORT ERROR ROW:", index, e)

                failed += 1

        db.commit()

        print("=" * 80)
        print("FINAL =>", "Inserted:", inserted, "Skipped:", skipped, "Failed:", failed)
        print("=" * 80)

        return {
            "inserted": inserted,
            "skipped": skipped,
            "failed": failed,
        }

    except Exception:

        db.rollback()

        raise
