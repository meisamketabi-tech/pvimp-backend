from pathlib import Path
import py_compile


# ============================================================
# PVIMP - Rewrite Live Dashboard KPI Service V2
# UTF-8 SAFE GENERATOR
# ============================================================

ROOT = Path(r"D:\pvimp_backend")

TARGET = (
    ROOT
    / "app"
    / "services"
    / "gis"
    / "live_dashboard_kpi_service_v2.py"
)


CONTENT = r'''from __future__ import annotations

# =========================================================
# PVIMP LIVE DASHBOARD KPI SERVICE V2
# =========================================================
#
# Scope:
#   Zanjan Province
#
# Design:
#   - PostgreSQL live queries
#   - No snapshot
#   - No fake data
#   - No KPI cache
#   - UTF-8 source
#   - Dynamic table/column discovery
#   - Safe identifier handling
#   - Province -> County -> Epidemiology Unit scope
#
# =========================================================

from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


# =========================================================
# Fixed dashboard scope
# =========================================================

ZANJAN_PROVINCE_ID = 5


class LiveDashboardKPIServiceV2:
    """
    PVIMP Live KPI Dashboard V2.

    The dashboard is intentionally scoped to Zanjan Province.

    The service reads PostgreSQL directly and does not maintain
    a snapshot or an application-level KPI cache.
    """

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(self, db: Session):
        self.db = db

        self._tables_cache: set[str] | None = None
        self._columns_cache: dict[str, set[str]] = {}
        self._fk_cache: list[dict[str, Any]] | None = None

    # =====================================================
    # Generic database helpers
    # =====================================================

    @staticmethod
    def ident(value: str) -> str:
        """
        Safely quote a PostgreSQL identifier.

        Only simple alphanumeric/underscore identifiers are allowed.
        """
        if not value:
            raise ValueError("Empty identifier")

        if not value.replace("_", "").isalnum():
            raise ValueError(f"Unsafe identifier: {value}")

        return '"' + value + '"'

    # -----------------------------------------------------

    def tables(self) -> set[str]:
        """
        Return all public base tables.
        """

        if self._tables_cache is not None:
            return self._tables_cache

        rows = self.db.execute(
            text(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_type = 'BASE TABLE'
                """
            )
        ).mappings().all()

        self._tables_cache = {
            str(row["table_name"])
            for row in rows
        }

        return self._tables_cache

    # -----------------------------------------------------

    def has_table(self, table: str) -> bool:
        return table in self.tables()

    # -----------------------------------------------------

    def cols(self, table: str) -> set[str]:
        """
        Return columns of a table.
        """

        if table in self._columns_cache:
            return self._columns_cache[table]

        if not self.has_table(table):
            return set()

        rows = self.db.execute(
            text(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = :table
                """
            ),
            {"table": table},
        ).mappings().all()

        result = {
            str(row["column_name"])
            for row in rows
        }

        self._columns_cache[table] = result

        return result

    # -----------------------------------------------------

    def pick(
        self,
        table: str,
        *candidates: str,
    ) -> str | None:
        """
        Return the first candidate column that actually exists.
        """

        available = self.cols(table)

        for candidate in candidates:
            if candidate in available:
                return candidate

        return None

    # -----------------------------------------------------

    def scalar(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        default: Any = 0,
    ):
        """
        Execute a scalar query.
        """

        value = self.db.execute(
            text(sql),
            params or {},
        ).scalar()

        if value is None:
            return default

        if isinstance(value, Decimal):
            return float(value)

        return value

    # -----------------------------------------------------

    def rows(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Execute a query and return dictionaries.
        """

        result = self.db.execute(
            text(sql),
            params or {},
        ).mappings().all()

        return [dict(row) for row in result]

    # -----------------------------------------------------

    def clean(self, value):
        """
        Convert DB/Python values into JSON-safe values.
        """

        if isinstance(value, dict):
            return {
                key: self.clean(item)
                for key, item in value.items()
            }

        if isinstance(value, list):
            return [
                self.clean(item)
                for item in value
            ]

        if isinstance(value, tuple):
            return [
                self.clean(item)
                for item in value
            ]

        if isinstance(value, (datetime, date)):
            return value.isoformat()

        if isinstance(value, Decimal):
            return float(value)

        return value

    # -----------------------------------------------------

    def count(
        self,
        table: str,
        where: str = "TRUE",
        params: dict[str, Any] | None = None,
    ) -> int:
        """
        Count rows.

        IMPORTANT:
        `where` must NOT use an undefined table alias.

        This fixes the previous V2 problem where a condition such as
        o.epidemiology_unit_id was passed to a query whose FROM clause
        did not define alias `o`.
        """

        if not self.has_table(table):
            return 0

        value = self.scalar(
            f"""
            SELECT COUNT(*)
            FROM {self.ident(table)}
            WHERE {where}
            """,
            params,
            0,
        )

        return int(value)

    # -----------------------------------------------------

    def count_alias(
        self,
        table: str,
        alias: str,
        where: str = "TRUE",
        params: dict[str, Any] | None = None,
    ) -> int:
        """
        Count rows when the WHERE clause explicitly uses an alias.
        """

        if not self.has_table(table):
            return 0

        value = self.scalar(
            f"""
            SELECT COUNT(*)
            FROM {self.ident(table)} {alias}
            WHERE {where}
            """,
            params,
            0,
        )

        return int(value)

    # -----------------------------------------------------

    def sum_column(
        self,
        table: str,
        column: str | None,
        where: str = "TRUE",
        params: dict[str, Any] | None = None,
    ) -> float:

        if not column:
            return 0.0

        if not self.has_table(table):
            return 0.0

        if column not in self.cols(table):
            return 0.0

        value = self.scalar(
            f"""
            SELECT COALESCE(
                SUM({self.ident(column)}),
                0
            )
            FROM {self.ident(table)}
            WHERE {where}
            """,
            params,
            0,
        )

        return float(value)

    # =====================================================
    # PostgreSQL FK discovery
    # =====================================================

    def foreign_keys(self) -> list[dict[str, Any]]:
        """
        Read actual PostgreSQL foreign-key metadata.
        """

        if self._fk_cache is not None:
            return self._fk_cache

        rows = self.rows(
            """
            SELECT
                tc.table_name AS source_table,
                kcu.column_name AS source_column,
                ccu.table_name AS target_table,
                ccu.column_name AS target_column
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
             AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage ccu
              ON ccu.constraint_name = tc.constraint_name
             AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
              AND tc.table_schema = 'public'
            ORDER BY
                tc.table_name,
                kcu.column_name
            """
        )

        self._fk_cache = rows

        return rows

    # -----------------------------------------------------

    def table_fks(self, table: str) -> list[dict[str, Any]]:
        return [
            row
            for row in self.foreign_keys()
            if row["source_table"] == table
        ]

    # -----------------------------------------------------

    def fk_column_to(
        self,
        source_table: str,
        target_tables: list[str],
    ) -> str | None:
        """
        Discover a real FK column from source_table to one of target_tables.
        """

        target_set = set(target_tables)

        for fk in self.table_fks(source_table):
            if fk["target_table"] in target_set:
                return str(fk["source_column"])

        return None

    # -----------------------------------------------------

    def fk_target_table(
        self,
        source_table: str,
        source_column: str,
    ) -> str | None:

        for fk in self.table_fks(source_table):
            if fk["source_column"] == source_column:
                return str(fk["target_table"])

        return None

    # =====================================================
    # Entity discovery
    # =====================================================

    def find_table(
        self,
        candidates: list[str],
    ) -> str | None:

        available = self.tables()

        for name in candidates:
            if name in available:
                return name

        return None

    # -----------------------------------------------------

    def province_table(self) -> str | None:
        return self.find_table(
            [
                "gis_provinces",
                "provinces",
                "province",
            ]
        )

    # -----------------------------------------------------

    def county_table(self) -> str | None:
        return self.find_table(
            [
                "gis_counties",
                "counties",
                "county",
            ]
        )

    # -----------------------------------------------------

    def unit_table(self) -> str | None:
        return self.find_table(
            [
                "gis_epidemiology_units",
                "gis_epidemiological_units",
                "epidemiology_units",
            ]
        )

    # -----------------------------------------------------

    def disease_table(self) -> str | None:
        return self.find_table(
            [
                "gis_diseases",
                "diseases",
                "disease",
            ]
        )

    # =====================================================
    # Name helpers
    # =====================================================

    def name_column(self, table: str) -> str | None:

        return self.pick(
            table,
            "name_fa",
            "name",
            "title",
            "label",
            "unit_name",
            "unit_title",
            "province_name",
            "county_name",
            "disease_name",
        )

    # =====================================================
    # Scope helpers
    # =====================================================

    def zanjan_params(self) -> dict[str, Any]:
        return {
            "zanjan_province_id": ZANJAN_PROVINCE_ID,
        }

    # -----------------------------------------------------

    def zanjan_unit_where(
        self,
        table_alias: str = "u",
    ) -> str | None:
        """
        Condition for an epidemiology unit belonging to Zanjan.
        """

        unit_table = self.unit_table()

        if not unit_table:
            return None

        province_fk = self.pick(
            unit_table,
            "province_id",
        )

        if not province_fk:
            province_fk = self.fk_column_to(
                unit_table,
                [
                    "gis_provinces",
                    "provinces",
                    "province",
                ],
            )

        if not province_fk:
            return None

        return (
            f"{table_alias}.{self.ident(province_fk)} "
            f"= :zanjan_province_id"
        )

    # -----------------------------------------------------

    def operation_unit_fk(
        self,
        operation_table: str,
    ) -> str | None:
        """
        Find the operation -> epidemiology unit FK.

        First use known project naming, then actual PostgreSQL FK metadata.
        """

        direct = self.pick(
            operation_table,
            "epidemiology_unit_id",
        )

        if direct:
            return direct

        return self.fk_column_to(
            operation_table,
            [
                "gis_epidemiology_units",
                "gis_epidemiological_units",
                "epidemiology_units",
            ],
        )

    # -----------------------------------------------------

    def zanjan_operation_where(
        self,
        operation_table: str,
    ) -> str | None:
        """
        Return a WHERE condition WITHOUT an alias.

        This is intentionally compatible with `count()`.

        Example result:

        "epidemiology_unit_id" IN (
            SELECT u.id
            FROM "gis_epidemiology_units" u
            WHERE u."province_id" = :zanjan_province_id
        )
        """

        unit_table = self.unit_table()

        if not unit_table:
            return None

        operation_unit_fk = self.operation_unit_fk(
            operation_table
        )

        if not operation_unit_fk:
            return None

        province_fk = self.pick(
            unit_table,
            "province_id",
        )

        if not province_fk:
            province_fk = self.fk_column_to(
                unit_table,
                [
                    "gis_provinces",
                    "provinces",
                    "province",
                ],
            )

        if not province_fk:
            return None

        return f"""
            {self.ident(operation_unit_fk)}
            IN (
                SELECT u.id
                FROM {self.ident(unit_table)} u
                WHERE u.{self.ident(province_fk)}
                    = :zanjan_province_id
            )
        """

    # -----------------------------------------------------

    def operation_zanjan_scope(
        self,
        operation_table: str,
        alias: str = "o",
    ) -> str | None:
        """
        Alias-aware version for queries using FROM table alias.
        """

        unit_table = self.unit_table()

        if not unit_table:
            return None

        operation_unit_fk = self.operation_unit_fk(
            operation_table
        )

        if not operation_unit_fk:
            return None

        province_fk = self.pick(
            unit_table,
            "province_id",
        )

        if not province_fk:
            province_fk = self.fk_column_to(
                unit_table,
                [
                    "gis_provinces",
                    "provinces",
                    "province",
                ],
            )

        if not province_fk:
            return None

        return f"""
            {alias}.{self.ident(operation_unit_fk)}
            IN (
                SELECT u.id
                FROM {self.ident(unit_table)} u
                WHERE u.{self.ident(province_fk)}
                    = :zanjan_province_id
            )
        """

    # =====================================================
    # Global overview
    # =====================================================

    def overview(self):

        units = self.unit_table()

        total_units = 0
        active_units = 0

        # -------------------------------------------------
        # Units
        # -------------------------------------------------

        if units:

            province_fk = self.pick(
                units,
                "province_id",
            )

            if not province_fk:
                province_fk = self.fk_column_to(
                    units,
                    [
                        "gis_provinces",
                        "provinces",
                        "province",
                    ],
                )

            if province_fk:

                scope = (
                    f"{self.ident(province_fk)} "
                    f"= :zanjan_province_id"
                )

                total_units = self.count(
                    units,
                    scope,
                    self.zanjan_params(),
                )

                active = self.pick(
                    units,
                    "is_active",
                    "active",
                    "enabled",
                )

                if active:

                    active_units = self.count(
                        units,
                        f"""
                        {scope}
                        AND {self.ident(active)} = TRUE
                        """,
                        self.zanjan_params(),
                    )

                else:
                    active_units = total_units

        # -------------------------------------------------
        # Generic operation count
        # -------------------------------------------------

        def operation_count(
            candidates: list[str],
        ) -> int:

            table = self.find_table(candidates)

            if not table:
                return 0

            where = self.zanjan_operation_where(table)

            if not where:
                return 0

            try:
                return self.count(
                    table,
                    where,
                    self.zanjan_params(),
                )
            except Exception:
                return 0

        # -------------------------------------------------
        # Operations
        # -------------------------------------------------

        disease_reports = operation_count(
            [
                "gis_disease_reports",
                "gis_disease_report",
            ]
        )

        disease_occurrences = operation_count(
            [
                "gis_disease_occurrences",
                "gis_disease_occurrence",
            ]
        )

        care_records = operation_count(
            [
                "gis_enable_cares",
                "gis_enable_care",
                "gis_active_cares",
            ]
        )

        lab_table = self.find_table(
            [
                "gis_laboratory_results",
                "gis_laboratory_result",
                "laboratory_results",
            ]
        )

        sample_table = self.find_table(
            [
                "gis_send_sample_details",
                "gis_send_sample_detail",
                "gis_samples",
                "gis_sample_details",
            ]
        )

        lab_results = operation_count(
            [
                "gis_laboratory_results",
                "gis_laboratory_result",
                "laboratory_results",
            ]
        )

        sample_records = operation_count(
            [
                "gis_send_sample_details",
                "gis_send_sample_detail",
                "gis_samples",
                "gis_sample_details",
            ]
        )

        # -------------------------------------------------
        # Vaccination
        # -------------------------------------------------

        vaccination_table = self.find_table(
            [
                "gis_vaccination_performances",
                "gis_vaccination_performance",
            ]
        )

        vaccinated = 0.0
        eligible = 0.0

        if vaccination_table:

            value_col = self.pick(
                vaccination_table,
                "vaccinated_animals",
                "vaccinated_count",
                "performed_count",
                "animal_count",
            )

            eligible_col = self.pick(
                vaccination_table,
                "eligible_animals",
                "eligible_count",
                "target_animals",
                "planned_animals",
            )

            scope = self.operation_zanjan_scope(
                vaccination_table,
                "o",
            )

            if scope:

                if value_col:

                    vaccinated = float(
                        self.scalar(
                            f"""
                            SELECT COALESCE(
                                SUM(
                                    o.{self.ident(value_col)}
                                ),
                                0
                            )
                            FROM {self.ident(vaccination_table)} o
                            WHERE {scope}
                            """,
                            self.zanjan_params(),
                            0,
                        )
                    )

                if eligible_col:

                    eligible = float(
                        self.scalar(
                            f"""
                            SELECT COALESCE(
                                SUM(
                                    o.{self.ident(eligible_col)}
                                ),
                                0
                            )
                            FROM {self.ident(vaccination_table)} o
                            WHERE {scope}
                            """,
                            self.zanjan_params(),
                            0,
                        )
                    )

        coverage = (
            round(
                vaccinated / eligible * 100,
                2,
            )
            if eligible
            else 0
        )

        # -------------------------------------------------
        # Positive laboratory results
        # -------------------------------------------------

        lab_positive = 0

        if lab_table:

            status = self.pick(
                lab_table,
                "result_status",
                "status",
                "result",
                "result_value",
            )

            scope = self.operation_zanjan_scope(
                lab_table,
                "o",
            )

            if status and scope:

                try:

                    lab_positive = self.count_alias(
                        lab_table,
                        "o",
                        f"""
                        {scope}
                        AND
                        (
                            LOWER(
                                COALESCE(
                                    CAST(
                                        o.{self.ident(status)}
                                        AS TEXT
                                    ),
                                    ''
                                )
                            ) LIKE '%positive%'

                            OR

                            LOWER(
                                COALESCE(
                                    CAST(
                                        o.{self.ident(status)}
                                        AS TEXT
                                    ),
                                    ''
                                )
                            ) LIKE '%مثبت%'
                        )
                        """,
                        self.zanjan_params(),
                    )

                except Exception:
                    lab_positive = 0

        lab_positive_rate = (
            round(
                lab_positive / lab_results * 100,
                2,
            )
            if lab_results
            else 0
        )

        # -------------------------------------------------
        # Vaccine inventory / distribution / disposal
        # -------------------------------------------------

        def operation_sum(
            candidates: list[str],
            columns: list[str],
        ) -> float:

            table = self.find_table(candidates)

            if not table:
                return 0.0

            value_col = self.pick(
                table,
                *columns,
            )

            if not value_col:
                return 0.0

            scope = self.operation_zanjan_scope(
                table,
                "o",
            )

            if not scope:
                return 0.0

            try:

                return float(
                    self.scalar(
                        f"""
                        SELECT COALESCE(
                            SUM(
                                o.{self.ident(value_col)}
                            ),
                            0
                        )
                        FROM {self.ident(table)} o
                        WHERE {scope}
                        """,
                        self.zanjan_params(),
                        0,
                    )
                )

            except Exception:
                return 0.0

        inventory = operation_sum(
            [
                "gis_vaccine_inventories",
                "gis_vaccine_inventory",
            ],
            [
                "quantity",
                "package_count",
                "packages_count",
                "stock_quantity",
            ],
        )

        distributed = operation_sum(
            [
                "gis_vaccine_distributions",
                "gis_vaccine_distribution",
            ],
            [
                "quantity",
                "package_count",
                "packages_count",
            ],
        )

        disposed = operation_sum(
            [
                "gis_vaccine_disposals",
                "gis_vaccine_disposal",
            ],
            [
                "quantity",
                "package_count",
                "packages_count",
            ],
        )

        return self.clean(
            {
                "live": True,

                "generated_at":
                    datetime.now(UTC),

                "province_id":
                    ZANJAN_PROVINCE_ID,

                "province_name":
                    "زنجان",

                "cards": {

                    "total_units":
                        total_units,

                    "active_units":
                        active_units,

                    "disease_reports":
                        disease_reports,

                    "disease_occurrences":
                        disease_occurrences,

                    "care_records":
                        care_records,

                    "vaccinated":
                        vaccinated,

                    "eligible":
                        eligible,

                    "vaccination_coverage":
                        coverage,

                    "vaccination_remaining":
                        max(
                            eligible - vaccinated,
                            0,
                        ),

                    "lab_results":
                        lab_results,

                    "lab_positive":
                        lab_positive,

                    "lab_positive_rate":
                        lab_positive_rate,

                    "sample_records":
                        sample_records,

                    "inventory":
                        inventory,

                    "distributed":
                        distributed,

                    "disposed":
                        disposed,
                },

                "charts": {

                    "vaccination":
                        self.vaccination_chart(),

                    "disease":
                        self.disease_chart(),

                    "care":
                        self.care_chart(),

                    "laboratory":
                        self.lab_chart(),
                },

                "drilldown": {

                    "levels": [
                        "province",
                        "county",
                        "unit",
                    ]
                }
            }
        )

    # =====================================================
    # Chart helpers
    # =====================================================

    def _scoped_chart(
        self,
        table: str,
        date_column: str,
        value_expression: str,
    ) -> list[dict[str, Any]]:
        """
        Generic Zanjan-scoped monthly chart.
        """

        scope = self.operation_zanjan_scope(
            table,
            "o",
        )

        if not scope:
            return []

        try:

            return self.rows(
                f"""
                SELECT
                    TO_CHAR(
                        DATE_TRUNC(
                            'month',
                            o.{self.ident(date_column)}
                        ),
                        'YYYY-MM'
                    ) AS period,

                    {value_expression} AS value

                FROM {self.ident(table)} o

                WHERE
                    o.{self.ident(date_column)} IS NOT NULL
                    AND
                    {scope}

                GROUP BY 1
                ORDER BY 1
                """,
                self.zanjan_params(),
            )

        except Exception:
            return []

    # -----------------------------------------------------

    def vaccination_chart(self):

        table = self.find_table(
            [
                "gis_vaccination_performances",
                "gis_vaccination_performance",
            ]
        )

        if not table:
            return []

        value = self.pick(
            table,
            "vaccinated_animals",
            "vaccinated_count",
            "performed_count",
            "animal_count",
        )

        d = self.pick(
            table,
            "vaccination_date",
            "operation_date",
            "date",
            "created_at",
        )

        if not value or not d:
            return []

        return self._scoped_chart(
            table,
            d,
            f"""
            COALESCE(
                SUM(o.{self.ident(value)}),
                0
            )::numeric
            """,
        )

    # -----------------------------------------------------

    def disease_chart(self):

        table = self.find_table(
            [
                "gis_disease_reports",
                "gis_disease_report",
            ]
        )

        if not table:
            return []

        d = self.pick(
            table,
            "report_date",
            "occurrence_date",
            "date",
            "created_at",
        )

        if not d:
            return []

        return self._scoped_chart(
            table,
            d,
            "COUNT(*)::numeric",
        )

    # -----------------------------------------------------

    def care_chart(self):

        table = self.find_table(
            [
                "gis_enable_cares",
                "gis_enable_care",
                "gis_active_cares",
            ]
        )

        if not table:
            return []

        d = self.pick(
            table,
            "care_date",
            "operation_date",
            "date",
            "created_at",
        )

        if not d:
            return []

        return self._scoped_chart(
            table,
            d,
            "COUNT(*)::numeric",
        )

    # -----------------------------------------------------

    def lab_chart(self):

        table = self.find_table(
            [
                "gis_laboratory_results",
                "gis_laboratory_result",
                "laboratory_results",
            ]
        )

        if not table:
            return []

        d = self.pick(
            table,
            "sampling_date",
            "result_date",
            "answer_date",
            "date",
            "created_at",
        )

        if not d:
            return []

        return self._scoped_chart(
            table,
            d,
            "COUNT(*)::numeric",
        )

    # =====================================================
    # Provinces
    # =====================================================

    def provinces(
        self,
        metric: str = "all",
    ):

        table = self.province_table()

        if not table:
            return []

        if "id" not in self.cols(table):
            return []

        name = self.name_column(table)

        if not name:
            name = "id"

        try:

            rows = self.rows(
                f"""
                SELECT
                    id,
                    {self.ident(name)} AS name
                FROM {self.ident(table)}
                WHERE id = :pid
                ORDER BY {self.ident(name)}
                """,
                {
                    "pid": ZANJAN_PROVINCE_ID
                },
            )

        except Exception:
            return []

        result = []

        for row in rows:

            pid = row["id"]

            value = self.location_metric(
                "province",
                pid,
                metric,
            )

            result.append(
                {
                    "id": pid,

                    "name":
                        row["name"]
                        or f"استان {pid}",

                    "value":
                        value,
                }
            )

        return self.clean(result)

    # =====================================================
    # Counties
    # =====================================================

    def counties(
        self,
        province_id: int,
        metric: str = "all",
    ):

        # Dashboard is exclusively scoped to Zanjan.
        if int(province_id) != ZANJAN_PROVINCE_ID:
            return []

        table = self.county_table()

        if not table:
            return []

        province_fk = self.pick(
            table,
            "province_id",
        )

        if not province_fk:
            province_fk = self.fk_column_to(
                table,
                [
                    "gis_provinces",
                    "provinces",
                    "province",
                ],
            )

        if not province_fk:
            return []

        name = self.name_column(table)

        if not name:
            name = "id"

        try:

            rows = self.rows(
                f"""
                SELECT
                    id,
                    {self.ident(name)} AS name
                FROM {self.ident(table)}
                WHERE {self.ident(province_fk)} = :pid
                ORDER BY {self.ident(name)}
                """,
                {
                    "pid": ZANJAN_PROVINCE_ID
                },
            )

        except Exception:
            return []

        result = []

        for row in rows:

            cid = row["id"]

            value = self.location_metric(
                "county",
                cid,
                metric,
            )

            result.append(
                {
                    "id": cid,

                    "name":
                        row["name"]
                        or f"شهرستان {cid}",

                    "value":
                        value,
                }
            )

        return self.clean(result)

    # =====================================================
    # Units
    # =====================================================

    def units(
        self,
        county_id: int,
        metric: str = "all",
    ):

        table = self.unit_table()

        if not table:
            return []

        county_fk = self.pick(
            table,
            "county_id",
        )

        if not county_fk:
            county_fk = self.fk_column_to(
                table,
                [
                    "gis_counties",
                    "counties",
                    "county",
                ],
            )

        if not county_fk:
            return []

        # -------------------------------------------------
        # Verify county belongs to Zanjan.
        # -------------------------------------------------

        county_table = self.county_table()

        if county_table:

            county_province_fk = self.pick(
                county_table,
                "province_id",
            )

            if not county_province_fk:
                county_province_fk = self.fk_column_to(
                    county_table,
                    [
                        "gis_provinces",
                        "provinces",
                        "province",
                    ],
                )

            if county_province_fk:

                try:

                    valid_count = self.count(
                        county_table,
                        f"""
                        id = :cid
                        AND {self.ident(county_province_fk)}
                            = :pid
                        """,
                        {
                            "cid": county_id,
                            "pid": ZANJAN_PROVINCE_ID,
                        },
                    )

                    if valid_count == 0:
                        return []

                except Exception:
                    return []

        name = self.name_column(table)

        if not name:
            name = "id"

        try:

            rows = self.rows(
                f"""
                SELECT
                    id,
                    {self.ident(name)} AS name
                FROM {self.ident(table)}
                WHERE {self.ident(county_fk)} = :cid
                ORDER BY {self.ident(name)}
                """,
                {
                    "cid": county_id
                },
            )

        except Exception:
            return []

        result = []

        for row in rows:

            uid = row["id"]

            value = self.unit_metric(
                uid,
                metric,
            )

            result.append(
                {
                    "id": uid,

                    "name":
                        row["name"]
                        or f"واحد {uid}",

                    "value":
                        value,
                }
            )

        return self.clean(result)

    # =====================================================
    # Location metric
    # =====================================================

    def location_metric(
        self,
        level: str,
        location_id: int,
        metric: str,
    ):

        table = self.unit_table()

        if not table:
            return 0

        if level == "province":

            fk = self.pick(
                table,
                "province_id",
            )

            if not fk:
                fk = self.fk_column_to(
                    table,
                    [
                        "gis_provinces",
                        "provinces",
                        "province",
                    ],
                )

        else:

            fk = self.pick(
                table,
                "county_id",
            )

            if not fk:
                fk = self.fk_column_to(
                    table,
                    [
                        "gis_counties",
                        "counties",
                        "county",
                    ],
                )

        if not fk:
            return 0

        # -------------------------------------------------
        # Unit count
        # -------------------------------------------------

        if metric == "units":

            return self.count(
                table,
                f"{self.ident(fk)} = :id",
                {
                    "id": location_id
                },
            )

        # -------------------------------------------------
        # Vaccination
        # -------------------------------------------------

        if metric == "vaccination":

            vp = self.find_table(
                [
                    "gis_vaccination_performances",
                    "gis_vaccination_performance",
                ]
            )

            if not vp:
                return 0

            unit_fk = self.operation_unit_fk(vp)

            value = self.pick(
                vp,
                "vaccinated_animals",
                "vaccinated_count",
                "performed_count",
                "animal_count",
            )

            if not unit_fk or not value:
                return 0

            try:

                return float(
                    self.scalar(
                        f"""
                        SELECT COALESCE(
                            SUM(p.{self.ident(value)}),
                            0
                        )

                        FROM {self.ident(vp)} p

                        JOIN {self.ident(table)} u
                          ON u.id =
                             p.{self.ident(unit_fk)}

                        WHERE
                            u.{self.ident(fk)}
                            = :id
                        """,
                        {
                            "id": location_id
                        },
                        0,
                    )
                )

            except Exception:
                return 0

        # -------------------------------------------------
        # Generic sources
        # -------------------------------------------------

        source_map = {

            "disease":
                [
                    "gis_disease_reports",
                    "gis_disease_report",
                ],

            "care":
                [
                    "gis_enable_cares",
                    "gis_enable_care",
                    "gis_active_cares",
                ],

            "lab":
                [
                    "gis_laboratory_results",
                    "gis_laboratory_result",
                    "laboratory_results",
                ],

            "samples":
                [
                    "gis_send_sample_details",
                    "gis_send_sample_detail",
                    "gis_samples",
                ],

            "all":
                [],
        }

        sources = source_map.get(
            metric,
            [],
        )

        source = self.find_table(sources)

        if source:

            source_fk = self.operation_unit_fk(source)

            if source_fk:

                try:

                    return self.count(
                        source,
                        f"""
                        {self.ident(source_fk)}
                        IN (
                            SELECT id
                            FROM {self.ident(table)}
                            WHERE {self.ident(fk)}
                                = :id
                        )
                        """,
                        {
                            "id": location_id
                        },
                    )

                except Exception:
                    return 0

        # -------------------------------------------------
        # All metrics
        # -------------------------------------------------

        if metric == "all":

            total = 0

            candidates = [

                "gis_disease_reports",
                "gis_disease_report",

                "gis_enable_cares",
                "gis_enable_care",

                "gis_vaccination_performances",
                "gis_vaccination_performance",

                "gis_laboratory_results",
                "gis_laboratory_result",

                "gis_send_sample_details",
                "gis_send_sample_detail",

                "gis_slaughter_disposals",
                "gis_slaughter_disposal",

                "gis_spraying",

                "gis_vaccine_distributions",
                "gis_vaccine_distribution",

                "gis_vaccine_disposals",
                "gis_vaccine_disposal",

                "gis_disease_occurrences",
                "gis_disease_occurrence",
            ]

            for candidate in candidates:

                if not self.has_table(candidate):
                    continue

                fk2 = self.operation_unit_fk(
                    candidate
                )

                if not fk2:
                    continue

                try:

                    total += self.count(
                        candidate,
                        f"""
                        {self.ident(fk2)}
                        IN (
                            SELECT id
                            FROM {self.ident(table)}
                            WHERE {self.ident(fk)}
                                = :id
                        )
                        """,
                        {
                            "id": location_id
                        },
                    )

                except Exception:
                    continue

            return total

        return 0

    # =====================================================
    # Unit metric
    # =====================================================

    def unit_metric(
        self,
        unit_id: int,
        metric: str,
    ):

        sources = {

            "disease":
                [
                    "gis_disease_reports",
                    "gis_disease_report",
                ],

            "care":
                [
                    "gis_enable_cares",
                    "gis_enable_care",
                    "gis_active_cares",
                ],

            "vaccination":
                [
                    "gis_vaccination_performances",
                    "gis_vaccination_performance",
                ],

            "lab":
                [
                    "gis_laboratory_results",
                    "gis_laboratory_result",
                    "laboratory_results",
                ],

            "samples":
                [
                    "gis_send_sample_details",
                    "gis_send_sample_detail",
                    "gis_samples",
                ],

            "spraying":
                [
                    "gis_spraying",
                ],

            "slaughter":
                [
                    "gis_slaughter_disposals",
                    "gis_slaughter_disposal",
                ],

            "all":
                [],
        }

        # -------------------------------------------------
        # All
        # -------------------------------------------------

        if metric == "all":

            total = 0

            candidates = [

                "gis_disease_reports",
                "gis_disease_report",

                "gis_enable_cares",
                "gis_enable_care",

                "gis_vaccination_performances",
                "gis_vaccination_performance",

                "gis_laboratory_results",
                "gis_laboratory_result",

                "gis_send_sample_details",
                "gis_send_sample_detail",

                "gis_slaughter_disposals",
                "gis_slaughter_disposal",

                "gis_spraying",

                "gis_vaccine_distributions",
                "gis_vaccine_distribution",

                "gis_vaccine_disposals",
                "gis_vaccine_disposal",

                "gis_disease_occurrences",
                "gis_disease_occurrence",
            ]

            for table in candidates:

                if not self.has_table(table):
                    continue

                fk = self.operation_unit_fk(table)

                if not fk:
                    continue

                try:

                    total += self.count(
                        table,
                        f"{self.ident(fk)} = :uid",
                        {
                            "uid": unit_id
                        },
                    )

                except Exception:
                    continue

            return total

        # -------------------------------------------------
        # Specific metric
        # -------------------------------------------------

        table = self.find_table(
            sources.get(metric, [])
        )

        if not table:
            return 0

        fk = self.operation_unit_fk(table)

        if not fk:
            return 0

        try:

            return self.count(
                table,
                f"{self.ident(fk)} = :uid",
                {
                    "uid": unit_id
                },
            )

        except Exception:
            return 0

    # =====================================================
    # Unit detail
    # =====================================================

    def unit_detail(
        self,
        unit_id: int,
    ):

        table = self.unit_table()

        if not table:
            return {
                "unit": None,
                "operations": [],
            }

        # -------------------------------------------------
        # Verify Unit belongs to Zanjan
        # -------------------------------------------------

        province_fk = self.pick(
            table,
            "province_id",
        )

        if not province_fk:
            province_fk = self.fk_column_to(
                table,
                [
                    "gis_provinces",
                    "provinces",
                    "province",
                ],
            )

        if province_fk:

            try:

                valid = self.count(
                    table,
                    f"""
                    id = :uid
                    AND {self.ident(province_fk)}
                        = :pid
                    """,
                    {
                        "uid": unit_id,
                        "pid": ZANJAN_PROVINCE_ID,
                    },
                )

                if valid == 0:

                    return {
                        "unit": None,
                        "operations": [],
                    }

            except Exception:
                return {
                    "unit": None,
                    "operations": [],
                }

        name = self.name_column(table)

        if not name:
            name = "id"

        try:

            rows = self.rows(
                f"""
                SELECT
                    id,
                    {self.ident(name)} AS name
                FROM {self.ident(table)}
                WHERE id = :uid
                """,
                {
                    "uid": unit_id
                },
            )

        except Exception:
            rows = []

        if not rows:
            return {
                "unit": None,
                "operations": [],
            }

        unit = rows[0]

        cards = {

            "all":
                self.unit_metric(
                    unit_id,
                    "all",
                ),

            "disease":
                self.unit_metric(
                    unit_id,
                    "disease",
                ),

            "care":
                self.unit_metric(
                    unit_id,
                    "care",
                ),

            "vaccination":
                self.unit_metric(
                    unit_id,
                    "vaccination",
                ),

            "lab":
                self.unit_metric(
                    unit_id,
                    "lab",
                ),

            "samples":
                self.unit_metric(
                    unit_id,
                    "samples",
                ),

            "spraying":
                self.unit_metric(
                    unit_id,
                    "spraying",
                ),

            "slaughter":
                self.unit_metric(
                    unit_id,
                    "slaughter",
                ),
        }

        operations = self.operation_timeline(
            unit_id
        )

        return self.clean(
            {
                "unit": unit,

                "cards": cards,

                "operations":
                    operations,

                "operation_count":
                    len(operations),
            }
        )

    # =====================================================
    # Operation timeline
    # =====================================================

    def operation_timeline(
        self,
        unit_id: int,
    ):

        specs = [

            (
                [
                    "gis_vaccination_performances",
                    "gis_vaccination_performance",
                ],
                "واکسیناسیون",
                [
                    "vaccination_date",
                    "operation_date",
                    "date",
                    "created_at",
                ],
            ),

            (
                [
                    "gis_disease_reports",
                    "gis_disease_report",
                ],
                "گزارش بیماری",
                [
                    "report_date",
                    "occurrence_date",
                    "date",
                    "created_at",
                ],
            ),

            (
                [
                    "gis_disease_occurrences",
                    "gis_disease_occurrence",
                ],
                "وقوع بیماری",
                [
                    "occurrence_date",
                    "event_date",
                    "date",
                    "created_at",
                ],
            ),

            (
                [
                    "gis_enable_cares",
                    "gis_enable_care",
                    "gis_active_cares",
                ],
                "مراقبت فعال",
                [
                    "care_date",
                    "operation_date",
                    "date",
                    "created_at",
                ],
            ),

            (
                [
                    "gis_send_sample_details",
                    "gis_send_sample_detail",
                ],
                "ارسال نمونه",
                [
                    "sampling_date",
                    "send_date",
                    "operation_date",
                    "date",
                    "created_at",
                ],
            ),

            (
                [
                    "gis_laboratory_results",
                    "gis_laboratory_result",
                    "laboratory_results",
                ],
                "نتیجه آزمایشگاه",
                [
                    "result_date",
                    "answer_date",
                    "sampling_date",
                    "date",
                    "created_at",
                ],
            ),

            (
                [
                    "gis_slaughter_disposals",
                    "gis_slaughter_disposal",
                ],
                "کشتار/امحاء",
                [
                    "disposal_date",
                    "operation_date",
                    "date",
                    "created_at",
                ],
            ),

            (
                [
                    "gis_spraying",
                ],
                "سمپاشی",
                [
                    "spraying_date",
                    "operation_date",
                    "date",
                    "created_at",
                ],
            ),

            (
                [
                    "gis_vaccine_distributions",
                    "gis_vaccine_distribution",
                ],
                "توزیع واکسن",
                [
                    "distribution_date",
                    "operation_date",
                    "date",
                    "created_at",
                ],
            ),

            (
                [
                    "gis_vaccine_disposals",
                    "gis_vaccine_disposal",
                ],
                "دفع واکسن",
                [
                    "disposal_date",
                    "operation_date",
                    "date",
                    "created_at",
                ],
            ),
        ]

        result: list[dict[str, Any]] = []

        for candidates, label, date_candidates in specs:

            table = self.find_table(candidates)

            if not table:
                continue

            unit_fk = self.operation_unit_fk(
                table
            )

            if not unit_fk:
                continue

            d = self.pick(
                table,
                *date_candidates,
            )

            if not d:
                continue

            # -------------------------------------------------
            # SELECT fields
            # -------------------------------------------------

            select = [

                f"{self.ident(d)} AS event_date",

                f":operation_label AS operation_type",

                "id AS source_id",
            ]

            # -------------------------------------------------
            # Disease relation
            # -------------------------------------------------

            disease_fk = self.pick(
                table,
                "disease_id",
            )

            if disease_fk:

                select.append(
                    f"""
                    {self.ident(disease_fk)}
                    AS disease_id
                    """
                )

            else:

                select.append(
                    "NULL AS disease_id"
                )

            # -------------------------------------------------
            # Sample relation
            # -------------------------------------------------

            sample_fk = self.pick(
                table,
                "sample_id",
                "send_sample_id",
                "sample_detail_id",
            )

            if sample_fk:

                select.append(
                    f"""
                    {self.ident(sample_fk)}
                    AS sample_id
                    """
                )

            else:

                select.append(
                    "NULL AS sample_id"
                )

            # -------------------------------------------------
            # Laboratory relation
            # -------------------------------------------------

            lab_fk = self.pick(
                table,
                "laboratory_result_id",
                "lab_result_id",
            )

            if lab_fk:

                select.append(
                    f"""
                    {self.ident(lab_fk)}
                    AS laboratory_result_id
                    """
                )

            else:

                select.append(
                    "NULL AS laboratory_result_id"
                )

            # -------------------------------------------------
            # Result status
            # -------------------------------------------------

            result_col = self.pick(
                table,
                "result_status",
                "status",
                "result",
                "result_value",
            )

            if result_col:

                select.append(
                    f"""
                    CAST(
                        {self.ident(result_col)}
                        AS TEXT
                    ) AS result_status
                    """
                )

            else:

                select.append(
                    "NULL AS result_status"
                )

            # -------------------------------------------------
            # Animal count
            # -------------------------------------------------

            animal_col = self.pick(
                table,
                "animal_count",
                "animals_count",
                "total_animals",
                "vaccinated_animals",
                "eligible_animals",
            )

            if animal_col:

                select.append(
                    f"""
                    {self.ident(animal_col)}
                    AS animal_count
                    """
                )

            else:

                select.append(
                    "NULL AS animal_count"
                )

            # -------------------------------------------------
            # Execute
            # -------------------------------------------------

            sql = f"""
                SELECT
                    {', '.join(select)}

                FROM {self.ident(table)}

                WHERE
                    {self.ident(unit_fk)} = :uid

                    AND

                    {self.ident(d)} IS NOT NULL
            """

            try:

                rows = self.rows(
                    sql,
                    {
                        "uid": unit_id,
                        "operation_label": label,
                    },
                )

                result.extend(rows)

            except Exception:
                # Optional source tables must never kill
                # the entire dashboard.
                continue

        # -----------------------------------------------------
        # Newest first
        # -----------------------------------------------------

        result.sort(
            key=lambda item:
                str(
                    item.get("event_date")
                    or ""
                ),
            reverse=True,
        )

        return result[:2000]

    # =====================================================
    # Related operation chain
    # =====================================================

    def related_chain(
        self,
        unit_id: int,
        operation_id: int | None = None,
    ):

        timeline = self.operation_timeline(
            unit_id
        )

        if operation_id is None:
            return timeline

        selected = None

        for event in timeline:

            if event.get("source_id") == operation_id:

                selected = event
                break

        if not selected:
            return []

        disease_id = selected.get(
            "disease_id"
        )

        sample_id = selected.get(
            "sample_id"
        )

        lab_id = selected.get(
            "laboratory_result_id"
        )

        chain = []

        for event in timeline:

            same_disease = (
                disease_id is not None
                and event.get("disease_id")
                == disease_id
            )

            same_sample = (
                sample_id is not None
                and event.get("sample_id")
                == sample_id
            )

            same_lab = (
                lab_id is not None
                and event.get("laboratory_result_id")
                == lab_id
            )

            if (
                event.get("source_id")
                == operation_id

                or same_disease

                or same_sample

                or same_lab
            ):

                chain.append(event)

        chain.sort(
            key=lambda item:
                str(
                    item.get("event_date")
                    or ""
                )
        )

        return self.clean(chain)
'''


