# -*- coding: utf-8 -*-

from sqlalchemy import text
from app.db.session import SessionLocal


# ============================================================
# واکسن‌های موجود در UI / دامنه واکسیناسیون سیستم
# ============================================================

VACCINES = [
    "آبله",
    "اکتیما",
    "آگالاکسی",
    "بروسلوز دام سبک",
    "بروسلوز گاو و گوساله",
    "پلی والان(چندگانه) - (غیرفعال)",
    "پلی والان(چندگانه) - (غیرفعال) آنتریت پارواویروسی سگ , بیماری تنفسی عفونی سگ(تراکئوبرونشیت عفونی) , دیستمپر , لپتوسپیروز , هاری , هپاتیت عفونی سگ",
    "تب برفکی",
    "تب برفکی هگزات",
    "تست سل",
    "چهارگانه کلستریدیایی",
    "دوگانه آنتریت پارواویروسی سگ , دیستمپر",
    "دوگانه کورینه باکتریوم+سالمونلوز",
    "سموم",
    "سه گانه آنتروتوکسمی، شاربن علامتی، کزاز",
    "شاربن",
    "طاعون نشخوارکنندگان کوچک",
    "کزاز",
    "لامپی اسکین",
    "هاری",
    "هپاتیت نکروزان",
    "واکسن های سگ",
    "واکسن های گربه",
]


