# ============================================================
# PVIMP - FIX PERSIAN UTF-8 / MOJIBAKE
# ============================================================

$ErrorActionPreference = "Stop"

$ProjectRoot = "D:\pvimp_backend"
$BackupDir = Join-Path $ProjectRoot ("_encoding_backup_" + (Get-Date -Format "yyyyMMdd_HHmmss"))
$PythonFile = Join-Path $ProjectRoot "fix_persian_encoding.py"

Write-Host "============================================================"
Write-Host "PVIMP - FIX PERSIAN ENCODING"
Write-Host "============================================================"
Write-Host ""

# ------------------------------------------------------------
# Create Python repair script
# ------------------------------------------------------------

@'
# -*- coding: utf-8 -*-

import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# ============================================================
# DATABASE CONFIG
# ============================================================

DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "pvimp_db"
DB_USER = "postgres"

PROJECT_ROOT = Path(r"D:\pvimp_backend")

# ============================================================
# Install/import psycopg
# ============================================================

try:
    import psycopg
except ImportError:
    print("psycopg not found. Installing...")
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "psycopg[binary]"
    ])
    import psycopg


# ============================================================
# Persian / Arabic Unicode ranges
# ============================================================

def is_persian_char(ch):
    return (
        "\u0600" <= ch <= "\u06ff"
        or "\u0750" <= ch <= "\u077f"
        or "\u08a0" <= ch <= "\u08ff"
        or "\ufb50" <= ch <= "\ufdff"
        or "\ufe70" <= ch <= "\ufeff"
    )


def persian_score(text):
    if not isinstance(text, str):
        return 0

    return sum(
        1 for ch in text
        if is_persian_char(ch)
    )


# ============================================================
# Mojibake detection
# ============================================================

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


def mojibake_score(text):
    if not isinstance(text, str):
        return 0

    return sum(text.count(x) for x in BAD_MARKERS)


def looks_broken(text):
    if not isinstance(text, str):
        return False

    if len(text.strip()) == 0:
        return False

    bad = mojibake_score(text)
    persian = persian_score(text)

    # Typical UTF8->Latin1 mojibake:
    # Ø§Ø¨Ù‡Ø±
    return bad >= 2 and persian < 3


# ============================================================
# Repair one value
# ============================================================

def repair_once(value):

    if not isinstance(value, str):
        return None

    candidates = []

    for encoding in ("latin1", "cp1252"):

        try:

            repaired = value.encode(encoding).decode("utf-8")

            if repaired != value:

                candidates.append(repaired)

        except (
            UnicodeEncodeError,
            UnicodeDecodeError
        ):
            pass

    if not candidates:
        return None

    # Choose candidate with highest Persian score.
    candidates.sort(
        key=persian_score,
        reverse=True
    )

    best = candidates[0]

    if persian_score(best) > persian_score(value):
        return best

    return None


def repair_value(value):

    current = value

    # Support accidental double encoding.
    for _ in range(3):

        repaired = repair_once(current)

        if not repaired:
            break

        current = repaired

    if current != value:
        return current

    return None


# ============================================================
# PostgreSQL identifier quoting
# ============================================================

def quote_identifier(name):
    return '"' + name.replace('"', '""') + '"'


# ============================================================
# Find pg_dump
# ============================================================

def find_pg_dump():

    candidates = [
        Path(r"C:\Program Files\PostgreSQL\18\bin\pg_dump.exe"),
        Path(r"C:\Program Files\PostgreSQL\17\bin\pg_dump.exe"),
        Path(r"C:\Program Files\PostgreSQL\16\bin\pg_dump.exe"),
        Path(r"C:\Program Files\PostgreSQL\15\bin\pg_dump.exe"),
    ]

    for path in candidates:
        if path.exists():
            return path

    found = shutil.which("pg_dump")

    if found:
        return Path(found)

    return None


# ============================================================
# Database backup
# ============================================================

