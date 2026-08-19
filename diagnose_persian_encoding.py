# -*- coding: utf-8 -*-

import sys
from pathlib import Path

# ---------------------------------------------------------
# PostgreSQL connection
# ---------------------------------------------------------

try:
    import psycopg
except ImportError:
    try:
        import psycopg2 as psycopg
    except ImportError:
        print("ERROR: psycopg / psycopg2 is not installed.")
        print()
        print("Run:")
        print("  .\\.venv\\Scripts\\python.exe -m pip install psycopg[binary]")
        sys.exit(1)


DB_HOST = "127.0.0.1"
DB_PORT = 5432
DB_NAME = "pvimp_db"
DB_USER = "postgres"


GIS_TABLE_PREFIX = "gis_"


# ---------------------------------------------------------
# Mojibake detector
# ---------------------------------------------------------

BAD_MARKERS = (
    "Ø",
    "Ù",
    "Ú",
    "Û",
    "Ü",
    "Ý",
    "Þ",
    "Ã",
    "Â",
    "Ð",
    "Ñ",
    " ",
)


def looks_mojibake(value: str) -> bool:
    if not value:
        return False

    score = sum(value.count(marker) for marker in BAD_MARKERS)

    # Persian text contains a lot of Arabic/Persian Unicode chars.
    persian_chars = sum(
        1
        for ch in value
        if (
            "\u0600" <= ch <= "\u06ff"
            or "\u0750" <= ch <= "\u077f"
            or "\u08a0" <= ch <= "\u08ff"
            or "\ufb50" <= ch <= "\ufdff"
            or "\ufe70" <= ch <= "\ufeff"
        )
    )

    # Typical mojibake has markers and very few real Persian chars.
    return score >= 2 and persian_chars < 3


def try_repair(value: str):
    """
    Typical UTF-8 -> Latin-1 mojibake repair.

    Example:
        Ø§Ø¨Ù‡Ø±
    becomes:
        ابهر
    """

    candidates = []

    for encoding in ("latin1", "cp1252"):
        try:
            repaired = value.encode(encoding).decode("utf-8")

            if repaired != value:
                candidates.append(repaired)

        except (UnicodeEncodeError, UnicodeDecodeError):
            pass

    if not candidates:
        return None

    # Choose the candidate containing more Persian characters.
    def persian_count(s):
        return sum(
            1
            for ch in s
            if (
                "\u0600" <= ch <= "\u06ff"
                or "\u0750" <= ch <= "\u077f"
                or "\u08a0" <= ch <= "\u08ff"
                or "\ufb50" <= ch <= "\ufdff"
                or "\ufe70" <= ch <= "\ufeff"
            )
        )

    candidates.sort(key=persian_count, reverse=True)

    repaired = candidates[0]

    if persian_count(repaired) > persian_count(value):
        return repaired

    return None


# ---------------------------------------------------------
# PostgreSQL connection
# ---------------------------------------------------------

def connect():
    try:
        conn = psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
        )
    except TypeError:
        # psycopg2 compatibility
        conn = psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
        )

    return conn


# ---------------------------------------------------------
# Main diagnostic
# ---------------------------------------------------------

def main():

    print("=" * 70)
    print("PERSIAN ENCODING DIAGNOSTIC")
    print("=" * 70)
    print()

    print(f"Database : {DB_NAME}")
    print(f"Host     : {DB_HOST}")
    print(f"User     : {DB_USER}")
    print()

    conn = connect()

    try:
        cur = conn.cursor()

        # -------------------------------------------------
        # PostgreSQL encoding
        # -------------------------------------------------

        cur.execute("SHOW server_encoding")
        server_encoding = cur.fetchone()[0]

        cur.execute("SHOW client_encoding")
        client_encoding = cur.fetchone()[0]

        print("PostgreSQL encoding:")
        print("  server_encoding :", server_encoding)
        print("  client_encoding :", client_encoding)
        print()

        # -------------------------------------------------
        # GIS tables
        # -------------------------------------------------

        cur.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_type = 'BASE TABLE'
              AND table_name LIKE 'gis_%'
            ORDER BY table_name
            """
        )

        tables = [row[0] for row in cur.fetchall()]

        print(f"GIS tables found: {len(tables)}")
        print()

        total_suspicious = 0

        # -------------------------------------------------
        # Inspect every text/varchar column
        # -------------------------------------------------

        for table in tables:

            cur.execute(
                """
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = %s
                  AND data_type IN (
                      'text',
                      'character varying',
                      'character'
                  )
                ORDER BY ordinal_position
                """,
                (table,),
            )

            columns = cur.fetchall()

            if not columns:
                continue

            for column, data_type in columns:

                query = f'''
                    SELECT "{column}"
                    FROM public."{table}"
                    WHERE "{column}" IS NOT NULL
                '''

                try:
                    cur.execute(query)
                    rows = cur.fetchall()
                except Exception as exc:
                    conn.rollback()
                    print(
                        f"[SKIP] {table}.{column} -> {exc}"
                    )
                    continue

                examples = []

                for (value,) in rows:

                    if not isinstance(value, str):
                        continue

                    if not looks_mojibake(value):
                        continue

                    repaired = try_repair(value)

                    if repaired:

                        total_suspicious += 1

                        if len(examples) < 5:
                            examples.append(
                                (value, repaired)
                            )

                if examples:

                    print("-" * 70)
                    print(f"{table}.{column}")
                    print(f"Suspicious values: {len(examples)}+")

                    for old, new in examples:
                        print()
                        print("  BAD     :", repr(old))
                        print("  REPAIRED:", repr(new))

        print()
        print("=" * 70)

        if total_suspicious == 0:
            print("No obvious mojibake values were detected.")
        else:
            print(
                f"Potential mojibake values detected: "
                f"{total_suspicious}+"
            )

        print("=" * 70)
        print()
        print("IMPORTANT:")
        print("This script ONLY diagnoses.")
        print("It does NOT modify the database.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()