def main():
    db = SessionLocal()

    try:
        print("")
        print("=" * 120)
        print("GIS VACCINATION PREDICTION SCHEMA")
        print("=" * 120)

        # ----------------------------------------------------
        # 1. بررسی جداول مرجع موجود
        # ----------------------------------------------------

        required_tables = [
            "gis_counties",
            "gis_diseases",
        ]

        for table_name in required_tables:
            exists = db.execute(
                text("""
                    SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                      AND table_name = :table_name
                """),
                {"table_name": table_name},
            ).scalar()

            if not exists:
                raise RuntimeError(
                    f"Required reference table does not exist: {table_name}"
                )

        # ----------------------------------------------------
        # 2. نمایش شهرستان‌ها
        # ----------------------------------------------------

        counties = db.execute(
            text("""
                SELECT
                    id,
                    province_id,
                    county_code,
                    county_name
                FROM public.gis_counties
                ORDER BY id
            """)
        ).fetchall()

        print("")
        print("=" * 120)
        print("COUNTY REFERENCE")
        print("=" * 120)

        for row in counties:
            print(row)

        if len(counties) == 0:
            raise RuntimeError("gis_counties is empty.")

        # ----------------------------------------------------
        # 3. نمایش بیماری‌های موجود
        # ----------------------------------------------------

        diseases = db.execute(
            text("""
                SELECT
                    id,
                    disease_code,
                    disease_name,
                    disease_group,
                    is_notifiable
                FROM public.gis_diseases
                ORDER BY id
            """)
        ).fetchall()

        print("")
        print("=" * 120)
        print("DISEASE REFERENCE")
        print("=" * 120)

        for row in diseases:
            print(row)

        if len(diseases) == 0:
            raise RuntimeError("gis_diseases is empty.")

        # ----------------------------------------------------
        # 4. ایجاد جدول نام واکسن‌ها
        # ----------------------------------------------------

        db.execute(text("""
            CREATE TABLE IF NOT EXISTS public.gis_vaccines (
                id BIGSERIAL PRIMARY KEY,

                vaccine_name VARCHAR(500) NOT NULL,

                vaccine_code VARCHAR(100),

                vaccine_category VARCHAR(150),

                description TEXT,

                is_active BOOLEAN NOT NULL DEFAULT TRUE,

                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                CONSTRAINT uq_gis_vaccines_name
                    UNIQUE (vaccine_name)
            );
        """))

        # ----------------------------------------------------
        # 5. ثبت واکسن‌ها
        # ----------------------------------------------------

        insert_vaccine = text("""
            INSERT INTO public.gis_vaccines (
                vaccine_name,
                is_active
            )
            VALUES (
                :vaccine_name,
                TRUE
            )
            ON CONFLICT (vaccine_name)
            DO UPDATE SET
                is_active = TRUE,
                updated_at = CURRENT_TIMESTAMP;
        """)

        for vaccine_name in VACCINES:
            db.execute(
                insert_vaccine,
                {
                    "vaccine_name": vaccine_name,
                },
            )

        # ----------------------------------------------------
        # 6. جدول Prediction نرمال‌شده
        #
        # شهرستان ← واکسن ← بیماری
        #
        # disease_id nullable است چون بعضی واکسن‌ها ممکن است
        # مستقیماً به یک بیماری واحد وابسته نباشند.
        # ----------------------------------------------------

        db.execute(text("""
            CREATE TABLE IF NOT EXISTS public.gis_vaccination_predictions (
                id BIGSERIAL PRIMARY KEY,

                county_id INTEGER NOT NULL,

                vaccine_id BIGINT NOT NULL,

                disease_id INTEGER,

                prediction_year INTEGER NOT NULL,

                prediction_value NUMERIC(14,2) NOT NULL,

                prediction_unit VARCHAR(50) NOT NULL DEFAULT 'DOSE',

                source VARCHAR(50) NOT NULL DEFAULT 'EXCEL',

                source_file VARCHAR(255),

                source_sheet VARCHAR(255),

                notes TEXT,

                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                CONSTRAINT fk_prediction_county
                    FOREIGN KEY (county_id)
                    REFERENCES public.gis_counties(id)
                    ON DELETE RESTRICT,

                CONSTRAINT fk_prediction_vaccine
                    FOREIGN KEY (vaccine_id)
                    REFERENCES public.gis_vaccines(id)
                    ON DELETE RESTRICT,

                CONSTRAINT fk_prediction_disease
                    FOREIGN KEY (disease_id)
                    REFERENCES public.gis_diseases(id)
                    ON DELETE RESTRICT,

                CONSTRAINT uq_vaccination_prediction
                    UNIQUE (
                        county_id,
                        vaccine_id,
                        disease_id,
                        prediction_year
                    )
            );
        """))

        # ----------------------------------------------------
        # 7. Indexها
        # ----------------------------------------------------

        db.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_vaccination_predictions_county
            ON public.gis_vaccination_predictions(county_id);
        """))

        db.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_vaccination_predictions_vaccine
            ON public.gis_vaccination_predictions(vaccine_id);
        """))

        db.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_vaccination_predictions_disease
            ON public.gis_vaccination_predictions(disease_id);
        """))

        db.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_vaccination_predictions_year
            ON public.gis_vaccination_predictions(prediction_year);
        """))

        # ----------------------------------------------------
        # 8. Commit
        # ----------------------------------------------------

        db.commit()

        # ----------------------------------------------------
        # 9. Verification - Vaccine table
        # ----------------------------------------------------

        vaccine_rows = db.execute(
            text("""
                SELECT
                    id,
                    vaccine_name,
                    vaccine_code,
                    vaccine_category,
                    is_active
                FROM public.gis_vaccines
                ORDER BY id
            """)
        ).fetchall()

        print("")
        print("=" * 120)
        print("VACCINE REFERENCE TABLE")
        print("=" * 120)

        for row in vaccine_rows:
            print(row)

        print("")
        print("VACCINE ROW COUNT:", len(vaccine_rows))

        # ----------------------------------------------------
        # 10. Verification - Prediction table structure
        # ----------------------------------------------------

        prediction_columns = db.execute(
            text("""
                SELECT
                    ordinal_position,
                    column_name,
                    data_type,
                    is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = 'gis_vaccination_predictions'
                ORDER BY ordinal_position
            """)
        ).fetchall()

        print("")
        print("=" * 120)
        print("PREDICTION TABLE STRUCTURE")
        print("=" * 120)

        for row in prediction_columns:
            print(row)

        # ----------------------------------------------------
        # 11. FK verification
        # ----------------------------------------------------

        fk_rows = db.execute(
            text("""
                SELECT
                    tc.constraint_name,
                    kcu.column_name,
                    ccu.table_name AS referenced_table,
                    ccu.column_name AS referenced_column
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                   AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                   AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY'
                  AND tc.table_schema = 'public'
                  AND tc.table_name = 'gis_vaccination_predictions'
                ORDER BY tc.constraint_name;
            """)
        ).fetchall()

        print("")
        print("=" * 120)
        print("PREDICTION FOREIGN KEYS")
        print("=" * 120)

        for row in fk_rows:
            print(row)

        # انتظار سه FK:
        # county_id  -> gis_counties.id
        # vaccine_id -> gis_vaccines.id
        # disease_id -> gis_diseases.id

        if len(fk_rows) != 3:
            raise RuntimeError(
                f"Expected 3 foreign keys, found {len(fk_rows)}"
            )

        # ----------------------------------------------------
        # 12. Prediction count
        # ----------------------------------------------------

        prediction_count = db.execute(
            text("""
                SELECT COUNT(*)
                FROM public.gis_vaccination_predictions
            """)
        ).scalar()

        print("")
        print("PREDICTION ROW COUNT:", prediction_count)

        # فعلاً باید صفر باشد؛ چون Excel هنوز Import نشده است.
        if prediction_count != 0:
            print(
                "WARNING: Prediction table already contains data."
            )

        # ----------------------------------------------------
        # 13. نهایی
        # ----------------------------------------------------

        print("")
        print("=" * 120)
        print("VERIFICATION")
        print("=" * 120)
        print("gis_counties       : PASS")
        print("gis_diseases       : PASS")
        print("gis_vaccines       : PASS")
        print("prediction schema  : PASS")
        print("foreign keys       : PASS")
        print("")
        print("DATABASE SCHEMA READY.")
        print("")
        print("IMPORTANT:")
        print(
            "Prediction values have NOT been imported."
        )
        print(
            "Excel will only be used later as the numeric prediction source."
        )
        print("")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()