def backup_database():

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_dir = (
        PROJECT_ROOT /
        f"_encoding_backup_{timestamp}"
    )

    backup_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    backup_file = (
        backup_dir /
        "pvimp_db_before_encoding_fix.dump"
    )

    pg_dump = find_pg_dump()

    if not pg_dump:
        raise RuntimeError(
            "pg_dump.exe was not found."
        )

    print()
    print("=" * 70)
    print("DATABASE BACKUP")
    print("=" * 70)
    print(f"Backup file: {backup_file}")

    command = [
        str(pg_dump),
        "-h", DB_HOST,
        "-p", DB_PORT,
        "-U", DB_USER,
        "-d", DB_NAME,
        "-F", "c",
        "-f", str(backup_file),
    ]

    print("Running pg_dump...")

    subprocess.run(
        command,
        check=True
    )

    if not backup_file.exists():
        raise RuntimeError(
            "Database backup was not created."
        )

    print("DATABASE BACKUP: OK")

    return backup_dir


# ============================================================
# Main repair
# ============================================================

def main():

    print()
    print("=" * 70)
    print("PVIMP PERSIAN ENCODING REPAIR")
    print("=" * 70)
    print()

    print("Database:")
    print(f"  host : {DB_HOST}")
    print(f"  port : {DB_PORT}")
    print(f"  db   : {DB_NAME}")
    print(f"  user : {DB_USER}")
    print()

    # --------------------------------------------------------
    # BACKUP FIRST
    # --------------------------------------------------------

    backup_dir = backup_database()

    # --------------------------------------------------------
    # CONNECT
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("CONNECTING TO POSTGRESQL")
    print("=" * 70)

    conn = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
    )

    conn.autocommit = False

    try:

        cur = conn.cursor()

        # ----------------------------------------------------
        # Force UTF-8 client encoding
        # ----------------------------------------------------

        cur.execute(
            "SET client_encoding TO 'UTF8'"
        )

        cur.execute(
            "SHOW server_encoding"
        )

        server_encoding = cur.fetchone()[0]

        cur.execute(
            "SHOW client_encoding"
        )

        client_encoding = cur.fetchone()[0]

        print(
            f"server_encoding : {server_encoding}"
        )

        print(
            f"client_encoding : {client_encoding}"
        )

        if server_encoding.upper() != "UTF8":
            raise RuntimeError(
                "PostgreSQL server_encoding is not UTF8."
            )

        # ----------------------------------------------------
        # Get GIS tables
        # ----------------------------------------------------

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

        tables = [
            row[0]
            for row in cur.fetchall()
        ]

        print()
        print(
            f"GIS tables found: {len(tables)}"
        )

        # ----------------------------------------------------
        # Counters
        # ----------------------------------------------------

        total_values_scanned = 0
        total_values_fixed = 0
        total_columns_fixed = 0

        changed_by_table = {}

        # ----------------------------------------------------
        # Process every GIS text column
        # ----------------------------------------------------

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
                (table,)
            )

            columns = cur.fetchall()

            if not columns:
                continue

            for column, data_type in columns:

                table_q = quote_identifier(table)
                column_q = quote_identifier(column)

                query = f"""
                    SELECT ctid, {column_q}
                    FROM public.{table_q}
                    WHERE {column_q} IS NOT NULL
                """

                try:

                    cur.execute(query)

                    rows = cur.fetchall()

                except Exception as exc:

                    conn.rollback()

                    cur.execute(
                        "SET client_encoding TO 'UTF8'"
                    )

                    print(
                        f"[SKIP] {table}.{column}: {exc}"
                    )

                    continue

                column_fixed = 0

                for ctid, value in rows:

                    total_values_scanned += 1

                    if not isinstance(value, str):
                        continue

                    if not looks_broken(value):
                        continue

                    repaired = repair_value(value)

                    if not repaired:
                        continue

                    # ----------------------------------------
                    # Update exact row by CTID.
                    # CTID is safe inside this transaction.
                    # ----------------------------------------

                    update_sql = f"""
                        UPDATE public.{table_q}
                        SET {column_q} = %s
                        WHERE ctid = %s
                    """

                    cur.execute(
                        update_sql,
                        (repaired, ctid)
                    )

                    column_fixed += 1
                    total_values_fixed += 1

                    # Show first few examples.
                    if column_fixed <= 3:

                        print()
                        print(
                            f"[FIX] {table}.{column}"
                        )

                        print(
                            "  OLD:",
                            repr(value)
                        )

                        print(
                            "  NEW:",
                            repr(repaired)
                        )

                if column_fixed:

                    total_columns_fixed += 1

                    changed_by_table.setdefault(
                        table,
                        0
                    )

                    changed_by_table[table] += (
                        column_fixed
                    )

                    print()
                    print(
                        f"[OK] {table}.{column}"
                        f" -> {column_fixed} values fixed"
                    )

        # ----------------------------------------------------
        # Commit
        # ----------------------------------------------------

        print()
        print("=" * 70)
        print("COMMITTING CHANGES")
        print("=" * 70)

        conn.commit()

        print("COMMIT: OK")

        # ----------------------------------------------------
        # Summary
        # ----------------------------------------------------

        print()
        print("=" * 70)
        print("ENCODING REPAIR SUMMARY")
        print("=" * 70)

        print(
            f"Values scanned : {total_values_scanned}"
        )

        print(
            f"Values fixed   : {total_values_fixed}"
        )

        print(
            f"Columns fixed  : {total_columns_fixed}"
        )

        print()

        if changed_by_table:

            print("Changes by table:")

            for table, count in sorted(
                changed_by_table.items()
            ):

                print(
                    f"  {table:<40} {count}"
                )

        else:

            print(
                "No mojibake values required repair."
            )

        print()
        print(
            f"Backup directory:"
        )
        print(
            f"  {backup_dir}"
        )

        # ----------------------------------------------------
        # Test known value from API problem
        # ----------------------------------------------------

        print()
        print("=" * 70)
        print("POST-REPAIR TEST")
        print("=" * 70)

        cur.execute(
            """
            SELECT name
            FROM public.gis_counties
            WHERE name IS NOT NULL
            ORDER BY id
            LIMIT 10
            """
        )

        county_names = [
            row[0]
            for row in cur.fetchall()
        ]

        print("Sample GIS county names:")

        for name in county_names:
            print(
                "  ",
                name
            )

        cur.execute(
            """
            SELECT name
            FROM public.gis_epidemiology_units
            WHERE name IS NOT NULL
            ORDER BY id
            LIMIT 10
            """
        )

        unit_names = [
            row[0]
            for row in cur.fetchall()
        ]

        print()
        print("Sample GIS unit names:")

        for name in unit_names:
            print(
                "  ",
                name
            )

        print()
        print("=" * 70)
        print("ENCODING REPAIR FINISHED SUCCESSFULLY")
        print("=" * 70)

    except Exception:

        print()
        print("=" * 70)
        print("ERROR - ROLLING BACK")
        print("=" * 70)

        conn.rollback()

        raise

    finally:

        conn.close()


if __name__ == "__main__":
    main()
'@ | Set-Content -Path $PythonFile -Encoding UTF8

Write-Host "Created:"
Write-Host "  $PythonFile"
Write-Host ""

# ------------------------------------------------------------
# Run Python repair
# ------------------------------------------------------------

$PythonExe = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $PythonExe)) {
    throw "Python virtual environment not found: $PythonExe"
}

Write-Host "Running encoding repair..."
Write-Host ""

& $PythonExe $PythonFile

if ($LASTEXITCODE -ne 0) {
    throw "Encoding repair failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "============================================================"
Write-Host "ENCODING FIX FINISHED SUCCESSFULLY"
Write-Host "============================================================"
Write-Host ""
Write-Host "IMPORTANT:"
Write-Host "Restart Uvicorn before testing the API."
Write-Host ""
Write-Host "Then test:"
Write-Host ""
Write-Host "  http://127.0.0.1:8000/api/v1/gis/dashboard/kpi/overview"
Write-Host ""
Write-Host "and:"
Write-Host ""
Write-Host "  http://localhost:5173/live-kpi"
Write-Host ""