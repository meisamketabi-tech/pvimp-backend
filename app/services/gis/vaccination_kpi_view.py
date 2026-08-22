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
        WHEN regexp_replace(trim(p.vaccine_type), '\s+', ' ', 'g') IN ('لمپی‌اسکین','لمپی اسکین','لامپی اسکین')
             OR regexp_replace(trim(p.vaccine_type), '\s+', ' ', 'g') LIKE 'لمپی اسکین%'
             OR regexp_replace(trim(p.vaccine_type), '\s+', ' ', 'g') LIKE 'لمپی‌اسکین%'
             OR regexp_replace(trim(p.vaccine_type), '\s+', ' ', 'g') LIKE 'لامپی اسکین%'
            THEN 'لمپی‌اسکین'
        WHEN trim(p.vaccine_type) = 'آبله' THEN 'آبله'
        WHEN trim(p.vaccine_type) = 'آبله‌گوسفندی' THEN 'آبله گوسفندی'
        WHEN trim(p.vaccine_type) = 'بروسلوز دام سبک' THEN 'بروسلوز دام سبک'
        WHEN trim(p.vaccine_type) = 'بروسلوز گاو و گوساله' THEN 'بروسلوز گاو و گوساله'
        WHEN trim(p.vaccine_type) = 'تب برفکی' THEN 'تب برفکی'
        WHEN trim(p.vaccine_type) = 'تب برفکی هگزازا' THEN 'تب برفکی هگزازا'
        WHEN trim(p.vaccine_type) = 'چهارگانه کلستریدیایی' THEN 'چهارگانه کلستریدیایی'
        WHEN trim(p.vaccine_type) LIKE 'دوگانه آنتریت%' THEN 'دوگانه آنتریت'
        WHEN trim(p.vaccine_type) LIKE 'دوگانه کورینه%' THEN 'دوگانه کورینه'
        WHEN trim(p.vaccine_type) LIKE 'سه‌گانه آنتروتوکسمی%' OR trim(p.vaccine_type) LIKE 'سه گانه آنتروتوکسمی%' THEN 'سه‌گانه آنتروتوکسمی + شاربن + کزاز'
        WHEN trim(p.vaccine_type) = 'شاربن' THEN 'شاربن'
        WHEN trim(p.vaccine_type) IN ('طاعون نشخوارکنندگان کوچک','P.P.R','PPR') THEN 'طاعون نشخوارکنندگان کوچک'
        WHEN trim(p.vaccine_type) = 'کزاز' THEN 'کزاز'
        WHEN trim(p.vaccine_type) IN ('هاری','واکسن هاری سگ','واکسن هاری گربه') THEN 'هاری'
        WHEN trim(p.vaccine_type) = 'هپاتیت نکرورزان' THEN 'هپاتیت نکرورزان'
        WHEN trim(p.vaccine_type) LIKE 'آکتیم%' THEN 'آکتیمـا'
        ELSE trim(p.vaccine_type)
    END AS vaccine_type,
    p.vaccine_brand,
    p.manufacturer,
    p.vaccine_category,
    p.batch_number,
    p.animal_type AS raw_animal_type,
    CASE
        WHEN trim(p.animal_type) = 'گاو میش' THEN 'گاومیش'
        WHEN trim(p.animal_type) IN ('گوسفند','بز','بره','بزغاله','گاو','گوساله','گاومیش','اسب','الاغ','قاطر','سگ','سگ صاحبدار','سگ بدون صاحب','گربه','شتر') THEN trim(p.animal_type)
        WHEN trim(p.animal_type) = 'گوسفند و بز' THEN 'گوسفند و بز'
        WHEN trim(p.animal_type) = 'بره و بزغاله' THEN 'بره و بزغاله'
        ELSE trim(p.animal_type)
    END AS animal_type,
    CASE
        WHEN trim(p.animal_type) IN ('گوسفند','بز','بره','بزغاله','گوسفند و بز','بره و بزغاله') THEN 'LIGHT_LIVESTOCK'
        WHEN trim(p.animal_type) IN ('گاو','گوساله','گاومیش','گاو میش') THEN 'HEAVY_LIVESTOCK'
        WHEN trim(p.animal_type) IN ('اسب','الاغ','قاطر') THEN 'EQUINE'
        WHEN trim(p.animal_type) IN ('سگ','سگ صاحبدار','سگ بدون صاحب') THEN 'DOG'
        WHEN trim(p.animal_type) = 'گربه' THEN 'CAT'
        WHEN trim(p.animal_type) = 'شتر' THEN 'CAMEL'
        ELSE 'UNKNOWN'
    END AS animal_group,
    CASE
        WHEN trim(p.animal_type) IN ('گوسفند و بز','بره و بزغاله') THEN TRUE
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
        WHEN trim(p.vaccine_type) IN ('آبله','آبله‌گوسفندی') THEN 'آبله'
        WHEN trim(p.vaccine_type) LIKE 'بروسلوز%' THEN 'بروسلوز'
        WHEN trim(p.vaccine_type) LIKE 'تب برفکی%' THEN 'تب برفکی'
        WHEN trim(p.vaccine_type) LIKE 'لمپی%' OR trim(p.vaccine_type) LIKE 'لامپی%' THEN 'لمپی‌اسکین'
        WHEN trim(p.vaccine_type) = 'شاربن' THEN 'شاربن'
        WHEN trim(p.vaccine_type) IN ('طاعون نشخوارکنندگان کوچک','P.P.R','PPR') THEN 'PPR'
        WHEN trim(p.vaccine_type) = 'تست سل' THEN 'سل'
        WHEN trim(p.vaccine_type) IN ('هاری','واکسن هاری سگ','واکسن هاری گربه') THEN 'هاری'
        WHEN trim(p.vaccine_type) = 'کزاز' THEN 'کزاز'
        ELSE trim(p.disease_name)
    END AS disease_name,
    CASE
        WHEN trim(p.vaccine_type) = 'تست سل' THEN 'SURVEILLANCE'
        WHEN trim(p.vaccine_type) = 'سموم' THEN 'OTHER'
        WHEN trim(p.vaccine_type) IS NULL OR trim(p.vaccine_type) = '' THEN 'OTHER'
        WHEN trim(p.vaccine_type) IN ('آبله','آبله‌گوسفندی','بروسلوز دام سبک','بروسلوز گاو و گوساله','تب برفکی','تب برفکی هگزازا','چهارگانه کلستریدیایی','شاربن','طاعون نشخوارکنندگان کوچک','P.P.R','PPR','کزاز','هاری','واکسن هاری سگ','واکسن هاری گربه','هپاتیت نکرورزان') THEN 'VACCINATION'
        WHEN trim(p.vaccine_type) LIKE 'لمپی%' OR trim(p.vaccine_type) LIKE 'لامپی%' THEN 'VACCINATION'
        WHEN trim(p.vaccine_type) LIKE 'دوگانه آنتریت%' OR trim(p.vaccine_type) LIKE 'دوگانه کورینه%' OR trim(p.vaccine_type) LIKE 'سه‌گانه آنتروتوکسمی%' OR trim(p.vaccine_type) LIKE 'سه گانه آنتروتوکسمی%' OR trim(p.vaccine_type) LIKE 'آکتیم%' THEN 'VACCINATION'
        ELSE 'OTHER'
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