def main() -> None:

    print("=" * 70)
    print("PVIMP - Rebuilding Live Dashboard KPI Service V2")
    print("=" * 70)

    if not ROOT.exists():
        raise SystemExit(
            f"Project directory not found: {ROOT}"
        )

    TARGET.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Backup existing file
    # --------------------------------------------------------

    if TARGET.exists():

        backup = TARGET.with_suffix(
            TARGET.suffix + ".bak"
        )

        backup.write_text(
            TARGET.read_text(
                encoding="utf-8"
            ),
            encoding="utf-8",
        )

        print(f"[OK] Backup created:")
        print(f"     {backup}")

    # --------------------------------------------------------
    # Write UTF-8
    # --------------------------------------------------------

    TARGET.write_text(
        CONTENT,
        encoding="utf-8",
        newline="\n",
    )

    print()
    print("[OK] File written with UTF-8:")
    print(f"     {TARGET}")

    # --------------------------------------------------------
    # Verify UTF-8 Persian content
    # --------------------------------------------------------

    content = TARGET.read_text(
        encoding="utf-8"
    )

    checks = [
        "زنجان",
        "استان",
        "شهرستان",
        "واحد",
        "واکسیناسیون",
        "گزارش بیماری",
        "مراقبت فعال",
        "نتیجه آزمایشگاه",
    ]

    print()
    print("UTF-8 content verification:")

    for item in checks:

        if item in content:
            print(f"[OK] {item}")
        else:
            print(f"[WARN] Missing: {item}")

    # --------------------------------------------------------
    # Check for previous Mojibake
    # --------------------------------------------------------

    mojibake_markers = [
        "Ø§",
        "Ø´",
        "Ùˆ",
        "Ù…",
        "Ú",
    ]

    found_mojibake = [
        marker
        for marker in mojibake_markers
        if marker in content
    ]

    print()

    if found_mojibake:
        print(
            "[WARN] Possible Mojibake markers found:"
        )
        print(
            "       "
            + ", ".join(found_mojibake)
        )
    else:
        print(
            "[OK] No common Mojibake markers found."
        )

    # --------------------------------------------------------
    # Python compile
    # --------------------------------------------------------

    print()
    print("Running Python compile check...")

    py_compile.compile(
        str(TARGET),
        doraise=True,
    )

    print("[OK] Python syntax/compile check passed.")

    # --------------------------------------------------------
    # Final
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("DONE")
    print("=" * 70)
    print()
    print("Target:")
    print(TARGET)
    print()
    print("Backup:")
    print(
        TARGET.with_suffix(
            TARGET.suffix + ".bak"
        )
    )
    print()
    print("The service is ready for the next test.")
    print("=" * 70)


if __name__ == "__main__":
    main()