from app.db.session import engine
from sqlalchemy import text


sql = """
ALTER TABLE gis_lab_results
ADD CONSTRAINT uq_gis_lab_results_sample_code
UNIQUE (sample_code);
"""


with engine.begin() as conn:
    conn.execute(text(sql))


print("unique sample_code added")