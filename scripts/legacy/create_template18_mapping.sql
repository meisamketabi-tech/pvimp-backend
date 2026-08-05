INSERT INTO gis_import_fields
(template_id, excel_column, database_column)
VALUES

(18,'SendSampleVCode','sample_send_code'),
(18,'استان','province'),
(18,'شهرستان','county'),
(18,'نام واحد اپیدمیولوژیک','unit_name'),
(18,'کد واحد اپیدمیولوژیک','unit_code'),
(18,'نوع واحد اپیدمیولوژیک','unit_type'),
(18,'نام بیماری','disease_type'),
(18,'نوع دام','animal_type'),
(18,'نوع نمونه','sample_type'),
(18,'تعداد نمونه','sample_count'),
(18,'تاریخ نمونه برداری','sampling_date'),
(18,'وضعیت جواب','result_status');

COMMIT;