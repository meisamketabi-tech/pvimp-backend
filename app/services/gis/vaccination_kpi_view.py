from sqlalchemy import text
from sqlalchemy.orm import Session

VIEW_NAME = "gis_vaccination_kpi"

CREATE_VIEW_SQL = r'''
CREATE OR REPLACE VIEW gis_vaccination_kpi AS
WITH base AS (
    SELECT
        p.*,
        p.animal_type AS raw_animal_type,
        regexp_replace(trim(coalesce(p.vaccine_type, '')), '\s+', ' ', 'g') AS vt,
        regexp_replace(trim(coalesce(p.animal_type, '')), '\s+', ' ', 'g') AS at
    FROM gis_vaccination_performances p
),
classified AS (
    SELECT
        b.*,

        /* =========================================================
           1) تشخیص بیماری
           ========================================================= */
        CASE
            WHEN vt ILIKE '%بروسلوز%'
              OR vt ILIKE '%REV-1%'
              OR vt ILIKE '%REV1%'
              OR vt ILIKE '%ریو وان%'
                THEN 'بروسلوز'

            WHEN vt ILIKE '%تب برفکی%'
                THEN 'تب برفکی'

            WHEN vt ILIKE '%لمپی%'
              OR vt ILIKE '%لامپی%'
                THEN 'لمپی‌اسکین'

            WHEN vt IN ('P.P.R', 'PPR')
              OR vt ILIKE '%طاعون نشخوارکنندگان کوچک%'
                THEN 'طاعون نشخوارکنندگان کوچک'

            WHEN vt = 'آبله'
                THEN 'آبله'

            WHEN vt = 'شاربن'
              OR vt ILIKE '%سیاه زخم%'
                THEN 'شاربن'

            WHEN vt = 'تست سل'
                THEN 'سل'

            WHEN vt = 'هاری'
                THEN 'هاری'

            WHEN vt IN ('اگالاکسی','آگالاکسی')
                THEN 'اگالاکسی'

            WHEN vt = 'اکتیما'
                THEN 'اکتیما'

            WHEN vt = 'کزاز'
                THEN 'کزاز'

            WHEN vt = 'هپاتیت نکروزان'
                THEN 'هپاتیت نکروزان'

            WHEN vt ILIKE '%کلستریدیایی%'
                THEN 'کلستریدیوز'

            ELSE trim(coalesce(b.disease_name, ''))
        END AS classified_disease,

        /* =========================================================
           2) تشخیص نوع دام
           اولویت با اطلاعات صریح واکسن/بیماری،
           سپس animal_type خام
           ========================================================= */
        CASE
            /* بروسلوز */
            WHEN (
                vt ILIKE '%بروسلوز گاو%'
                OR vt ILIKE '%بروسلوز گاوی%'
            )
                THEN 'گاو و گوساله'

            WHEN (
                vt ILIKE '%بروسلوز دام سبک%'
                OR vt ILIKE '%REV-1%'
                OR vt ILIKE '%REV1%'
                OR vt ILIKE '%ریو وان%'
            )
                THEN 'گوسفند و بز'

            /* واکسن‌های اختصاصی دام سنگین */
            WHEN vt ILIKE '%لمپی%'
              OR vt ILIKE '%لامپی%'
                THEN 'گاو و گوساله'

            WHEN vt ILIKE '%تب برفکی هگزا%'
                THEN CASE
                    WHEN at IN ('گاو','گوساله','گاو و گوساله')
                        THEN 'گاو و گوساله'
                    WHEN at IN ('گوسفند','بز','گوسفند و بز','بره','بزغاله','بره و بزغاله')
                        THEN 'گوسفند و بز'
                    ELSE at
                END

            /* PPR */
            WHEN vt IN ('P.P.R','PPR')
              OR vt ILIKE '%طاعون نشخوارکنندگان کوچک%'
                THEN 'گوسفند و بز'

            /* واکسن‌های عمومی */
            WHEN vt = 'آبله'
                THEN CASE
                    WHEN at IN ('گوسفند','بز','گوسفند و بز','بره','بزغاله','بره و بزغاله')
                        THEN 'گوسفند و بز'
                    WHEN at IN ('گاو','گوساله','گاو و گوساله')
                        THEN 'گاو و گوساله'
                    ELSE at
                END

            WHEN vt = 'شاربن'
                THEN CASE
                    WHEN at IN ('گاو','گوساله','گاو و گوساله','گاومیش','گاو میش')
                        THEN 'گاو و گوساله'
                    WHEN at IN ('گوسفند','بز','گوسفند و بز','بره','بزغاله','بره و بزغاله')
                        THEN 'گوسفند و بز'
                    ELSE at
                END

            /* هاری */
            WHEN vt = 'هاری'
                THEN CASE
                    WHEN at IN ('سگ','سگ صاحبدار','سگ بدون صاحب')
                        THEN 'سگ'
                    WHEN at = 'گربه'
                        THEN 'گربه'
                    ELSE at
                END

            /* در سایر موارد، animal_type منبع ثانویه است */
            WHEN at = 'گاو میش'
                THEN 'گاومیش'

            WHEN at IN ('گوسفند و بز','بره و بزغاله')
                THEN at

            WHEN at = 'گاو و گوساله'
                THEN 'گاو و گوساله'

            ELSE at
        END AS classified_animal_type

    FROM base b
),
normalized AS (
    SELECT
        c.*,

        /* =========================================================
           3) Map نهایی واکسن بر اساس بیماری + دام
           ========================================================= */
        CASE

            /* ---------------- بروسلوز ---------------- */
            WHEN classified_disease = 'بروسلوز'
             AND classified_animal_type IN ('گاو','گوساله','گاو و گوساله')
                THEN 'بروسلوز گاو و گوساله'

            WHEN classified_disease = 'بروسلوز'
             AND classified_animal_type IN (
                    'گوسفند','بز','گوسفند و بز',
                    'بره','بزغاله','بره و بزغاله'
                )
                THEN 'بروسلوز دام سبک'

            /* ---------------- PPR ---------------- */
            WHEN classified_disease = 'طاعون نشخوارکنندگان کوچک'
                THEN 'PPR'

            /* ---------------- لمپی ---------------- */
            WHEN classified_disease = 'لمپی‌اسکین'
                THEN 'لمپی‌اسکین'

            /* ---------------- تب برفکی ---------------- */
            WHEN classified_disease = 'تب برفکی'
             AND classified_animal_type IN ('گاو','گوساله','گاو و گوساله')
                THEN 'تب برفکی گاو و گوساله'

            WHEN classified_disease = 'تب برفکی'
             AND classified_animal_type IN (
                    'گوسفند','بز','گوسفند و بز',
                    'بره','بزغاله','بره و بزغاله'
                )
                THEN 'تب برفکی دام سبک'

            WHEN classified_disease = 'تب برفکی'
                THEN 'تب برفکی'

            /* ---------------- سایر واکسن‌ها ---------------- */
            WHEN classified_disease = 'آبله'
                THEN 'آبله'

            WHEN classified_disease = 'شاربن'
                THEN 'شاربن'

            WHEN classified_disease = 'هاری'
                THEN 'هاری'

            WHEN classified_disease = 'سل'
                THEN 'تست سل'

            WHEN classified_disease = 'اگالاکسی'
                THEN 'اگالاکسی'

            WHEN classified_disease = 'اکتیما'
                THEN 'اکتیما'

            WHEN classified_disease = 'کزاز'
                THEN 'کزاز'

            WHEN classified_disease = 'هپاتیت نکروزان'
                THEN 'هپاتیت نکروزان'

            ELSE trim(coalesce(vt, ''))
        END AS mapped_vaccine_type

    FROM classified c
)
SELECT
    id,
    control_action_vaccine_vcode,
    vaccination_no,
    epidemiology_unit_id,
    province_code,
    province_name,
    county_code,
    county_name,
    epidemiology_unit_name,
    epidemiology_unit_code,
    epidemiology_unit_type,
    latitude,
    longitude,
    vaccination_center_name,
    vaccination_center_code,

    vaccine_type AS raw_vaccine_type,
    classified_disease AS disease_name,
    classified_animal_type AS animal_type,
    mapped_vaccine_type AS vaccine_type,

    vaccine_brand,
    manufacturer,
    vaccine_category,
    batch_number,

    animal_type AS raw_animal_type,

    CASE
        WHEN classified_animal_type IN (
            'گوسفند','بز','بره','بزغاله',
            'گوسفند و بز','بره و بزغاله'
        )
            THEN 'LIGHT_LIVESTOCK'

        WHEN classified_animal_type IN (
            'گاو','گوساله','گاومیش',
            'گاو میش','گاو و گوساله'
        )
            THEN 'HEAVY_LIVESTOCK'

        WHEN classified_animal_type IN ('اسب','الاغ','قاطر')
            THEN 'EQUINE'

        WHEN classified_animal_type IN ('سگ','سگ صاحبدار','سگ بدون صاحب')
            THEN 'DOG'

        WHEN classified_animal_type = 'گربه'
            THEN 'CAT'

        WHEN classified_animal_type = 'شتر'
            THEN 'CAMEL'

        ELSE 'UNKNOWN'
    END AS animal_group,

    CASE
        WHEN classified_animal_type IN (
            'گوسفند و بز',
            'بره و بزغاله',
            'گاو و گوساله'
        )
            THEN TRUE
        ELSE FALSE
    END AS is_composite_animal,

    age_group,
    vaccination_date,
    registration_date,
    rappel_vaccination,
    operation_type,
    total_animals,
    animal_count,
    eligible_animals,
    vaccinated_animals,
    dose_per_vial,
    package_count,

    CASE
        WHEN classified_disease IS NOT NULL
         AND classified_disease <> ''
            THEN classified_disease
        ELSE NULL
    END AS disease,

    CASE
        WHEN mapped_vaccine_type = 'تست سل'
            THEN 'SURVEILLANCE'
        WHEN mapped_vaccine_type = 'سموم'
            THEN 'OTHER'
        WHEN mapped_vaccine_type IS NULL
          OR mapped_vaccine_type = ''
            THEN 'OTHER'
        ELSE 'VACCINATION'
    END AS activity_type,

    shock_after_injection,
    shock_count,
    death_count,
    abortion,
    abortion_count,
    hypersensitivity,
    hypersensitivity_count,
    local_complication,
    local_complication_count

FROM normalized;
'''


def ensure_vaccination_kpi_view(db: Session) -> None:
    db.execute(text(CREATE_VIEW_SQL))
    db.commit()

