from __future__ import annotations

import os
from collections import defaultdict
from sqlalchemy import create_engine, text


def db_url() -> str:
    for key in ("DATABASE_URL", "SQLALCHEMY_DATABASE_URI", "POSTGRES_URL"):
        value = os.getenv(key)
        if value:
            return value
    try:
        from app.core.config import settings
        for key in ("DATABASE_URL", "SQLALCHEMY_DATABASE_URI", "POSTGRES_URL"):
            value = getattr(settings, key, None)
            if value:
                return value
        value = getattr(settings, "database_url", None)
        if value:
            return value
    except Exception:
        pass
    raise RuntimeError("Database URL was not found in environment or app.core.config.settings")


def rows(db, sql, params=None):
    return db.execute(text(sql), params or {}).mappings().all()


def main() -> None:
    engine = create_engine(db_url())
    with engine.connect() as db:
        print("=== DATABASE ===")
        print("connected: OK")

        print("\n=== RAW VACCINE TYPES ===")
        q = """
        SELECT COALESCE(vaccine_type,'<NULL>') AS vaccine_type,
               COUNT(*) AS records,
               COALESCE(SUM(vaccinated_animals),0) AS vaccinated_animals
        FROM gis_vaccination_performances
        GROUP BY vaccine_type
        ORDER BY records DESC, vaccine_type
        """
        raw = rows(db, q)
        for r in raw:
            print(f"{r['vaccine_type']} | records={r['records']} | vaccinated={r['vaccinated_animals']}")

        print("\n=== CLASSIFICATION FROM VIEW ===")
        q = """
        SELECT COALESCE(vaccine_type,'<NULL>') AS vaccine_type,
               activity_type,
               COUNT(*) AS records,
               COALESCE(SUM(vaccinated_animals),0) AS vaccinated_animals
        FROM gis_vaccination_kpi
        GROUP BY vaccine_type, activity_type
        ORDER BY activity_type, vaccine_type
        """
        for r in rows(db, q):
            print(f"{r['vaccine_type']} | {r['activity_type']} | records={r['records']} | vaccinated={r['vaccinated_animals']}")

        print("\n=== ANIMAL TYPE MAPPING ===")
        q = """
        SELECT COALESCE(raw_animal_type,'<NULL>') AS raw_animal_type,
               COALESCE(animal_type,'<NULL>') AS standard_animal_type,
               animal_group,
               is_composite_animal,
               COUNT(*) AS records,
               COALESCE(SUM(vaccinated_animals),0) AS vaccinated_animals
        FROM gis_vaccination_kpi
        GROUP BY raw_animal_type, animal_type, animal_group, is_composite_animal
        ORDER BY animal_group, raw_animal_type
        """
        for r in rows(db, q):
            print(f"{r['raw_animal_type']} -> {r['standard_animal_type']} | {r['animal_group']} | composite={r['is_composite_animal']} | records={r['records']} | vaccinated={r['vaccinated_animals']}")

        print("\n=== UNKNOWN ANIMALS ===")
        q = """
        SELECT raw_animal_type, COUNT(*) AS records,
               COALESCE(SUM(vaccinated_animals),0) AS vaccinated_animals
        FROM gis_vaccination_kpi
        WHERE animal_group='UNKNOWN'
        GROUP BY raw_animal_type
        ORDER BY records DESC
        """
        unknown = rows(db, q)
        if not unknown:
            print("NONE")
        else:
            for r in unknown:
                print(f"{r['raw_animal_type']} | records={r['records']} | vaccinated={r['vaccinated_animals']}")

        print("\n=== NON-VACCINATION CLASSIFICATION ===")
        q = """
        SELECT activity_type, COUNT(*) AS records,
               COALESCE(SUM(vaccinated_animals),0) AS vaccinated_animals
        FROM gis_vaccination_kpi
        WHERE activity_type <> 'VACCINATION'
        GROUP BY activity_type
        ORDER BY activity_type
        """
        for r in rows(db, q):
            print(f"{r['activity_type']} | records={r['records']} | vaccinated={r['vaccinated_animals']}")

        print("\n=== RAW VS KPI TOTALS ===")
        r = rows(db, """
            SELECT
              (SELECT COUNT(*) FROM gis_vaccination_performances) AS raw_records,
              (SELECT COALESCE(SUM(vaccinated_animals),0) FROM gis_vaccination_performances) AS raw_vaccinated,
              (SELECT COUNT(*) FROM gis_vaccination_kpi) AS view_records,
              (SELECT COALESCE(SUM(vaccinated_animals),0) FROM gis_vaccination_kpi) AS view_vaccinated
        """)[0]
        print(f"raw_records={r['raw_records']} | view_records={r['view_records']}")
        print(f"raw_vaccinated={r['raw_vaccinated']} | view_vaccinated={r['view_vaccinated']}")
        print("record_count_match:", r['raw_records'] == r['view_records'])
        print("vaccinated_sum_match:", r['raw_vaccinated'] == r['view_vaccinated'])

        print("\n=== COMPOSITE ANIMAL ROWS ===")
        q = """
        SELECT raw_animal_type, COUNT(*) AS records,
               COALESCE(SUM(vaccinated_animals),0) AS vaccinated_animals
        FROM gis_vaccination_kpi
        WHERE is_composite_animal IS TRUE
        GROUP BY raw_animal_type
        ORDER BY raw_animal_type
        """
        composite = rows(db, q)
        if not composite:
            print("NONE")
        else:
            for r in composite:
                print(f"{r['raw_animal_type']} | records={r['records']} | vaccinated={r['vaccinated_animals']}")

        print("\n=== DONE: READ ONLY / NO DATA MODIFIED ===")


if __name__ == "__main__":
    main()
