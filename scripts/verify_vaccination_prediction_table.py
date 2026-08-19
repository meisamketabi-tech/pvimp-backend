# -*- coding: utf-8 -*-

from sqlalchemy import text
from app.db.session import SessionLocal


SQL = """
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
ORDER BY id;
"""


def main():
    db = SessionLocal()

    try:
        rows = db.execute(text(SQL)).fetchall()

        print("")
        print("=" * 120)
        print("gis_vaccination_predictions - VERIFY")
        print("=" * 120)

        for row in rows:
            print(row)

        print("")
        print("ROW COUNT:", len(rows))

        if len(rows) != 8:
            raise RuntimeError(
                f"Expected 8 rows, but found {len(rows)} rows."
            )

        print("VERIFICATION: PASS")

    finally:
        db.close()


if __name__ == "__main__":
    main()