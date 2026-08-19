from __future__ import annotations

# =========================================================
# ZANJAN DASHBOARD SCOPE
# =========================================================
ZANJAN_PROVINCE_ID = 5


from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class LiveDashboardKPIServiceV2:
    """
    PVIMP Live KPI Dashboard V2.

    Important:
    - Reads PostgreSQL live.
    - No snapshot.
    - No KPI cache.
    - No fake rows.
    - Uses information_schema and FK metadata.
    """

    def __init__(self, db: Session):
        self.db = db
        self._tables_cache: set[str] | None = None
        self._columns_cache: dict[str, set[str]] = {}
        self._fk_cache: list[dict[str, Any]] | None = None

    # ---------------------------------------------------------
    # Generic helpers
    # ---------------------------------------------------------

    @staticmethod
    def ident(value: str) -> str:
        if not value:
            raise ValueError("Empty identifier")

        if not value.replace("_", "").isalnum():
            raise ValueError(f"Unsafe identifier: {value}")

        return '"' + value + '"'

    def tables(self) -> set[str]:

        if self._tables_cache is None:

            rows = self.db.execute(
                text("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                      AND table_type = 'BASE TABLE'
                """)
            ).mappings().all()

            self._tables_cache = {
                str(r["table_name"])
                for r in rows
            }

        return self._tables_cache

    def has_table(self, table: str) -> bool:
        return table in self.tables()

    def cols(self, table: str) -> set[str]:

        if table in self._columns_cache:
            return self._columns_cache[table]

        if not self.has_table(table):
            return set()

        rows = self.db.execute(
            text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema='public'
                  AND table_name=:table
            """),
            {"table": table}
        ).mappings().all()

        result = {
            str(r["column_name"])
            for r in rows
        }

        self._columns_cache[table] = result

        return result

    def pick(self, table: str, *candidates: str) -> str | None:

        available = self.cols(table)

        for candidate in candidates:
            if candidate in available:
                return candidate

        return None

    def scalar(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        default=0
    ):

        value = self.db.execute(
            text(sql),
            params or {}
        ).scalar()

        if value is None:
            return default

        if isinstance(value, Decimal):
            return float(value)

        return value

    def rows(
        self,
        sql: str,
        params: dict[str, Any] | None = None
    ):

        result = self.db.execute(
            text(sql),
            params or {}
        ).mappings().all()

        return [dict(r) for r in result]

    def clean(self, value):

        if isinstance(value, dict):
            return {
                k: self.clean(v)
                for k, v in value.items()
            }

        if isinstance(value, list):
            return [
                self.clean(v)
                for v in value
            ]

        if isinstance(value, (datetime, date)):
            return value.isoformat()

        if isinstance(value, Decimal):
            return float(value)

        return value

    def count(self, table: str, where="TRUE", params=None):

        if not self.has_table(table):
            return 0

        return int(
            self.scalar(
                f"""
                SELECT COUNT(*)
                FROM {self.ident(table)}
                WHERE {where}
                """,
                params,
                0
            )
        )

    def sum_column(
        self,
        table: str,
        column: str | None,
        where="TRUE",
        params=None
    ):

        if not column:
            return 0.0

        if not self.has_table(table):
            return 0.0

        if column not in self.cols(table):
            return 0.0

        return float(
            self.scalar(
                f"""
                SELECT COALESCE(
                    SUM({self.ident(column)}),
                    0
                )
                FROM {self.ident(table)}
                WHERE {where}
                """,
                params,
                0
            )
        )

    # ---------------------------------------------------------
    # FK discovery
    # ---------------------------------------------------------

    def foreign_keys(self):

        if self._fk_cache is not None:
            return self._fk_cache

        rows = self.rows("""
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
            WHERE tc.constraint_type='FOREIGN KEY'
              AND tc.table_schema='public'
            ORDER BY tc.table_name, kcu.column_name
        """)

        self._fk_cache = rows

        return rows

    def table_fks(self, table: str):

        return [
            x for x in self.foreign_keys()
            if x["source_table"] == table
        ]

    # ---------------------------------------------------------
    # Entity discovery
    # ---------------------------------------------------------

    def find_table(self, candidates):

        available = self.tables()

        for name in candidates:
            if name in available:
                return name

        return None

    def province_table(self):

        return self.find_table([
            "gis_provinces",
            "provinces",
            "province"
        ])

    def county_table(self):

        return self.find_table([
            "gis_counties",
            "counties",
            "county"
        ])

    def unit_table(self):

        return self.find_table([
            "gis_epidemiology_units",
            "gis_epidemiological_units",
            "epidemiology_units"
        ])

    def disease_table(self):

        return self.find_table([
            "gis_diseases",
            "diseases",
            "disease"
        ])

    # ---------------------------------------------------------
    # Names
    # ---------------------------------------------------------

    def name_column(self, table: str):

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
            "disease_name"
        )

    # ---------------------------------------------------------
    # Global overview
    # ---------------------------------------------------------

    def overview(self):

        units = self.unit_table()

        total_units = self.count(units) if units else 0

        active_units = 0

        if units:

            active = self.pick(
                units,
                "is_active",
                "active",
                "enabled"
            )

            if active:
                active_units = self.count(
                    units,
                    f"{self.ident(active)} = TRUE"
                )
            else:
                active_units = total_units

        disease_reports = 0

        report_table = self.find_table([
            "gis_disease_reports",
            "gis_disease_report"
        ])

        if report_table:
            disease_reports = self.count(report_table)

        disease_occurrences = 0

        occurrence_table = self.find_table([
            "gis_disease_occurrences",
            "gis_disease_occurrence"
        ])

        if occurrence_table:
            disease_occurrences = self.count(
                occurrence_table
            )

        care_table = self.find_table([
            "gis_enable_cares",
            "gis_enable_care",
            "gis_active_cares"
        ])

        care_records = (
            self.count(care_table)
            if care_table
            else 0
        )

        vaccination_table = self.find_table([
            "gis_vaccination_performances",
            "gis_vaccination_performance"
        ])

        vaccinated_column = None
        eligible_column = None

        vaccinated = 0.0
        eligible = 0.0

        if vaccination_table:

            vaccinated_column = self.pick(
                vaccination_table,
                "vaccinated_animals",
                "vaccinated_count",
                "performed_count",
                "animal_count"
            )

            eligible_column = self.pick(
                vaccination_table,
                "eligible_animals",
                "eligible_count",
                "target_animals",
                "planned_animals"
            )

            vaccinated = self.sum_column(
                vaccination_table,
                vaccinated_column
            )

            eligible = self.sum_column(
                vaccination_table,
                eligible_column
            )

        coverage = (
            round(
                vaccinated / eligible * 100,
                2
            )
            if eligible
            else 0
        )

        lab_table = self.find_table([
            "gis_laboratory_results",
            "gis_laboratory_result",
            "laboratory_results"
        ])

        sample_table = self.find_table([
            "gis_send_sample_details",
            "gis_send_sample_detail",
            "gis_samples",
            "gis_sample_details"
        ])

        lab_results = (
            self.count(lab_table)
            if lab_table
            else 0
        )

        sample_records = (
            self.count(sample_table)
            if sample_table
            else 0
        )

        lab_positive = 0

        if lab_table:

            status = self.pick(
                lab_table,
                "result_status",
                "status",
                "result",
                "result_value"
            )

            if status:

                lab_positive = self.count(
                    lab_table,
                    f"""
                    (
                        LOWER(
                            COALESCE(
                                CAST(
                                    {self.ident(status)}
                                    AS TEXT
                                ),
                                ''
                            )
                        ) LIKE '%positive%'
                        OR
                        LOWER(
                            COALESCE(
                                CAST(
                                    {self.ident(status)}
                                    AS TEXT
                                ),
                                ''
                            )
                        ) LIKE '%Ù…Ø«Ø¨Øª%'
                    )
                    """
                )

        lab_positive_rate = (
            round(
                lab_positive / lab_results * 100,
                2
            )
            if lab_results
            else 0
        )

        inventory_table = self.find_table([
            "gis_vaccine_inventories",
            "gis_vaccine_inventory"
        ])

        distribution_table = self.find_table([
            "gis_vaccine_distributions",
            "gis_vaccine_distribution"
        ])

        disposal_table = self.find_table([
            "gis_vaccine_disposals",
            "gis_vaccine_disposal"
        ])

        inventory = self.sum_column(
            inventory_table,
            self.pick(
                inventory_table,
                "quantity",
                "package_count",
                "packages_count",
                "stock_quantity"
            )
        ) if inventory_table else 0

        distributed = self.sum_column(
            distribution_table,
            self.pick(
                distribution_table,
                "quantity",
                "package_count",
                "packages_count"
            )
        ) if distribution_table else 0

        disposed = self.sum_column(
            disposal_table,
            self.pick(
                disposal_table,
                "quantity",
                "package_count",
                "packages_count"
            )
        ) if disposal_table else 0

        return self.clean({

            "live": True,

            "generated_at": datetime.utcnow(),

            "cards": {

                "total_units": total_units,

                "active_units": active_units,

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
                        0
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

                "vaccination": self.vaccination_chart(),

                "disease": self.disease_chart(),

                "care": self.care_chart(),

                "laboratory": self.lab_chart(),

            },

            "drilldown": {

                "levels": [
                    "province",
                    "county",
                    "unit"
                ]

            }

        })

    # ---------------------------------------------------------
    # Charts
    # ---------------------------------------------------------

    def vaccination_chart(self):

        table = self.find_table([
            "gis_vaccination_performances",
            "gis_vaccination_performance"
        ])

        if not table:
            return []

        value = self.pick(
            table,
            "vaccinated_animals",
            "vaccinated_count",
            "performed_count",
            "animal_count"
        )

        d = self.pick(
            table,
            "vaccination_date",
            "operation_date",
            "date",
            "created_at"
        )

        if not value or not d:
            return []

        return self.rows(
            f"""
            SELECT
                TO_CHAR(
                    DATE_TRUNC(
                        'month',
                        {self.ident(d)}
                    ),
                    'YYYY-MM'
                ) AS period,

                COALESCE(
                    SUM({self.ident(value)}),
                    0
                )::numeric AS value

            FROM {self.ident(table)}

            WHERE {self.ident(d)} IS NOT NULL

            GROUP BY 1
            ORDER BY 1
            """
        )

    def disease_chart(self):

        table = self.find_table([
            "gis_disease_reports",
            "gis_disease_report"
        ])

        if not table:
            return []

        d = self.pick(
            table,
            "report_date",
            "occurrence_date",
            "date",
            "created_at"
        )

        if not d:
            return []

        return self.rows(
            f"""
            SELECT
                TO_CHAR(
                    DATE_TRUNC(
                        'month',
                        {self.ident(d)}
                    ),
                    'YYYY-MM'
                ) AS period,

                COUNT(*)::numeric AS value

            FROM {self.ident(table)}

            WHERE {self.ident(d)} IS NOT NULL

            GROUP BY 1
            ORDER BY 1
            """
        )

    def care_chart(self):

        table = self.find_table([
            "gis_enable_cares",
            "gis_enable_care",
            "gis_active_cares"
        ])

        if not table:
            return []

        d = self.pick(
            table,
            "care_date",
            "operation_date",
            "date",
            "created_at"
        )

        if not d:
            return []

        return self.rows(
            f"""
            SELECT
                TO_CHAR(
                    DATE_TRUNC(
                        'month',
                        {self.ident(d)}
                    ),
                    'YYYY-MM'
                ) AS period,

                COUNT(*)::numeric AS value

            FROM {self.ident(table)}

            WHERE {self.ident(d)} IS NOT NULL

            GROUP BY 1
            ORDER BY 1
            """
        )

    def lab_chart(self):

        table = self.find_table([
            "gis_laboratory_results",
            "gis_laboratory_result",
            "laboratory_results"
        ])

        if not table:
            return []

        d = self.pick(
            table,
            "sampling_date",
            "result_date",
            "answer_date",
            "date",
            "created_at"
        )

        if not d:
            return []

        return self.rows(
            f"""
            SELECT
                TO_CHAR(
                    DATE_TRUNC(
                        'month',
                        {self.ident(d)}
                    ),
                    'YYYY-MM'
                ) AS period,

                COUNT(*)::numeric AS value

            FROM {self.ident(table)}

            WHERE {self.ident(d)} IS NOT NULL

            GROUP BY 1
            ORDER BY 1
            """
        )

    # ---------------------------------------------------------
    # Provinces
    # ---------------------------------------------------------

    def provinces(self, metric="all"):

        table = self.province_table()

        if not table:
            return []

        name = self.name_column(table)

        if not name:
            name = "id"

        rows = self.rows(
            f"""
            SELECT
                id,
                {self.ident(name)} AS name
            FROM {self.ident(table)}
            ORDER BY {self.ident(name)}
            """
        )

        result = []

        for row in rows:

            pid = row["id"]

            value = self.location_metric(
                "province",
                pid,
                metric
            )

            result.append({

                "id": pid,

                "name":
                    row["name"] or
                    f"Ø§Ø³ØªØ§Ù† {pid}",

                "value":
                    value

            })

        return self.clean(result)

    # ---------------------------------------------------------
    # Counties
    # ---------------------------------------------------------

    def counties(
        self,
        province_id: int,
        metric="all"
    ):

        table = self.county_table()

        if not table:
            return []

        province_fk = self.pick(
            table,
            "province_id"
        )

        if not province_fk:
            return []

        name = self.name_column(table)

        if not name:
            name = "id"

        rows = self.rows(
            f"""
            SELECT
                id,
                {self.ident(name)} AS name
            FROM {self.ident(table)}
            WHERE {self.ident(province_fk)}=:pid
            ORDER BY {self.ident(name)}
            """,
            {"pid": province_id}
        )

        result = []

        for row in rows:

            cid = row["id"]

            value = self.location_metric(
                "county",
                cid,
                metric
            )

            result.append({

                "id": cid,

                "name":
                    row["name"] or
                    f"Ø´Ù‡Ø±Ø³ØªØ§Ù† {cid}",

                "value":
                    value

            })

        return self.clean(result)

    # ---------------------------------------------------------
    # Units
    # ---------------------------------------------------------

    def units(
        self,
        county_id: int,
        metric="all"
    ):

        table = self.unit_table()

        if not table:
            return []

        county_fk = self.pick(
            table,
            "county_id"
        )

        if not county_fk:
            return []

        name = self.name_column(table)

        if not name:
            name = "id"

        rows = self.rows(
            f"""
            SELECT
                id,
                {self.ident(name)} AS name
            FROM {self.ident(table)}
            WHERE {self.ident(county_fk)}=:cid
            ORDER BY {self.ident(name)}
            """,
            {"cid": county_id}
        )

        result = []

        for row in rows:

            uid = row["id"]

            value = self.unit_metric(
                uid,
                metric
            )

            result.append({

                "id": uid,

                "name":
                    row["name"] or
                    f"ÙˆØ§Ø­Ø¯ {uid}",

                "value":
                    value

            })

        return self.clean(result)

    # ---------------------------------------------------------
    # Metric calculation
    # ---------------------------------------------------------

    def location_metric(
        self,
        level,
        location_id,
        metric
    ):

        table = self.unit_table()

        if not table:
            return 0

        fk = (
            self.pick(table, "province_id")
            if level == "province"
            else
            self.pick(table, "county_id")
        )

        if not fk:
            return 0

        if metric == "units":
            return self.count(
                table,
                f"{self.ident(fk)}=:id",
                {"id": location_id}
            )

        if metric == "vaccination":

            vp = self.find_table([
                "gis_vaccination_performances",
                "gis_vaccination_performance"
            ])

            if not vp:
                return 0

            unit_fk = self.pick(
                vp,
                "epidemiology_unit_id"
            )

            value = self.pick(
                vp,
                "vaccinated_animals",
                "vaccinated_count",
                "performed_count",
                "animal_count"
            )

            if not unit_fk or not value:
                return 0

            return float(
                self.scalar(
                    f"""
                    SELECT COALESCE(
                        SUM(p.{self.ident(value)}),
                        0
                    )

                    FROM {self.ident(vp)} p

                    JOIN {self.ident(table)} u
                      ON u.id=p.{self.ident(unit_fk)}

                    WHERE
                        u.{self.ident(fk)}=:id
                    """,
                    {"id": location_id},
                    0
                )
            )

        source_map = {

            "disease":
                [
                    "gis_disease_reports",
                    "gis_disease_report"
                ],

            "care":
                [
                    "gis_enable_cares",
                    "gis_enable_care",
                    "gis_active_cares"
                ],

            "lab":
                [
                    "gis_laboratory_results",
                    "gis_laboratory_result"
                ],

            "samples":
                [
                    "gis_send_sample_details",
                    "gis_send_sample_detail",
                    "gis_samples"
                ],

            "all":
                []

        }

        sources = source_map.get(metric, [])

        source = self.find_table(sources)

        if source:

            source_fk = self.pick(
                source,
                "epidemiology_unit_id"
            )

            if source_fk:

                return self.count(
                    source,
                    f"""
                    {self.ident(source_fk)}
                    IN (
                        SELECT id
                        FROM {self.ident(table)}
                        WHERE {self.ident(fk)}=:id
                    )
                    """,
                    {"id": location_id}
                )

        if metric == "all":

            total = 0

            for candidate in [

                "gis_disease_reports",
                "gis_enable_cares",
                "gis_vaccination_performances",
                "gis_laboratory_results",
                "gis_send_sample_details",
                "gis_slaughter_disposals",
                "gis_spraying",
                "gis_vaccine_distributions",
                "gis_vaccine_disposals",
                "gis_disease_occurrences"

            ]:

                if not self.has_table(candidate):
                    continue

                fk2 = self.pick(
                    candidate,
                    "epidemiology_unit_id"
                )

                if not fk2:
                    continue

                total += self.count(
                    candidate,
                    f"""
                    {self.ident(fk2)}
                    IN (
                        SELECT id
                        FROM {self.ident(table)}
                        WHERE {self.ident(fk)}=:id
                    )
                    """,
                    {"id": location_id}
                )

            return total

        return 0

    def unit_metric(
        self,
        unit_id,
        metric
    ):

        sources = {

            "disease":
                [
                    "gis_disease_reports",
                    "gis_disease_report"
                ],

            "care":
                [
                    "gis_enable_cares",
                    "gis_enable_care",
                    "gis_active_cares"
                ],

            "vaccination":
                [
                    "gis_vaccination_performances",
                    "gis_vaccination_performance"
                ],

            "lab":
                [
                    "gis_laboratory_results",
                    "gis_laboratory_result"
                ],

            "samples":
                [
                    "gis_send_sample_details",
                    "gis_send_sample_detail",
                    "gis_samples"
                ],

            "spraying":
                [
                    "gis_spraying"
                ],

            "slaughter":
                [
                    "gis_slaughter_disposals"
                ],

            "all":
                []

        }

        if metric == "all":

            total = 0

            for table in [
                "gis_disease_reports",
                "gis_enable_cares",
                "gis_vaccination_performances",
                "gis_laboratory_results",
                "gis_send_sample_details",
                "gis_slaughter_disposals",
                "gis_spraying",
                "gis_vaccine_distributions",
                "gis_vaccine_disposals",
                "gis_disease_occurrences"
            ]:

                if not self.has_table(table):
                    continue

                fk = self.pick(
                    table,
                    "epidemiology_unit_id"
                )

                if fk:

                    total += self.count(
                        table,
                        f"{self.ident(fk)}=:uid",
                        {"uid": unit_id}
                    )

            return total

        table = self.find_table(
            sources.get(metric, [])
        )

        if not table:
            return 0

        fk = self.pick(
            table,
            "epidemiology_unit_id"
        )

        if not fk:
            return 0

        return self.count(
            table,
            f"{self.ident(fk)}=:uid",
            {"uid": unit_id}
        )

    # ---------------------------------------------------------
    # Unit detail
    # ---------------------------------------------------------

    def unit_detail(self, unit_id: int):

        table = self.unit_table()

        if not table:
            return {
                "unit": None,
                "operations": []
            }

        name = self.name_column(table)

        if not name:
            name = "id"

        rows = self.rows(
            f"""
            SELECT
                id,
                {self.ident(name)} AS name
            FROM {self.ident(table)}
            WHERE id=:uid
            """,
            {"uid": unit_id}
        )

        if not rows:
            return {
                "unit": None,
                "operations": []
            }

        unit = rows[0]

        cards = {

            "all":
                self.unit_metric(unit_id, "all"),

            "disease":
                self.unit_metric(unit_id, "disease"),

            "care":
                self.unit_metric(unit_id, "care"),

            "vaccination":
                self.unit_metric(unit_id, "vaccination"),

            "lab":
                self.unit_metric(unit_id, "lab"),

            "samples":
                self.unit_metric(unit_id, "samples"),

            "spraying":
                self.unit_metric(unit_id, "spraying"),

            "slaughter":
                self.unit_metric(unit_id, "slaughter"),

        }

        operations = self.operation_timeline(
            unit_id
        )

        return self.clean({

            "unit": unit,

            "cards": cards,

            "operations": operations,

            "operation_count":
                len(operations)

        })

    # ---------------------------------------------------------
    # Operation timeline
    # ---------------------------------------------------------

    def operation_timeline(self, unit_id: int):

        specs = [

            (
                "gis_vaccination_performances",
                "ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†",
                [
                    "vaccination_date",
                    "operation_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_disease_reports",
                "Ú¯Ø²Ø§Ø±Ø´ Ø¨ÛŒÙ…Ø§Ø±ÛŒ",
                [
                    "report_date",
                    "occurrence_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_disease_occurrences",
                "ÙˆÙ‚ÙˆØ¹ Ø¨ÛŒÙ…Ø§Ø±ÛŒ",
                [
                    "occurrence_date",
                    "event_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_enable_cares",
                "Ù…Ø±Ø§Ù‚Ø¨Øª ÙØ¹Ø§Ù„",
                [
                    "care_date",
                    "operation_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_send_sample_details",
                "Ø§Ø±Ø³Ø§Ù„ Ù†Ù…ÙˆÙ†Ù‡",
                [
                    "sampling_date",
                    "send_date",
                    "operation_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_laboratory_results",
                "Ù†ØªÛŒØ¬Ù‡ Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡",
                [
                    "result_date",
                    "answer_date",
                    "sampling_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_slaughter_disposals",
                "Ú©Ø´ØªØ§Ø±/Ø§Ù…Ø­Ø§Ø¡",
                [
                    "disposal_date",
                    "operation_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_spraying",
                "Ø³Ù…Ù¾Ø§Ø´ÛŒ",
                [
                    "spraying_date",
                    "operation_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_vaccine_distributions",
                "ØªÙˆØ²ÛŒØ¹ ÙˆØ§Ú©Ø³Ù†",
                [
                    "distribution_date",
                    "operation_date",
                    "date",
                    "created_at"
                ]
            ),

            (
                "gis_vaccine_disposals",
                "Ø¯ÙØ¹ ÙˆØ§Ú©Ø³Ù†",
                [
                    "disposal_date",
                    "operation_date",
                    "date",
                    "created_at"
                ]
            )

        ]

        result = []

        for table, label, date_candidates in specs:

            if not self.has_table(table):
                continue

            unit_fk = self.pick(
                table,
                "epidemiology_unit_id"
            )

            if not unit_fk:
                continue

            d = self.pick(
                table,
                *date_candidates
            )

            if not d:
                continue

            columns = self.cols(table)

            select = [

                f"{self.ident(d)} AS event_date",

                f"'{label}' AS operation_type",

                "id AS source_id"

            ]

            # Disease relation
            disease_fk = self.pick(
                table,
                "disease_id"
            )

            if disease_fk:
                select.append(
                    f"{self.ident(disease_fk)} AS disease_id"
                )
            else:
                select.append(
                    "NULL AS disease_id"
                )

            # Sample relation
            sample_fk = self.pick(
                table,
                "sample_id",
                "send_sample_id",
                "sample_detail_id"
            )

            if sample_fk:
                select.append(
                    f"{self.ident(sample_fk)} AS sample_id"
                )
            else:
                select.append(
                    "NULL AS sample_id"
                )

            # Laboratory relation
            lab_fk = self.pick(
                table,
                "laboratory_result_id",
                "lab_result_id"
            )

            if lab_fk:
                select.append(
                    f"{self.ident(lab_fk)} AS laboratory_result_id"
                )
            else:
                select.append(
                    "NULL AS laboratory_result_id"
                )

            # Result status
            result_col = self.pick(
                table,
                "result_status",
                "status",
                "result",
                "result_value"
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

            # Animal count
            animal_col = self.pick(
                table,
                "animal_count",
                "animals_count",
                "total_animals",
                "vaccinated_animals",
                "eligible_animals"
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

            sql = f"""
                SELECT
                    {', '.join(select)}
                FROM {self.ident(table)}
                WHERE
                    {self.ident(unit_fk)}=:uid
                    AND
                    {self.ident(d)} IS NOT NULL
            """

            try:

                rows = self.rows(
                    sql,
                    {"uid": unit_id}
                )

                result.extend(rows)

            except Exception:
                # One malformed optional source table must not kill
                # the complete dashboard.
                continue

        result.sort(
            key=lambda x:
                str(x.get("event_date") or ""),
            reverse=True
        )

        return result[:2000]

    # ---------------------------------------------------------
    # Related operation chain
    # ---------------------------------------------------------

    def related_chain(
        self,
        unit_id: int,
        operation_id: int | None = None
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
            key=lambda x:
                str(x.get("event_date") or "")
        )

        return chain