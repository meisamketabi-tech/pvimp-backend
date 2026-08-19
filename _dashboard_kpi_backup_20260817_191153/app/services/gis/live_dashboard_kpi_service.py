from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class LiveDashboardKPIService:
    """
    Live GIS Dashboard KPI service.

    All KPI values are calculated directly from PostgreSQL.
    No snapshot or cache of KPI values is used.
    """

    _tables_cache: set[str] | None = None
    _columns_cache: dict[str, set[str]] = {}

    def __init__(self, db: Session):
        self.db = db

    # =========================================================
    # Schema helpers
    # =========================================================

    def _tables(self) -> set[str]:
        if self.__class__._tables_cache is None:
            rows = self.db.execute(text("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                      AND table_type = 'BASE TABLE'
                    """)).mappings().all()

            self.__class__._tables_cache = {str(row["table_name"]) for row in rows}

        return self.__class__._tables_cache

    def has_table(self, table: str) -> bool:
        return table in self._tables()

    def cols(self, table: str) -> set[str]:
        if table in self.__class__._columns_cache:
            return self.__class__._columns_cache[table]

        if not self.has_table(table):
            return set()

        rows = (
            self.db.execute(
                text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = :table_name
                """),
                {"table_name": table},
            )
            .mappings()
            .all()
        )

        result = {str(row["column_name"]) for row in rows}

        self.__class__._columns_cache[table] = result

        return result

    def pick(
        self,
        table: str,
        *candidates: str,
    ) -> str | None:
        columns = self.cols(table)

        for candidate in candidates:
            if candidate in columns:
                return candidate

        return None

    @staticmethod
    def ident(value: str) -> str:
        """
        Safely quote an SQL identifier.

        Identifiers are accepted only from information_schema
        or hard-coded candidate names.
        """
        if not value or not value.replace("_", "").isalnum():
            raise ValueError(f"Unsafe SQL identifier: {value}")

        return f'"{value}"'

    # =========================================================
    # Generic SQL helpers
    # =========================================================

    def _scalar(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        default: Any = 0,
    ) -> Any:
        value = self.db.execute(
            text(sql),
            params or {},
        ).scalar()

        if value is None:
            return default

        if isinstance(value, Decimal):
            return float(value)

        return value

    def _rows(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        rows = (
            self.db.execute(
                text(sql),
                params or {},
            )
            .mappings()
            .all()
        )

        return [dict(row) for row in rows]

    @staticmethod
    def _jsonable(value: Any) -> Any:
        if isinstance(value, (datetime, date)):
            return value.isoformat()

        if isinstance(value, Decimal):
            return float(value)

        return value

    def _clean(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {key: self._clean(item) for key, item in value.items()}

        if isinstance(value, list):
            return [self._clean(item) for item in value]

        return self._jsonable(value)

    # =========================================================
    # Generic aggregation
    # =========================================================

    def count(
        self,
        table: str,
        where: str = "TRUE",
        params: dict[str, Any] | None = None,
    ) -> int:
        if not self.has_table(table):
            return 0

        return int(
            self._scalar(
                f"""
                SELECT COUNT(*)
                FROM {self.ident(table)}
                WHERE {where}
                """,
                params,
                0,
            )
        )

    def sum_col(
        self,
        table: str,
        column: str | None,
        where: str = "TRUE",
        params: dict[str, Any] | None = None,
    ) -> float:
        if not column or not self.has_table(table) or column not in self.cols(table):
            return 0.0

        return float(
            self._scalar(
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
        )

    def date_col(
        self,
        table: str,
        candidates: tuple[str, ...],
    ) -> str | None:
        return self.pick(table, *candidates)

    def _period_where(
        self,
        table: str,
        start: date | None,
        end: date | None,
    ) -> tuple[str, dict[str, Any]]:
        column = self.date_col(
            table,
            (
                "operation_date",
                "vaccination_date",
                "care_date",
                "report_date",
                "occurrence_date",
                "sampling_date",
                "sample_date",
                "answer_date",
                "spraying_date",
                "disposal_date",
                "distribution_date",
                "event_date",
                "start_date",
                "created_at",
                "date",
                "inspection_date",
            ),
        )

        if not column:
            return "TRUE", {}

        conditions: list[str] = []
        params: dict[str, Any] = {}

        if start:
            conditions.append(f"{self.ident(column)} >= :p_start")
            params["p_start"] = start

        if end:
            conditions.append(f"{self.ident(column)} < :p_end")
            params["p_end"] = end

        if not conditions:
            return "TRUE", params

        return " AND ".join(conditions), params

    # =========================================================
    # Overview
    # =========================================================

    def overview(
        self,
        start: date | None = None,
        end: date | None = None,
    ) -> dict[str, Any]:

        units = "gis_epidemiology_units"

        active_column = self.pick(
            units,
            "is_active",
            "active",
        )

        unit_where = (
            "TRUE" if not active_column else f"{self.ident(active_column)} = TRUE"
        )

        total_units = self.count(units)
        active_units = self.count(
            units,
            unit_where,
        )

        # -----------------------------------------------------
        # Livestock
        # -----------------------------------------------------

        livestock_columns = [
            self.pick(units, "sheep_count"),
            self.pick(units, "cattle_count"),
            self.pick(units, "goat_count"),
            self.pick(units, "horse_count"),
            self.pick(units, "dog_count"),
            self.pick(units, "camel_count"),
            self.pick(units, "buffalo_count"),
        ]

        livestock_columns = [column for column in livestock_columns if column]

        total_livestock = 0.0

        if livestock_columns:
            expression = " + ".join(
                f"COALESCE({self.ident(column)}, 0)" for column in livestock_columns
            )

            total_livestock = float(
                self._scalar(
                    f"""
                    SELECT COALESCE(
                        SUM({expression}),
                        0
                    )
                    FROM {self.ident(units)}
                    """,
                    {},
                    0,
                )
            )

        # -----------------------------------------------------
        # Disease
        # -----------------------------------------------------

        disease_reports = self.count("gis_disease_reports")

        disease_occurrences = self.count("gis_disease_occurrences")

        diseases = self.count("gis_diseases")

        active_outbreaks = 0

        if self.has_table("gis_outbreaks"):
            status_column = self.pick(
                "gis_outbreaks",
                "status",
            )

            if status_column:
                active_outbreaks = self.count(
                    "gis_outbreaks",
                    f"""
                    LOWER(
                        COALESCE(
                            {self.ident(status_column)},
                            ''
                        )
                    ) IN (
                        'active',
                        'open',
                        'ongoing'
                    )
                    """,
                )
            else:
                active_outbreaks = self.count("gis_outbreaks")

        # -----------------------------------------------------
        # Active care
        # -----------------------------------------------------

        care_table = "gis_enable_cares"

        care_total = self.count(care_table)

        care_animals = self.sum_col(
            care_table,
            self.pick(
                care_table,
                "total_animals",
                "animal_count",
                "animals_count",
            ),
        )

        care_positive = self.sum_col(
            care_table,
            self.pick(
                care_table,
                "positive_count",
                "positive",
            ),
        )

        care_negative = self.sum_col(
            care_table,
            self.pick(
                care_table,
                "negative_count",
                "negative",
            ),
        )

        care_suspicious = self.sum_col(
            care_table,
            self.pick(
                care_table,
                "suspicious_count",
                "suspect_count",
                "suspected_count",
            ),
        )

        care_positive_rate = (
            round(
                care_positive / care_animals * 100,
                2,
            )
            if care_animals
            else 0
        )

        # -----------------------------------------------------
        # Vaccination
        # -----------------------------------------------------

        vaccination_table = "gis_vaccination_performances"

        vaccinated_column = self.pick(
            vaccination_table,
            "vaccinated_animals",
            "vaccinated_count",
            "performed_count",
        )

        eligible_column = self.pick(
            vaccination_table,
            "eligible_animals",
            "eligible_count",
            "target_animals",
            "planned_animals",
        )

        vaccinated = self.sum_col(
            vaccination_table,
            vaccinated_column,
        )

        eligible = self.sum_col(
            vaccination_table,
            eligible_column,
        )

        vaccination_coverage = (
            round(
                vaccinated / eligible * 100,
                2,
            )
            if eligible
            else 0
        )

        vaccination_remaining = max(
            eligible - vaccinated,
            0,
        )

        # -----------------------------------------------------
        # Laboratory / samples
        # -----------------------------------------------------

        laboratory_table = "gis_laboratory_results"
        sample_table = "gis_send_sample_details"

        lab_results = self.count(laboratory_table)

        lab_samples = self.sum_col(
            laboratory_table,
            self.pick(
                laboratory_table,
                "sample_count",
                "samples_count",
            ),
        )

        sent_samples = self.sum_col(
            sample_table,
            self.pick(
                sample_table,
                "sample_count",
                "samples_count",
            ),
        )

        lab_status_column = self.pick(
            laboratory_table,
            "result_status",
            "status",
            "result",
        )

        lab_positive = 0

        if lab_status_column:
            lab_positive = self.count(
                laboratory_table,
                f"""
                LOWER(
                    COALESCE(
                        {self.ident(lab_status_column)},
                        ''
                    )
                ) LIKE '%positive%'
                OR
                LOWER(
                    COALESCE(
                        {self.ident(lab_status_column)},
                        ''
                    )
                ) LIKE '%مثبت%'
                """,
            )

        lab_positive_rate = (
            round(
                lab_positive / lab_results * 100,
                2,
            )
            if lab_results
            else 0
        )

        # -----------------------------------------------------
        # Vaccine inventory / logistics
        # -----------------------------------------------------

        inventory_table = "gis_vaccine_inventories"
        distribution_table = "gis_vaccine_distributions"
        disposal_table = "gis_vaccine_disposals"

        inventory_packages = self.sum_col(
            inventory_table,
            self.pick(
                inventory_table,
                "package_count",
                "packages_count",
                "quantity",
                "stock_quantity",
            ),
        )

        distributed_packages = self.sum_col(
            distribution_table,
            self.pick(
                distribution_table,
                "package_count",
                "packages_count",
                "quantity",
            ),
        )

        disposed_packages = self.sum_col(
            disposal_table,
            self.pick(
                disposal_table,
                "package_count",
                "packages_count",
                "quantity",
            ),
        )

        expiring_30_days = 0

        expiration_column = self.pick(
            inventory_table,
            "expiration_date",
            "expiry_date",
            "expire_date",
        )

        if expiration_column:
            expiring_30_days = self.count(
                inventory_table,
                f"""
                {self.ident(expiration_column)} IS NOT NULL
                AND
                {self.ident(expiration_column)}
                    <= CURRENT_DATE + INTERVAL '30 days'
                """,
            )

        # -----------------------------------------------------
        # Time series
        # -----------------------------------------------------

        vaccination_series = self.monthly_series(
            vaccination_table,
            vaccinated_column,
            (
                "vaccination_date",
                "operation_date",
                "date",
            ),
            "vaccination",
            start=start,
            end=end,
        )

        disease_series = self.monthly_count_series(
            "gis_disease_reports",
            (
                "report_date",
                "occurrence_date",
                "created_at",
                "date",
            ),
            "reports",
            start=start,
            end=end,
        )

        care_series = self.monthly_sum_series(
            care_table,
            self.pick(
                care_table,
                "positive_count",
                "positive",
            ),
            (
                "care_date",
                "operation_date",
                "date",
            ),
            "positive",
            start=start,
            end=end,
        )

        # -----------------------------------------------------
        # Breakdowns
        # -----------------------------------------------------

        county_breakdown = self.vaccination_by_county(
            vaccination_table,
            vaccinated_column,
            eligible_column,
        )

        disease_breakdown = self.disease_breakdown(
            start=start,
            end=end,
        )

        return self._clean(
            {
                "generated_at": datetime.utcnow(),
                "live": True,
                "cards": {
                    "total_units": total_units,
                    "active_units": active_units,
                    "total_livestock": total_livestock,
                    "disease_reports": disease_reports,
                    "disease_occurrences": disease_occurrences,
                    "diseases": diseases,
                    "active_outbreaks": active_outbreaks,
                    "care_records": care_total,
                    "care_animals": care_animals,
                    "care_positive": care_positive,
                    "care_negative": care_negative,
                    "care_suspicious": care_suspicious,
                    "care_positive_rate": care_positive_rate,
                    "vaccinated_animals": vaccinated,
                    "eligible_animals": eligible,
                    "vaccination_coverage": vaccination_coverage,
                    "vaccination_remaining": vaccination_remaining,
                    "lab_results": lab_results,
                    "lab_samples": lab_samples,
                    "sent_samples": sent_samples,
                    "lab_positive": lab_positive,
                    "lab_positive_rate": lab_positive_rate,
                    "inventory_packages": inventory_packages,
                    "distributed_packages": distributed_packages,
                    "disposed_packages": disposed_packages,
                    "expiring_30_days": expiring_30_days,
                },
                "series": {
                    "vaccination": vaccination_series,
                    "disease_reports": disease_series,
                    "care_positive": care_series,
                },
                "breakdowns": {
                    "vaccination_by_county": county_breakdown,
                    "disease_by_name": disease_breakdown,
                },
                "scopes": {
                    "prediction_scope": "county",
                    "unit_drilldown": True,
                },
            }
        )

    # =========================================================
    # Time series
    # =========================================================

    def _series_where(
        self,
        column: str,
        start: date | None,
        end: date | None,
    ) -> tuple[str, dict[str, Any]]:
        conditions = [f"{self.ident(column)} IS NOT NULL"]

        params: dict[str, Any] = {}

        if start:
            conditions.append(f"{self.ident(column)} >= :series_start")
            params["series_start"] = start

        if end:
            conditions.append(f"{self.ident(column)} < :series_end")
            params["series_end"] = end

        return " AND ".join(conditions), params

    def monthly_count_series(
        self,
        table: str,
        date_candidates: tuple[str, ...],
        label: str,
        start: date | None = None,
        end: date | None = None,
    ) -> list[dict[str, Any]]:

        if not self.has_table(table):
            return []

        date_column = self.pick(
            table,
            *date_candidates,
        )

        if not date_column:
            return []

        where, params = self._series_where(
            date_column,
            start,
            end,
        )

        rows = self._rows(
            f"""
            SELECT
                TO_CHAR(
                    DATE_TRUNC(
                        'month',
                        {self.ident(date_column)}
                    ),
                    'YYYY-MM'
                ) AS period,
                COUNT(*)::numeric AS value
            FROM {self.ident(table)}
            WHERE {where}
            GROUP BY 1
            ORDER BY 1
            """,
            params,
        )

        return [
            {
                "period": row["period"],
                "value": float(row["value"]),
                "label": label,
            }
            for row in rows
        ]

    def monthly_sum_series(
        self,
        table: str,
        value_column: str | None,
        date_candidates: tuple[str, ...],
        label: str,
        start: date | None = None,
        end: date | None = None,
    ) -> list[dict[str, Any]]:

        if not value_column or not self.has_table(table):
            return []

        date_column = self.pick(
            table,
            *date_candidates,
        )

        if not date_column:
            return []

        where, params = self._series_where(
            date_column,
            start,
            end,
        )

        rows = self._rows(
            f"""
            SELECT
                TO_CHAR(
                    DATE_TRUNC(
                        'month',
                        {self.ident(date_column)}
                    ),
                    'YYYY-MM'
                ) AS period,
                COALESCE(
                    SUM({self.ident(value_column)}),
                    0
                )::numeric AS value
            FROM {self.ident(table)}
            WHERE {where}
            GROUP BY 1
            ORDER BY 1
            """,
            params,
        )

        return [
            {
                "period": row["period"],
                "value": float(row["value"]),
                "label": label,
            }
            for row in rows
        ]

    def monthly_series(
        self,
        table: str,
        value_column: str | None,
        date_candidates: tuple[str, ...],
        label: str,
        start: date | None = None,
        end: date | None = None,
    ) -> list[dict[str, Any]]:
        return self.monthly_sum_series(
            table,
            value_column,
            date_candidates,
            label,
            start=start,
            end=end,
        )

    # =========================================================
    # Disease breakdown
    # =========================================================

    def disease_breakdown(
        self,
        start: date | None = None,
        end: date | None = None,
    ) -> list[dict[str, Any]]:

        table = "gis_disease_reports"

        if not self.has_table(table):
            return []

        disease_id = self.pick(
            table,
            "disease_id",
        )

        if not disease_id:
            return []

        date_column = self.pick(
            table,
            "report_date",
            "occurrence_date",
            "created_at",
            "date",
        )

        where = "TRUE"
        params: dict[str, Any] = {}

        if date_column:
            where, params = self._series_where(
                date_column,
                start,
                end,
            )

        if self.has_table("gis_diseases"):
            disease_name = self.pick(
                "gis_diseases",
                "name_fa",
                "name",
                "title",
                "disease_name",
                "label",
            )

            if disease_name:
                rows = self._rows(
                    f"""
                    SELECT
                        d.{self.ident(disease_name)} AS name,
                        COUNT(r.id)::numeric AS value
                    FROM {self.ident(table)} r
                    LEFT JOIN gis_diseases d
                        ON d.id = r.{self.ident(disease_id)}
                    WHERE {where}
                    GROUP BY d.{self.ident(disease_name)}
                    ORDER BY value DESC
                    LIMIT 10
                    """,
                    params,
                )

                return [
                    {
                        "name": row["name"] or "بدون نام",
                        "value": float(row["value"]),
                    }
                    for row in rows
                ]

        rows = self._rows(
            f"""
            SELECT
                CAST(
                    {self.ident(disease_id)}
                    AS text
                ) AS name,
                COUNT(*)::numeric AS value
            FROM {self.ident(table)}
            WHERE {where}
            GROUP BY 1
            ORDER BY value DESC
            LIMIT 10
            """,
            params,
        )

        return [
            {
                "name": row["name"],
                "value": float(row["value"]),
            }
            for row in rows
        ]

    # =========================================================
    # Vaccination by county
    # =========================================================

    def vaccination_by_county(
        self,
        table: str,
        vaccinated_column: str | None,
        eligible_column: str | None,
    ) -> list[dict[str, Any]]:

        if not self.has_table(table) or not vaccinated_column:
            return []

        county_column = self.pick(
            table,
            "county_id",
        )

        unit_column = self.pick(
            table,
            "epidemiology_unit_id",
        )

        if not county_column and not unit_column:
            return []

        if unit_column and self.has_table("gis_epidemiology_units"):
            unit_county_column = self.pick(
                "gis_epidemiology_units",
                "county_id",
            )

            if not unit_county_column:
                return []

            county_name = None

            if self.has_table("gis_counties"):
                county_name = self.pick(
                    "gis_counties",
                    "name_fa",
                    "name",
                    "title",
                    "county_name",
                    "label",
                )

            if county_name:
                name_sql = f"c.{self.ident(county_name)}"

                join_sql = """
                LEFT JOIN gis_counties c
                    ON c.id = u."county_id"
                """
            else:
                name_sql = f"CAST(" f"u.{self.ident(unit_county_column)}" f" AS text)"
                join_sql = ""

            eligible_expression = (
                f"SUM(p.{self.ident(eligible_column)})" if eligible_column else "0"
            )

            rows = self._rows(f"""
                SELECT
                    {name_sql} AS name,
                    COALESCE(
                        SUM(
                            p.{self.ident(vaccinated_column)}
                        ),
                        0
                    )::numeric AS vaccinated,
                    COALESCE(
                        {eligible_expression},
                        0
                    )::numeric AS eligible
                FROM {self.ident(table)} p
                JOIN gis_epidemiology_units u
                    ON u.id = p.{self.ident(unit_column)}
                {join_sql}
                GROUP BY {name_sql}
                ORDER BY vaccinated DESC
                LIMIT 12
                """)

            result = []

            for row in rows:
                vaccinated = float(row["vaccinated"] or 0)

                eligible = float(row["eligible"] or 0)

                result.append(
                    {
                        "name": (row["name"] or "بدون نام"),
                        "vaccinated": vaccinated,
                        "eligible": eligible,
                        "coverage": (
                            round(
                                vaccinated / eligible * 100,
                                2,
                            )
                            if eligible
                            else 0
                        ),
                    }
                )

            return result

        return []

    # =========================================================
    # Unit detail
    # =========================================================

    def unit_detail(
        self,
        unit_id: int,
    ) -> dict[str, Any]:

        table = "gis_epidemiology_units"

        if not self.has_table(table):
            return {
                "unit": None,
                "error": "gis_epidemiology_units not found",
            }

        name_column = self.pick(
            table,
            "unit_name",
            "name",
            "title",
            "name_fa",
            "unit_title",
        )

        province_column = self.pick(
            table,
            "province_id",
        )

        county_column = self.pick(
            table,
            "county_id",
        )

        unit_type_column = self.pick(
            table,
            "unit_type_id",
        )

        select_parts = ["u.id"]

        if name_column:
            select_parts.append(f"u.{self.ident(name_column)} AS unit_name")

        if province_column:
            select_parts.append(f"u.{self.ident(province_column)} AS province_id")

        if county_column:
            select_parts.append(f"u.{self.ident(county_column)} AS county_id")

        if unit_type_column:
            select_parts.append(f"u.{self.ident(unit_type_column)} AS unit_type_id")

        rows = self._rows(
            f"""
            SELECT {", ".join(select_parts)}
            FROM gis_epidemiology_units u
            WHERE u.id = :unit_id
            """,
            {"unit_id": unit_id},
        )

        if not rows:
            return {
                "unit": None,
                "error": "واحد پیدا نشد",
            }

        unit = rows[0]

        vaccination_table = "gis_vaccination_performances"

        unit_fk = self.pick(
            vaccination_table,
            "epidemiology_unit_id",
        )

        vaccinated_column = self.pick(
            vaccination_table,
            "vaccinated_animals",
            "vaccinated_count",
            "performed_count",
        )

        eligible_column = self.pick(
            vaccination_table,
            "eligible_animals",
            "eligible_count",
            "target_animals",
            "planned_animals",
        )

        if unit_fk:
            where = f"{self.ident(unit_fk)} = :unit_id"

            vaccinated_total = self.sum_col(
                vaccination_table,
                vaccinated_column,
                where,
                {"unit_id": unit_id},
            )

            eligible_total = self.sum_col(
                vaccination_table,
                eligible_column,
                where,
                {"unit_id": unit_id},
            )
        else:
            vaccinated_total = 0.0
            eligible_total = 0.0

        coverage = (
            round(
                vaccinated_total / eligible_total * 100,
                2,
            )
            if eligible_total
            else 0
        )

        operations = self.operation_history(unit_id)

        operation_counts: dict[str, int] = {}

        for operation in operations:
            operation_type = operation["operation_type"]

            operation_counts[operation_type] = (
                operation_counts.get(
                    operation_type,
                    0,
                )
                + 1
            )

        predictions = self.county_predictions(unit.get("county_id"))

        return self._clean(
            {
                "unit": unit,
                "vaccination": {
                    "eligible": eligible_total,
                    "vaccinated": vaccinated_total,
                    "remaining": max(
                        eligible_total - vaccinated_total,
                        0,
                    ),
                    "coverage_percent": coverage,
                    "target_source": ("unit eligible_animals"),
                },
                "county_predictions": predictions,
                "operation_history": operations,
                "operation_counts": [
                    {
                        "name": key,
                        "value": value,
                    }
                    for key, value in sorted(
                        operation_counts.items(),
                        key=lambda item: -item[1],
                    )
                ],
            }
        )

    # =========================================================
    # County predictions
    # =========================================================

    def county_predictions(
        self,
        county_id: int | None,
    ) -> list[dict[str, Any]]:

        table = "gis_vaccination_predictions"

        if not self.has_table(table) or county_id is None:
            return []

        county_column = self.pick(
            table,
            "county_id",
        )

        value_column = self.pick(
            table,
            "prediction_value",
            "predicted_value",
            "target_value",
            "value",
        )

        year_column = self.pick(
            table,
            "prediction_year",
            "year",
        )

        category_column = self.pick(
            table,
            "prediction_category",
            "category",
        )

        if not county_column or not value_column:
            return []

        select_parts = [f"{self.ident(value_column)} AS value"]

        if year_column:
            select_parts.append(f"{self.ident(year_column)} AS year")

        if category_column:
            select_parts.append(f"{self.ident(category_column)} AS category")

        order_sql = f"{self.ident(year_column)} DESC" if year_column else "1"

        return self._rows(
            f"""
            SELECT {", ".join(select_parts)}
            FROM {self.ident(table)}
            WHERE {self.ident(county_column)} = :county_id
            ORDER BY {order_sql}
            """,
            {"county_id": county_id},
        )

    # =========================================================
    # Operation history
    # =========================================================

    def operation_history(
        self,
        unit_id: int,
    ) -> list[dict[str, Any]]:

        specs = [
            (
                "gis_enable_cares",
                "care_date",
                "مراقبت",
            ),
            (
                "gis_vaccination_performances",
                "vaccination_date",
                "واکسیناسیون",
            ),
            (
                "gis_laboratory_results",
                "sampling_date",
                "آزمایشگاه",
            ),
            (
                "gis_send_sample_details",
                "sampling_date",
                "ارسال نمونه",
            ),
            (
                "gis_slaughter_disposals",
                "disposal_date",
                "کشتار/امحاء",
            ),
            (
                "gis_spraying",
                "spraying_date",
                "سمپاشی",
            ),
            (
                "gis_vaccine_distributions",
                "distribution_date",
                "توزیع واکسن",
            ),
            (
                "gis_vaccine_disposals",
                "disposal_date",
                "دفع واکسن",
            ),
            (
                "gis_disease_reports",
                "report_date",
                "گزارش بیماری",
            ),
            (
                "gis_disease_occurrences",
                "occurrence_date",
                "وقوع بیماری",
            ),
        ]

        union_parts: list[str] = []

        for table, preferred_date, label in specs:

            if not self.has_table(table):
                continue

            foreign_key = self.pick(
                table,
                "epidemiology_unit_id",
            )

            if not foreign_key:
                continue

            date_column = self.pick(
                table,
                preferred_date,
                "operation_date",
                "date",
                "created_at",
                "event_date",
            )

            if not date_column:
                continue

            union_parts.append(f"""
                SELECT
                    {self.ident(date_column)}
                        AS event_date,
                    :operation_label_{len(union_parts)}
                        AS operation_type
                FROM {self.ident(table)}
                WHERE
                    {self.ident(foreign_key)}
                    = :unit_id
                    AND
                    {self.ident(date_column)}
                    IS NOT NULL
                """)

        if not union_parts:
            return []

        params: dict[str, Any] = {"unit_id": unit_id}

        for index, (_, _, label) in enumerate(specs):
            if index < len(union_parts):
                params[f"operation_label_{index}"] = label

        sql = " UNION ALL ".join(union_parts) + """
            ORDER BY event_date DESC
            LIMIT 500
            """

        return self._rows(
            sql,
            params,
        )

    # =========================================================
    # County detail
    # =========================================================

    def county_detail(
        self,
        county_id: int,
    ) -> dict[str, Any]:

        table = "gis_epidemiology_units"

        if not self.has_table(table):
            return {"units": []}

        county_column = self.pick(
            table,
            "county_id",
        )

        name_column = self.pick(
            table,
            "unit_name",
            "name",
            "title",
            "name_fa",
            "unit_title",
        )

        if not county_column:
            return {"units": []}

        name_sql = (
            f"u.{self.ident(name_column)}" if name_column else "CAST(u.id AS text)"
        )

        rows = self._rows(
            f"""
            SELECT
                u.id,
                {name_sql} AS name
            FROM gis_epidemiology_units u
            WHERE
                u.{self.ident(county_column)}
                = :county_id
            ORDER BY name
            """,
            {"county_id": county_id},
        )

        result = []

        for row in rows:
            detail = self.unit_detail(int(row["id"]))

            vaccination = detail.get(
                "vaccination",
                {},
            )

            result.append(
                {
                    "id": row["id"],
                    "name": (row["name"] or "بدون نام"),
                    "eligible": vaccination.get(
                        "eligible",
                        0,
                    ),
                    "vaccinated": vaccination.get(
                        "vaccinated",
                        0,
                    ),
                    "remaining": vaccination.get(
                        "remaining",
                        0,
                    ),
                    "coverage": vaccination.get(
                        "coverage_percent",
                        0,
                    ),
                    "operations": len(
                        detail.get(
                            "operation_history",
                            [],
                        )
                    ),
                }
            )

        return {
            "county_id": county_id,
            "units": result,
        }

    # =========================================================
    # KPI drilldown
    # =========================================================

    def metric_units(
        self,
        metric: str,
    ) -> list[dict[str, Any]]:

        table = "gis_epidemiology_units"

        if not self.has_table(table):
            return []

        name_column = self.pick(
            table,
            "unit_name",
            "name",
            "title",
            "name_fa",
            "unit_title",
        )

        county_column = self.pick(
            table,
            "county_id",
        )

        province_column = self.pick(
            table,
            "province_id",
        )

        name_sql = (
            f"u.{self.ident(name_column)}" if name_column else "CAST(u.id AS text)"
        )

        base_columns = [
            "u.id AS unit_id",
            f"{name_sql} AS unit_name",
        ]

        if county_column:
            base_columns.append(f"u.{self.ident(county_column)} AS county_id")

        if province_column:
            base_columns.append(f"u.{self.ident(province_column)} AS province_id")

        group_columns = [
            "u.id",
            name_sql,
        ]

        if county_column:
            group_columns.append(f"u.{self.ident(county_column)}")

        if province_column:
            group_columns.append(f"u.{self.ident(province_column)}")

        # -----------------------------------------------------
        # Vaccination
        # -----------------------------------------------------

        if metric == "vaccination" and self.has_table("gis_vaccination_performances"):
            vaccination_table = "gis_vaccination_performances"

            foreign_key = self.pick(
                vaccination_table,
                "epidemiology_unit_id",
            )

            vaccinated_column = self.pick(
                vaccination_table,
                "vaccinated_animals",
                "vaccinated_count",
                "performed_count",
            )

            eligible_column = self.pick(
                vaccination_table,
                "eligible_animals",
                "eligible_count",
                "target_animals",
                "planned_animals",
            )

            if foreign_key and vaccinated_column:

                target_expression = (
                    f"""
                    COALESCE(
                        SUM(
                            p.{self.ident(eligible_column)}
                        ),
                        0
                    )
                    """
                    if eligible_column
                    else "0"
                )

                rows = self._rows(f"""
                    SELECT
                        {", ".join(base_columns)},
                        COALESCE(
                            SUM(
                                p.{self.ident(vaccinated_column)}
                            ),
                            0
                        )::numeric AS value,
                        {target_expression}::numeric AS target
                    FROM gis_epidemiology_units u
                    LEFT JOIN
                        gis_vaccination_performances p
                    ON
                        p.{self.ident(foreign_key)}
                        = u.id
                    GROUP BY
                        {", ".join(group_columns)}
                    ORDER BY value DESC
                    """)

                for row in rows:
                    value = float(row["value"] or 0)

                    target = float(row["target"] or 0)

                    row["progress_percent"] = (
                        round(
                            value / target * 100,
                            2,
                        )
                        if target
                        else 0
                    )

                return rows

        # -----------------------------------------------------
        # Count based metrics
        # -----------------------------------------------------

        metric_specs = {
            "disease_reports": (
                "gis_disease_reports",
                "report_date",
            ),
            "care": (
                "gis_enable_cares",
                "care_date",
            ),
            "lab": (
                "gis_laboratory_results",
                "sampling_date",
            ),
            "samples": (
                "gis_send_sample_details",
                "sampling_date",
            ),
            "spraying": (
                "gis_spraying",
                "spraying_date",
            ),
            "operations": (
                "gis_operation_history",
                "operation_date",
            ),
        }

        if metric in metric_specs:
            source_table, preferred_date = metric_specs[metric]

            if self.has_table(source_table):
                foreign_key = self.pick(
                    source_table,
                    "epidemiology_unit_id",
                )

                date_column = self.pick(
                    source_table,
                    preferred_date,
                    "operation_date",
                    "date",
                    "created_at",
                    "event_date",
                )

                if foreign_key:
                    rows = self._rows(f"""
                        SELECT
                            {", ".join(base_columns)},
                            COUNT(x.id)::numeric AS value
                        FROM gis_epidemiology_units u
                        LEFT JOIN
                            {self.ident(source_table)} x
                        ON
                            x.{self.ident(foreign_key)}
                            = u.id
                        GROUP BY
                            {", ".join(group_columns)}
                        ORDER BY value DESC
                        """)

                    return rows

        # -----------------------------------------------------
        # All live operations
        # -----------------------------------------------------

        rows = []

        for point in self.map_points():
            unit_id = int(point["id"])

            history = self.operation_history(unit_id)

            rows.append(
                {
                    "unit_id": unit_id,
                    "unit_name": point.get("name"),
                    "county_id": point.get("county_id"),
                    "province_id": point.get("province_id"),
                    "value": len(history),
                }
            )

        rows.sort(
            key=lambda item: item["value"],
            reverse=True,
        )

        return rows

    # =========================================================
    # Map
    # =========================================================

    def map_points(
        self,
    ) -> list[dict[str, Any]]:

        table = "gis_epidemiology_units"

        if not self.has_table(table):
            return []

        latitude = self.pick(
            table,
            "latitude",
            "lat",
        )

        longitude = self.pick(
            table,
            "longitude",
            "lon",
            "lng",
        )

        name_column = self.pick(
            table,
            "unit_name",
            "name",
            "title",
            "name_fa",
            "unit_title",
        )

        county_column = self.pick(
            table,
            "county_id",
        )

        province_column = self.pick(
            table,
            "province_id",
        )

        if not latitude or not longitude:
            return []

        name_sql = self.ident(name_column) if name_column else "CAST(id AS text)"

        county_sql = self.ident(county_column) if county_column else "NULL"

        province_sql = self.ident(province_column) if province_column else "NULL"

        return self._rows(f"""
            SELECT
                id,
                {name_sql} AS name,
                {self.ident(latitude)} AS latitude,
                {self.ident(longitude)} AS longitude,
                {county_sql} AS county_id,
                {province_sql} AS province_id
            FROM {self.ident(table)}
            WHERE
                {self.ident(latitude)} IS NOT NULL
                AND
                {self.ident(longitude)} IS NOT NULL
            LIMIT 20000
            """)
