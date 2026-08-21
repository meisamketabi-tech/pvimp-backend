import psycopg2


conn = psycopg2.connect(
    host="localhost",
    database="pvimp_db",
    user="postgres",
    password="postgres123"
)

cur = conn.cursor()


fields = [

("ControlActionVaccineVCode","control_action_vaccine_code"),
("شماره واکسیناسیون","vaccination_number"),
("تاریخ ثبت","register_date"),
("کد استان","province_code"),
("استان","province"),
("نام مرکز واکسیناسیون","vaccination_center_name"),
("کد مرکز واکسیناسیون","vaccination_center_code"),
("نوع واکسن","vaccine_type"),
("نوع دام","animal_type"),
("تاریخ واکسیناسیون","vaccination_date"),
("نوع عملیات","operation_type"),
("نام تجاری واکسن","vaccine_brand"),
("کارخانه سازنده","manufacturer"),
("دسته واکسن","vaccine_category"),
("سری ساخت","batch_number"),
("تعداد کل دام","total_animals"),
("تعداد دام واکسینه شده","vaccinated_animals"),
("نام بیماری","disease_name"),
("شوک پس از تزریق؟","post_injection_shock"),
("تعداد شوک پس از تزریق","shock_count"),
("تعداد تلفات / کشتار شده","death_or_culling_count"),
("سقط جنین؟","abortion"),
("تعداد سقط جنین","abortion_count"),
("ازدیاد حساسیت؟","hypersensitivity"),
("تعداد ازدیاد حساسیت","hypersensitivity_count"),
("عوارض موضعی؟","local_reaction"),
("تعداد عوارض موضعی","local_reaction_count")

]


for i,(excel_col,db_col) in enumerate(fields):

    cur.execute(
        """
        INSERT INTO gis_import_fields
        (
        template_id,
        excel_column,
        database_column,
        data_type,
        is_required,
        order_index
        )
        VALUES
        (
        28,
        %s,
        %s,
        'text',
        false,
        %s
        )
        """,
        (
            excel_col,
            db_col,
            i+1
        )
    )


conn.commit()

cur.close()
conn.close()


print("province mapping created")