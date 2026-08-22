from sqlalchemy import text
from sqlalchemy.orm import Session

VIEW_NAME = "gis_vaccination_kpi"


CREATE_VIEW_SQL = r'''
CREATE OR REPLACE VIEW gis_vaccination_kpi AS
SELECT
    p.id,
    p.control_action_vaccine_vcode,
    p.vaccination_no,
    p.epidemiology_unit_id,
    p.province_code,
    p.province_name,
    p.county_code,
    p.county_name,
    p.epidemiology_unit_name,
    p.epidemiology_unit_code,
    p.epidemiology_unit_type,
    p.latitude,
    p.longitude,
    p.vaccination_center_name,
    p.vaccination_center_code,
    p.vaccine_type AS raw_vaccine_type,
    CASE
        WHEN regexp_replace(trim(p.vaccine_type), '\s+', ' ', 'g') LIKE 'لمپی اسکین%'
          OR regexp_replace(trim(p.vaccine_type), '\s+', ' ', 'g') LIKE 'لمپی‌اسکین%'
          OR regexp_replace(trim(p.vaccine_type), '\s+', ' ', 'g') LIKE 'لامپی اسکین%'
            THEN 'لمپی‌اسکین'
        WHEN trim(p.vaccine_type) = 'آبله' THEN 'آبله'
        WHEN trim(p.vaccine_type) = 'بروسلوز دام سبک' THEN 'بروسلوز دام سبک'
        WHEN trim(p.vaccine_type) = 'بروسلوز گاو و گوساله' THEN 'بروسلوز گاو و گوساله'
        WHEN trim(p.vaccine_type) = 'تب برفکی' THEN 'تب برفکی'
        WHEN trim(p.vaccine_type) = 'تب برفکی هگزا' THEN 'تب برفکی هگزا'
        WHEN trim(p.vaccine_type) = 'چهارگانه کلستریدیایی' THEN 'چهارگانه کلستریدیایی'
        WHEN trim(p.vaccine_type) = 'شاربن' THEN 'شاربن'
        WHEN trim(p.vaccine_type) = 'طاعون نشخوارکنندگان کوچک' THEN 'طاعون نشخوارکنندگان کوچک'
        WHEN trim(p.vaccine_type) IN ('P.P.R','PPR') THEN 'طاعون نشخوارکنندگان کوچک'
        WHEN trim(p.vaccine_type) = 'کزاز' THEN 'کزاز'
        WHEN trim(p.vaccine_type) = 'هاری' THEN 'هاری'
        WHEN trim(p.vaccine_type) = 'هپاتیت نکروزان' THEN 'هپاتیت نکروزان'
        WHEN trim(p.vaccine_type) IN ('اگالاکسی','آگالاکسی') THEN 'اگالاکسی'
        WHEN trim(p.vaccine_type) = 'اکتیما' THEN 'اکتیما'
        WHEN trim(p.vaccine_type) = 'واکسن های سگ' THEN 'واکسن های سگ'
        WHEN trim(p.vaccine_type) = 'واکسن های گربه' THEN 'واکسن های گربه'
        WHEN trim(p.vaccine_type) = 'پلی والان(چندگانه) - (غیرفعال)' THEN 'پلی‌والان چندگانه غیرفعال'
        WHEN trim(p.vaccine_type) LIKE 'پلی والان(چندگانه) - (غیرفعال) آنتریت%' THEN 'پلی‌والان چندگانه سگ'
        WHEN trim(p.vaccine_type) LIKE 'دوگانه آنتریت%' THEN 'دوگانه آنتریت پارواویروسی سگ و دیستمپر'
        WHEN trim(p.vaccine_type) LIKE 'دوگانه کورینه%' THEN 'دوگانه کورینه باکتریوم + سالمونلوز'
        WHEN trim(p.vaccine_type) LIKE 'سه گانه آنتروتوکسمی%' OR trim(p.vaccine_type) LIKE 'سه‌گانه آنتروتوکسمی%' THEN 'سه‌گانه آنتروتوکسمی + شاربن علامتی + کزاز'
        WHEN trim(p.vaccine_type) = 'تست سل' THEN 'تست سل'
        WHEN trim(p.vaccine_type) = 'سموم' THEN 'سموم'
        ELSE trim(p.vaccine_type)
    END AS vaccine_type,
    p.vaccine_brand,
    p.manufacturer,
    p.vaccine_category,
    p.batch_number,
    p.animal_type AS raw_animal_type,
    CASE
        WHEN trim(p.animal_type) = 'گاو میش' THEN 'گاومیش'
        WHEN trim(p.animal_type) = 'گوسفند و بز' THEN 'گوسفند و بز'
        WHEN trim(p.animal_type) = 'بره و بزغاله' THEN 'بره و بزغاله'
        WHEN trim(p.animal_type) = 'گاو و گوساله' THEN 'گاو و گوساله'
        ELSE trim(p.animal_type)
    END AS animal_type,
    CASE
        WHEN trim(p.animal_type) IN ('گوسفند','بز','بره','بزغاله','گوسفند و بز','بره و بزغاله') THEN 'LIGHT_LIVESTOCK'
        WHEN trim(p.animal_type) IN ('گاو','گوساله','گاومیش','گاو میش','گاو و گوساله') THEN 'HEAVY_LIVESTOCK'
        WHEN trim(p.animal_type) IN ('اسب','الاغ','قاطر') THEN 'EQUINE'
        WHEN trim(p.animal_type) IN ('سگ','سگ صاحبدار','سگ بدون صاحب') THEN 'DOG'
        WHEN trim(p.animal_type) = 'گربه' THEN 'CAT'
        WHEN trim(p.animal_type) = 'شتر' THEN 'CAMEL'
        ELSE 'UNKNOWN'
    END AS animal_group,
    CASE
        WHEN trim(p.animal_type) IN ('گوسفند و بز','بره و بزغاله','گاو و گوساله') THEN TRUE
        ELSE FALSE
    END AS is_composite_animal,
    p.age_group,
    p.vaccination_date,
    p.registration_date,
    p.rappel_vaccination,
    p.operation_type,
    p.total_animals,
    p.animal_count,
    p.eligible_animals,
    p.vaccinated_animals,
    p.dose_per_vial,
    p.package_count,
    CASE
        WHEN trim(p.vaccine_type) IN ('آبله') THEN 'آبله'
        WHEN trim(p.vaccine_type) LIKE 'بروسلوز%' THEN 'بروسلوز'
        WHEN trim(p.vaccine_type) LIKE 'تب برفکی%' THEN 'تب برفکی'
        WHEN trim(p.vaccine_type) LIKE 'لمپی%' OR trim(p.vaccine_type) LIKE 'لامپی%' THEN 'لمپی‌اسکین'
        WHEN trim(p.vaccine_type) = 'شاربن' THEN 'شاربن'
        WHEN trim(p.vaccine_type) IN ('طاعون نشخوارکنندگان کوچک','P.P.R','PPR') THEN 'PPR'
        WHEN trim(p.vaccine_type) = 'تست سل' THEN 'سل'
        WHEN trim(p.vaccine_type) = 'هاری' THEN 'هاری'
        WHEN trim(p.vaccine_type) IN ('واکسن های سگ','واکسن های گربه') THEN NULL
        WHEN trim(p.vaccine_type) = 'کزاز' THEN 'کزاز'
        WHEN trim(p.vaccine_type) IN ('اگالاکسی','آگالاکسی') THEN 'اگالاکسی'
        WHEN trim(p.vaccine_type) = 'اکتیما' THEN 'اکتیما'
        WHEN trim(p.vaccine_type) = 'هپاتیت نکروزان' THEN 'هپاتیت نکروزان'
        ELSE trim(p.disease_name)
    END AS disease_name,
    CASE
        WHEN trim(p.vaccine_type) = 'تست سل' THEN 'SURVEILLANCE'
        WHEN trim(p.vaccine_type) = 'سموم' THEN 'OTHER'
        WHEN trim(p.vaccine_type) IS NULL OR trim(p.vaccine_type) = '' THEN 'OTHER'
        ELSE 'VACCINATION'
    END AS activity_type,
    p.shock_after_injection,
    p.shock_count,
    p.death_count,
    p.abortion,
    p.abortion_count,
    p.hypersensitivity,
    p.hypersensitivity_count,
    p.local_complication,
    p.local_complication_count
FROM gis_vaccination_performances p;
'''


def ensure_vaccination_kpi_view(db: Session) -> None:
    db.execute(text(CREATE_VIEW_SQL))
    db.commit()
