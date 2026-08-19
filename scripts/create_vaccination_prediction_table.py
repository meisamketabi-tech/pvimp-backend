# -*- coding: utf-8 -*-

from sqlalchemy import text
from app.db.session import SessionLocal


TABLE_NAME = "gis_vaccination_predictions"


CREATE_SQL = """
CREATE TABLE IF NOT EXISTS gis_vaccination_predictions (
    id BIGSERIAL PRIMARY KEY,

    county_name VARCHAR(100) NOT NULL,

    prediction_year INTEGER NOT NULL DEFAULT 1405,

    abeleh_bazi_imported INTEGER,
    abeleh_bazi INTEGER,
    abeleh_gosfandi INTEGER,

    brucellosis_lamb_rev1 INTEGER,
    brucellosis_ewe_rev1 INTEGER,

    brucellosis_heavy_fd_iriba INTEGER,
    brucellosis_heavy_rd_iriba INTEGER,

    sharbun INTEGER,
    ppr INTEGER,
    rabies INTEGER,
    lumpy_skin INTEGER,
    foot_and_mouth INTEGER,

    source VARCHAR(20) NOT NULL DEFAULT 'EXCEL',

    report_date VARCHAR(20),

    notes TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_gis_vaccination_prediction_county_year
        UNIQUE (county_name, prediction_year)
);
"""


INSERT_SQL = """
INSERT INTO gis_vaccination_predictions (
    county_name,
    prediction_year,

    abeleh_bazi_imported,
    abeleh_bazi,
    abeleh_gosfandi,

    brucellosis_lamb_rev1,
    brucellosis_ewe_rev1,

    brucellosis_heavy_fd_iriba,
    brucellosis_heavy_rd_iriba,

    source,
    report_date
)
VALUES (
    :county_name,
    1405,

    :abeleh_bazi_imported,
    :abeleh_bazi,
    :abeleh_gosfandi,

    :brucellosis_lamb_rev1,
    :brucellosis_ewe_rev1,

    :brucellosis_heavy_fd_iriba,
    :brucellosis_heavy_rd_iriba,

    'EXCEL',
    '1405/05/01'
)
ON CONFLICT (county_name, prediction_year)
DO UPDATE SET
    abeleh_bazi_imported = EXCLUDED.abeleh_bazi_imported,
    abeleh_bazi = EXCLUDED.abeleh_bazi,
    abeleh_gosfandi = EXCLUDED.abeleh_gosfandi,
    brucellosis_lamb_rev1 = EXCLUDED.brucellosis_lamb_rev1,
    brucellosis_ewe_rev1 = EXCLUDED.brucellosis_ewe_rev1,
    brucellosis_heavy_fd_iriba = EXCLUDED.brucellosis_heavy_fd_iriba,
    brucellosis_heavy_rd_iriba = EXCLUDED.brucellosis_heavy_rd_iriba,
    source = EXCLUDED.source,
    report_date = EXCLUDED.report_date,
    updated_at = CURRENT_TIMESTAMP;
"""


DATA = [
    {
        "county_name": "ابهر",
        "abeleh_bazi_imported": 0,
        "abeleh_bazi": 10920,
        "abeleh_gosfandi": 106176,
        "brucellosis_lamb_rev1": 26347,
        "brucellosis_ewe_rev1": 65867,
        "brucellosis_heavy_fd_iriba": 2565,
        "brucellosis_heavy_rd_iriba": 5230,
    },
    {
        "county_name": "ایجرود",
        "abeleh_bazi_imported": 0,
        "abeleh_bazi": 1480,
        "abeleh_gosfandi": 70400,
        "brucellosis_lamb_rev1": 17173,
        "brucellosis_ewe_rev1": 43433,
        "brucellosis_heavy_fd_iriba": 1413,
        "brucellosis_heavy_rd_iriba": 2827,
    },
    {
        "county_name": "خدابنده",
        "abeleh_bazi_imported": 50,
        "abeleh_bazi": 6646,
        "abeleh_gosfandi": 196384,
        "brucellosis_lamb_rev1": 43882,
        "brucellosis_ewe_rev1": None,
        "brucellosis_heavy_fd_iriba": 2816,
        "brucellosis_heavy_rd_iriba": 5472,
    },
    {
        "county_name": "خرمدره",
        "abeleh_bazi_imported": 0,
        "abeleh_bazi": 969,
        "abeleh_gosfandi": 17380,
        "brucellosis_lamb_rev1": 4128,
        "brucellosis_ewe_rev1": 10321,
        "brucellosis_heavy_fd_iriba": 3250,
        "brucellosis_heavy_rd_iriba": 4269,
    },
    {
        "county_name": "زنجان",
        "abeleh_bazi_imported": 0,
        "abeleh_bazi": 40373,
        "abeleh_gosfandi": 235419,
        "brucellosis_lamb_rev1": 64353,
        "brucellosis_ewe_rev1": None,
        "brucellosis_heavy_fd_iriba": 4948,
        "brucellosis_heavy_rd_iriba": 9996,
    },
    {
        "county_name": "سلطانیه",
        "abeleh_bazi_imported": 100,
        "abeleh_bazi": 4492,
        "abeleh_gosfandi": 66870,
        "brucellosis_lamb_rev1": 15476,
        "brucellosis_ewe_rev1": 37960,
        "brucellosis_heavy_fd_iriba": 1242,
        "brucellosis_heavy_rd_iriba": 2481,
    },
    {
        "county_name": "طارم",
        "abeleh_bazi_imported": 0,
        "abeleh_bazi": 14354,
        "abeleh_gosfandi": 55226,
        "brucellosis_lamb_rev1": 14305,
        "brucellosis_ewe_rev1": 35763,
        "brucellosis_heavy_fd_iriba": 1312,
        "brucellosis_heavy_rd_iriba": 2624,
    },
    {
        "county_name": "ماهنشان",
        "abeleh_bazi_imported": 0,
        "abeleh_bazi": 19968,
        "abeleh_gosfandi": 130808,
        "brucellosis_lamb_rev1": 32210,
        "brucellosis_ewe_rev1": 82187,
        "brucellosis_heavy_fd_iriba": 1298,
        "brucellosis_heavy_rd_iriba": 2644,
    },
]


def main():
    db = SessionLocal()

    try:
        db.execute(text(CREATE_SQL))

        for row in DATA:
            db.execute(text(INSERT_SQL), row)

        db.commit()

        result = db.execute(
            text(
                """
                SELECT
                    county_name,
                    prediction_year,
                    abeleh_bazi_imported,
                    abeleh_bazi,
                    abeleh_gosfandi,
                    brucellosis_lamb_rev1,
                    brucellosis_ewe_rev1,
                    brucellosis_heavy_fd_iriba,
                    brucellosis_heavy_rd_iriba
                FROM gis_vaccination_predictions
                WHERE prediction_year = 1405
                ORDER BY id;
                """
            )
        ).fetchall()

        print("")
        print("=" * 100)
        print("gis_vaccination_predictions")
        print("=" * 100)

        for row in result:
            print(row)

        print("")
        print("TABLE CREATED/UPDATED SUCCESSFULLY")
        print("TABLE:", TABLE_NAME)
        print("ROWS:", len(result))

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()