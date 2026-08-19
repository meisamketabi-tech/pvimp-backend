-- ============================================================
-- PVIMP KPI TARGET / FORECAST SEED
-- ============================================================
--
-- IMPORTANT:
-- target_value values are intentionally 0.
-- Replace them with the official management targets.
--
-- animal_group:
--   LIGHT = دام سبک
--   HEAVY = دام سنگین
--   EQUID = تک سمی
--
-- target_period_months:
--   3  = سه ماهه
--   4  = چهار ماهه
--   5  = پنج ماهه
--   12 = سالانه
--
-- target_unit:
--   head = رأس
--   test = تست
--   sample = نمونه
--   operation = عملیات
--
-- ============================================================


-- ============================================================
-- نمونه ساختار:
-- ============================================================

-- INSERT INTO gis_kpi_targets (
--     category_code,
--     category_title,
--     indicator_code,
--     indicator_title,
--     disease_name,
--     vaccine_type,
--     county_code,
--     county_name,
--     animal_group,
--     target_year,
--     target_month,
--     target_period_months,
--     target_value,
--     target_unit,
--     notes,
--     is_active
-- )
-- VALUES (
--     'infectious',
--     'الف- عملکرد مبارزه با بیماری‌های واگیر',
--     'sharbon',
--     'شاربن',
--     'شاربن',
--     NULL,
--     NULL,
--     NULL,
--     'LIGHT',
--     1405,
--     NULL,
--     12,
--     0,
--     'head',
--     'هدف سالانه شاربن - دام سبک',
--     TRUE
-- );


-- ============================================================
-- شاخص‌های فعلی
-- ============================================================

INSERT INTO gis_kpi_targets (
    category_code,
    category_title,
    indicator_code,
    indicator_title,
    disease_name,
    animal_group,
    target_year,
    target_period_months,
    target_value,
    target_unit,
    is_active
)
VALUES

(
    'infectious',
    'الف- عملکرد مبارزه با بیماری‌های واگیر',
    'sharbon',
    'شاربن',
    'شاربن',
    'LIGHT',
    1405,
    12,
    0,
    'head',
    TRUE
),

(
    'infectious',
    'الف- عملکرد مبارزه با بیماری‌های واگیر',
    'sharbon',
    'شاربن',
    'شاربن',
    'HEAVY',
    1405,
    12,
    0,
    'head',
    TRUE
),

(
    'infectious',
    'الف- عملکرد مبارزه با بیماری‌های واگیر',
    'sharbon',
    'شاربن',
    'شاربن',
    'EQUID',
    1405,
    12,
    0,
    'head',
    TRUE
),

(
    'infectious',
    'الف- عملکرد مبارزه با بیماری‌های واگیر',
    'fmd',
    'تب برفکی',
    'تب برفکی',
    'LIGHT',
    1405,
    12,
    0,
    'head',
    TRUE
),

(
    'infectious',
    'الف- عملکرد مبارزه با بیماری‌های واگیر',
    'fmd',
    'تب برفکی',
    'تب برفکی',
    'HEAVY',
    1405,
    12,
    0,
    'head',
    TRUE
),

(
    'infectious',
    'الف- عملکرد مبارزه با بیماری‌های واگیر',
    'fmd',
    'تب برفکی',
    'تب برفکی',
    'EQUID',
    1405,
    12,
    0,
    'head',
    TRUE
),

(
    'infectious',
    'الف- عملکرد مبارزه با بیماری‌های واگیر',
    'sheep_pox',
    'آبله',
    'آبله',
    'LIGHT',
    1405,
    12,
    0,
    'head',
    TRUE
),

(
    'infectious',
    'الف- عملکرد مبارزه با بیماری‌های واگیر',
    'lumpy_skin',
    'لمپی اسکین',
    'لمپی اسکین',
    'HEAVY',
    1405,
    12,
    0,
    'head',
    TRUE
),

(
    'infectious',
    'الف- عملکرد مبارزه با بیماری‌های واگیر',
    'ppr',
    'P.P.R',
    'PPR',
    'LIGHT',
    1405,
    12,
    0,
    'head',
    TRUE
),

(
    'zoonotic',
    'ب- عملکرد مبارزه با بیماری‌های مشترک',
    'brucellosis',
    'بروسلوز',
    'بروسلوز',
    'LIGHT',
    1405,
    12,
    0,
    'head',
    TRUE
),

(
    'zoonotic',
    'ب- عملکرد مبارزه با بیماری‌های مشترک',
    'brucellosis',
    'بروسلوز',
    'بروسلوز',
    'HEAVY',
    1405,
    12,
    0,
    'head',
    TRUE
),

(
    'zoonotic',
    'ب- عملکرد مبارزه با بیماری‌های مشترک',
    'rabies',
    'هاری',
    'هاری',
    'LIGHT',
    1405,
    12,
    0,
    'head',
    TRUE
),

(
    'zoonotic',
    'ب- عملکرد مبارزه با بیماری‌های مشترک',
    'rabies',
    'هاری',
    'هاری',
    'HEAVY',
    1405,
    12,
    0,
    'head',
    TRUE
),

(
    'surveillance',
    'ج- عملکرد پایش و مراقبت بیماری‌های مشترک',
    'blood_sampling',
    'خونگیری',
    NULL,
    'LIGHT',
    1405,
    12,
    0,
    'test',
    TRUE
),

(
    'surveillance',
    'ج- عملکرد پایش و مراقبت بیماری‌های مشترک',
    'tuberculosis_test',
    'تست سل',
    'سل',
    'HEAVY',
    1405,
    12,
    0,
    'test',
    TRUE
),

(
    'surveillance',
    'ج- عملکرد پایش و مراقبت بیماری‌های مشترک',
    'glanders_test',
    'تست مشمشه',
    'مشمشه',
    'EQUID',
    1405,
    12,
    0,
    'test',
    TRUE
);