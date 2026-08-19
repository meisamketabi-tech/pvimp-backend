from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class LiveDashboardKPIService:
    """
    Live KPI service for the GIS dashboard.

    Important vaccination rule
    ---------------------------
    The column `eligible_animals` in the current vaccination-performance
    dataset is not usable as the vaccination denominator because it is zero
    in the current imported data.

    Therefore vaccination coverage is calculated from the livestock population
    stored in `gis_epidemiology_units`.

    Animal grouping rules:

        گاو
        گاو و گوساله
            -> cattle_count

        گوسفند
            -> sheep_count

        بز
            -> goat_count

        گوسفند و بز
        بره و بزغاله
            -> sheep_count + goat_count

        سگ صاحبدار
        سگ بدون صاحب
            -> dog_count

        اسب
            -> horse_count

        شتر
            -> camel_count

        گاومیش
            -> buffalo_count

    Animals for which the master population is not currently available
    (for example الاغ / قاطر) are kept in vaccination statistics, but
    population coverage is not calculated for them.

    All KPIs are live and are calculated directly from PostgreSQL.
    No KPI snapshot/cache is used.
    """

    _tables_cache: set[str] | None = None
    _columns_cache: dict[str, set[str]] = {}

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------
    # Schema helpers
    # ------------------------------------------------------------------

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
        Safely quote a PostgreSQL identifier.

        Identifiers are only accepted from:
        - information_schema
        - hard-coded application values
        """
        if not value.replace("_", "").isalnum():
            raise ValueError(f"Unsafe identifier: {value}")

        return '"' + value + '"'

    # ------------------------------------------------------------------
    # SQL helpers
    # ------------------------------------------------------------------

    def _scalar(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        default: Any = 0,
    ):
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
        return [
            dict(row)
            for row in self.db.execute(
                text(sql),
                params or {},
            )
            .mappings()
            .all()
        ]

    @staticmethod
    def _jsonable(value: Any):
        if isinstance(value, (datetime, date)):
            return value.isoformat()

        if isinstance(value, Decimal):
            return float(value)

        return value

    def _clean(self, obj: Any):
        if isinstance(obj, dict):
            return {key: self._clean(value) for key, value in obj.items()}

        if isinstance(obj, list):
            return [self._clean(value) for value in obj]

        return self._jsonable(obj)

    # ------------------------------------------------------------------
    # Generic aggregation helpers
    # ------------------------------------------------------------------

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
        col: str | None,
        where: str = "TRUE",
        params: dict[str, Any] | None = None,
    ) -> float:
        if not col or not self.has_table(table) or col not in self.cols(table):
            return 0.0

        return float(
            self._scalar(
                f"""
                SELECT COALESCE(
                    SUM({self.ident(col)}),
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
    ):
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

        parts: list[str] = []
        params: dict[str, Any] = {}

        if start:
            parts.append(f"{self.ident(column)} >= :p_start")
            params["p_start"] = start

        if end:
            parts.append(f"{self.ident(column)} < :p_end")
            params["p_end"] = end

        if not parts:
            return "TRUE", {}

        return " AND ".join(parts), params

    # ------------------------------------------------------------------
    # Vaccination population mapping
    # ------------------------------------------------------------------

    @staticmethod
    def _normalise_animal_type(value: Any) -> str:
        """
        Normalize animal type strings only for KPI grouping.
        Original database values remain untouched.
        """
        if value is None:
            return ""

        value = str(value).strip()

        replacements = {
            "ي": "ی",
            "ك": "ک",
            "\u200c": " ",
        }

        for old, new in replacements.items():
            value = value.replace(old, new)

        return " ".join(value.split())

    @classmethod
    def vaccination_animal_group(
        cls,
        animal_type: Any,
    ) -> str | None:
        """
        Convert source animal_type into a population group.

        This is intentionally conservative. We only return groups for which
        the master population exists in gis_epidemiology_units.
        """

        value = cls._normalise_animal_type(animal_type)

        if not value:
            return None

        # Combined sheep/goat categories
        if value == "گوسفند و بز" or value == "بره و بزغاله":
            return "گوسفند و بز"

        # Cattle + calf
        if value in {
            "گاو",
            "گاو و گوساله",
        }:
            return "گاو و گوساله"

        # Sheep
        if value == "گوسفند":
            return "گوسفند"

        # Goat
        if value == "بز":
            return "بز"

        # Dogs
        if value in {
            "سگ صاحبدار",
            "سگ بدون صاحب",
        }:
            return "سگ"

        # Horse
        if value == "اسب":
            return "اسب"

        # Camel
        if value in {
            "شتر",
            "شتر و بچه شتر",
        }:
            return "شتر"

        # Buffalo
        if value in {
            "گاومیش",
            "گاو میش",
        }:
            return "گاومیش"

        # No master population currently available
        return None

    @staticmethod
    def vaccination_population_sql(
        group: str,
        unit_alias: str = "u",
    ) -> str | None:
        """
        Return SQL expression for the master livestock population
        corresponding to a normalized animal group.
        """

        if group == "گاو و گوساله":
            return f"COALESCE({unit_alias}.cattle_count, 0)"

        if group == "گوسفند":
            return f"COALESCE({unit_alias}.sheep_count, 0)"

        if group == "بز":
            return f"COALESCE({unit_alias}.goat_count, 0)"

        if group == "گوسفند و بز":
            return (
                f"COALESCE({unit_alias}.sheep_count, 0) "
                f"+ COALESCE({unit_alias}.goat_count, 0)"
            )

        if group == "سگ":
            return f"COALESCE({unit_alias}.dog_count, 0)"

        if group == "اسب":
            return f"COALESCE({unit_alias}.horse_count, 0)"

        if group == "شتر":
            return f"COALESCE({unit_alias}.camel_count, 0)"

        if group == "گاومیش":
            return f"COALESCE({unit_alias}.buffalo_count, 0)"

        return None

    # ------------------------------------------------------------------
    # Vaccination KPI
    # ------------------------------------------------------------------

    def vaccination_kpi(
        self,
        vaccine_type: str | None = None,
        province_id: int | None = None,
        county_id: int | None = None,
        unit_id: int | None = None,
    ) -> dict[str, Any]:
        """
        Calculate vaccination coverage using master livestock population.

        Numerator:
            SUM(vaccinated_animals)

        Denominator:
            Master population from gis_epidemiology_units.

        Important:
            The denominator is calculated once per unit + animal group,
            so repeated vaccination rows cannot multiply the master
            population.
        """

        vp = "gis_vaccination_performances"
        units = "gis_epidemiology_units"

        if not self.has_table(vp):
            return {
                "vaccinated": 0,
                "population": 0,
                "coverage_percent": 0,
                "remaining": 0,
                "groups": [],
            }

        if not self.has_table(units):
            return {
                "vaccinated": 0,
                "population": 0,
                "coverage_percent": 0,
                "remaining": 0,
                "groups": [],
            }

        fk = self.pick(
            vp,
            "epidemiology_unit_id",
        )

        vaccinated_col = self.pick(
            vp,
            "vaccinated_animals",
            "vaccinated_count",
            "performed_count",
        )

        animal_col = self.pick(
            vp,
            "animal_type",
        )

        vaccine_col = self.pick(
            vp,
            "vaccine_type",
        )

        if not fk or not vaccinated_col or not animal_col:
            return {
                "vaccinated": 0,
                "population": 0,
                "coverage_percent": 0,
                "remaining": 0,
                "groups": [],
            }

        filters: list[str] = [f"v.{self.ident(fk)} IS NOT NULL"]

        params: dict[str, Any] = {}

        if vaccine_type and vaccine_col:
            filters.append(f"v.{self.ident(vaccine_col)} = :vaccine_type")
            params["vaccine_type"] = vaccine_type

        if unit_id is not None:
            filters.append(f"v.{self.ident(fk)} = :unit_id")
            params["unit_id"] = unit_id

        elif county_id is not None:
            filters.append(f"u.county_id = :county_id")
            params["county_id"] = county_id

        elif province_id is not None:
            filters.append(f"u.province_id = :province_id")
            params["province_id"] = province_id

        # Build source rows first.
        #
        # Each source row receives a normalized animal group.
        # Unsupported animals are excluded from population coverage.
        rows = self._rows(
            f"""
            SELECT
                v.{self.ident(fk)} AS unit_id,
                v.{self.ident(animal_col)} AS animal_type,
                COALESCE(
                    v.{self.ident(vaccinated_col)},
                    0
                )::numeric AS vaccinated
            FROM {self.ident(vp)} v
            JOIN {self.ident(units)} u
              ON u.id = v.{self.ident(fk)}
            WHERE {' AND '.join(filters)}
            """,
            params,
        )

        if not rows:
            return {
                "vaccinated": 0,
                "population": 0,
                "coverage_percent": 0,
                "remaining": 0,
                "groups": [],
            }

        # Group vaccination numerator by:
        # unit + normalized animal group
        #
        # This lets us later join one population value to each unit/group.
        unit_group_vaccinated: dict[
            tuple[int, str],
            float,
        ] = {}

        for row in rows:
            group = self.vaccination_animal_group(row["animal_type"])

            if not group:
                continue

            key = (
                int(row["unit_id"]),
                group,
            )

            unit_group_vaccinated[key] = unit_group_vaccinated.get(key, 0.0) + float(
                row["vaccinated"] or 0
            )

        if not unit_group_vaccinated:
            return {
                "vaccinated": 0,
                "population": 0,
                "coverage_percent": 0,
                "remaining": 0,
                "groups": [],
            }

        unit_ids = sorted({unit_id for unit_id, _ in unit_group_vaccinated})

        group_names = sorted({group for _, group in unit_group_vaccinated})

        population_rows: list[dict[str, Any]] = []

        # Query all required unit populations in one query.
        unit_rows = self._rows(
            f"""
            SELECT
                u.id,
                u.sheep_count,
                u.cattle_count,
                u.goat_count,
                u.horse_count,
                u.dog_count,
                u.camel_count,
                u.buffalo_count
            FROM {self.ident(units)} u
            WHERE u.id = ANY(:unit_ids)
            """,
            {"unit_ids": unit_ids},
        )

        population_by_key: dict[
            tuple[int, str],
            float,
        ] = {}

        for unit in unit_rows:
            unit_id_value = int(unit["id"])

            for group in group_names:
                expression = self.vaccination_population_sql(
                    group,
                    "u",
                )

                if not expression:
                    continue

                # Population is computed in Python from the already selected
                # master population columns. This avoids another SQL query
                # for every unit/group.
                if group == "گاو و گوساله":
                    population = float(unit["cattle_count"] or 0)

                elif group == "گوسفند":
                    population = float(unit["sheep_count"] or 0)

                elif group == "بز":
                    population = float(unit["goat_count"] or 0)

                elif group == "گوسفند و بز":
                    population = float(unit["sheep_count"] or 0) + float(
                        unit["goat_count"] or 0
                    )

                elif group == "سگ":
                    population = float(unit["dog_count"] or 0)

                elif group == "اسب":
                    population = float(unit["horse_count"] or 0)

                elif group == "شتر":
                    population = float(unit["camel_count"] or 0)

                elif group == "گاومیش":
                    population = float(unit["buffalo_count"] or 0)

                else:
                    continue

                population_by_key[(unit_id_value, group)] = population

        # Aggregate final groups.
        group_totals: dict[
            str,
            dict[str, float],
        ] = {}

        for key, vaccinated in unit_group_vaccinated.items():
            unit_id_value, group = key

            population = population_by_key.get(
                key,
                0.0,
            )

            if group not in group_totals:
                group_totals[group] = {
                    "vaccinated": 0.0,
                    "population": 0.0,
                }

            group_totals[group]["vaccinated"] += vaccinated
            group_totals[group]["population"] += population

        result_groups: list[dict[str, Any]] = []

        total_vaccinated = 0.0
        total_population = 0.0

        for group in sorted(group_totals):
            vaccinated = group_totals[group]["vaccinated"]
            population = group_totals[group]["population"]

            coverage = (
                round(
                    vaccinated / population * 100,
                    2,
                )
                if population > 0
                else 0
            )

            # We don't artificially cap the raw result.
            # If repeated vaccination operations exist, that should remain
            # visible in the raw KPI instead of silently hiding the issue.
            result_groups.append(
                {
                    "animal_group": group,
                    "vaccinated": vaccinated,
                    "population": population,
                    "remaining": max(
                        population - vaccinated,
                        0,
                    ),
                    "coverage_percent": coverage,
                }
            )

            total_vaccinated += vaccinated
            total_population += population

        total_coverage = (
            round(
                total_vaccinated / total_population * 100,
                2,
            )
            if total_population > 0
            else 0
        )

        return self._clean(
            {
                "vaccinated": total_vaccinated,
                "population": total_population,
                "remaining": max(
                    total_population - total_vaccinated,
                    0,
                ),
                "coverage_percent": total_coverage,
                "groups": result_groups,
            }
        )

    # ------------------------------------------------------------------
    # Vaccination breakdown by animal type
    # ------------------------------------------------------------------

    def vaccination_by_animal_type(
        self,
        vaccine_type: str | None = None,
        province_id: int | None = None,
        county_id: int | None = None,
        unit_id: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Return vaccination KPIs by normalized animal population group.

        This is the main dataset for dashboard charts/cards.
        """

        result = self.vaccination_kpi(
            vaccine_type=vaccine_type,
            province_id=province_id,
            county_id=county_id,
            unit_id=unit_id,
        )

        return result.get("groups", [])

    # ------------------------------------------------------------------
    # Overview
    # ------------------------------------------------------------------

    def overview(
        self,
        start: date | None = None,
        end: date | None = None,
    ):
        units = "gis_epidemiology_units"

        u_active = self.pick(
            units,
            "is_active",
            "active",
        )

        unit_where = "TRUE" if not u_active else f"{self.ident(u_active)} = TRUE"

        total_units = self.count(units)
        active_units = self.count(
            units,
            unit_where,
        )

        # --------------------------------------------------------------
        # Livestock population
        # --------------------------------------------------------------

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

        # --------------------------------------------------------------
        # Disease
        # --------------------------------------------------------------

        disease_reports = self.count("gis_disease_reports")

        disease_occurrences = self.count("gis_disease_occurrences")

        diseases = self.count("gis_diseases")

        active_outbreaks = 0

        if self.has_table("gis_outbreaks"):
            status = self.pick(
                "gis_outbreaks",
                "status",
            )

            if status:
                active_outbreaks = self.count(
                    "gis_outbreaks",
                    f"""
                    LOWER(
                        COALESCE(
                            {self.ident(status)},
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

        # --------------------------------------------------------------
        # Care
        # --------------------------------------------------------------

        care = "gis_enable_cares"

        care_total = self.count(care)

        care_animals = self.sum_col(
            care,
            self.pick(
                care,
                "total_animals",
                "animal_count",
                "animals_count",
            ),
        )

        care_positive = self.sum_col(
            care,
            self.pick(
                care,
                "positive_count",
                "positive",
            ),
        )

        care_negative = self.sum_col(
            care,
            self.pick(
                care,
                "negative_count",
                "negative",
            ),
        )

        care_suspicious = self.sum_col(
            care,
            self.pick(
                care,
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

        # --------------------------------------------------------------
        # Vaccination
        # --------------------------------------------------------------

        vaccination = self.vaccination_kpi()

        vaccinated = float(
            vaccination.get(
                "vaccinated",
                0,
            )
        )

        livestock_population_for_vaccination = float(
            vaccination.get(
                "population",
                0,
            )
        )

        vaccination_coverage = float(
            vaccination.get(
                "coverage_percent",
                0,
            )
        )

        vaccination_remaining = float(
            vaccination.get(
                "remaining",
                0,
            )
        )

        vaccination_groups = vaccination.get(
            "groups",
            [],
        )

        # --------------------------------------------------------------
        # Laboratory / samples
        # --------------------------------------------------------------

        lab = "gis_laboratory_results"
        sample = "gis_send_sample_details"

        lab_results = self.count(lab)

        lab_samples = self.sum_col(
            lab,
            self.pick(
                lab,
                "sample_count",
                "samples_count",
            ),
        )

        sent_samples = self.sum_col(
            sample,
            self.pick(
                sample,
                "sample_count",
                "samples_count",
            ),
        )

        # --------------------------------------------------------------
        # Positive laboratory results
        # --------------------------------------------------------------

        lab_status = self.pick(
            lab,
            "result_status",
            "status",
            "result",
        )

        lab_positive = 0

        if lab_status:
            status_identifier = self.ident(lab_status)

            lab_positive = self.count(
                lab,
                f"""
                (
                    LOWER(
                        COALESCE(
                            {status_identifier},
                            ''
                        )
                    ) LIKE '%positive%'
                    OR
                    COALESCE(
                        {status_identifier},
                        ''
                    ) LIKE '%مثبت%'
                )
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

        # --------------------------------------------------------------
        # Vaccine inventory / logistics
        # --------------------------------------------------------------

        inv = "gis_vaccine_inventories"

        inv_packages = self.sum_col(
            inv,
            self.pick(
                inv,
                "package_count",
                "packages_count",
                "quantity",
                "stock_quantity",
            ),
        )

        dist = "gis_vaccine_distributions"

        dist_packages = self.sum_col(
            dist,
            self.pick(
                dist,
                "package_count",
                "packages_count",
                "quantity",
            ),
        )

        disp = "gis_vaccine_disposals"

        disp_packages = self.sum_col(
            disp,
            self.pick(
                disp,
                "package_count",
                "packages_count",
                "quantity",
            ),
        )

        expiring_30 = 0

        exp_col = self.pick(
            inv,
            "expiration_date",
            "expiry_date",
            "expire_date",
        )

        if exp_col:
            expiring_30 = self.count(
                inv,
                f"""
                {self.ident(exp_col)} IS NOT NULL
                AND
                {self.ident(exp_col)}
                    <= CURRENT_DATE + INTERVAL '30 days'
                """,
            )

        # --------------------------------------------------------------
        # Time series
        # --------------------------------------------------------------

        vaccination_series = self.monthly_sum_series(
            "gis_vaccination_performances",
            self.pick(
                "gis_vaccination_performances",
                "vaccinated_animals",
                "vaccinated_count",
                "performed_count",
            ),
            (
                "vaccination_date",
                "operation_date",
                "date",
            ),
            "vaccination",
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
        )

        care_series = self.monthly_sum_series(
            care,
            self.pick(
                care,
                "positive_count",
                "positive",
            ),
            (
                "care_date",
                "operation_date",
                "date",
            ),
            "positive",
        )

        # --------------------------------------------------------------
        # Breakdowns
        # --------------------------------------------------------------

        vaccination_by_county = self.vaccination_by_county()

        disease_breakdown = self.disease_breakdown()

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
                    # Vaccination KPI
                    "vaccinated_animals": vaccinated,
                    "vaccination_population": livestock_population_for_vaccination,
                    "eligible_animals": livestock_population_for_vaccination,
                    "vaccination_coverage": vaccination_coverage,
                    "vaccination_remaining": vaccination_remaining,
                    "lab_results": lab_results,
                    "lab_samples": lab_samples,
                    "sent_samples": sent_samples,
                    "lab_positive": lab_positive,
                    "lab_positive_rate": lab_positive_rate,
                    "inventory_packages": inv_packages,
                    "distributed_packages": dist_packages,
                    "disposed_packages": disp_packages,
                    "expiring_30_days": expiring_30,
                },
                "vaccination": {
                    "total": vaccination,
                    "by_animal_type": vaccination_groups,
                },
                "series": {
                    "vaccination": vaccination_series,
                    "disease_reports": disease_series,
                    "care_positive": care_series,
                },
                "breakdowns": {
                    "vaccination_by_county": vaccination_by_county,
                    "vaccination_by_animal_type": vaccination_groups,
                    "disease_by_name": disease_breakdown,
                },
                "scopes": {
                    "prediction_scope": "county",
                    "unit_drilldown": True,
                    "vaccination_denominator": "gis_epidemiology_units livestock population",
                    "eligible_animals_source": "master_population",
                },
            }
        )

    # ------------------------------------------------------------------
    # Monthly series
    # ------------------------------------------------------------------

    def monthly_count_series(
        self,
        table: str,
        date_candidates: tuple[str, ...],
        label: str,
    ):
        if not self.has_table(table):
            return []

        date_column = self.pick(
            table,
            *date_candidates,
        )

        if not date_column:
            return []

        rows = self._rows(f"""
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
            WHERE {self.ident(date_column)} IS NOT NULL
            GROUP BY 1
            ORDER BY 1
            """)

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
        value_col: str | None,
        date_candidates: tuple[str, ...],
        label: str,
    ):
        if not value_col or not self.has_table(table):
            return []

        date_column = self.pick(
            table,
            *date_candidates,
        )

        if not date_column:
            return []

        rows = self._rows(f"""
            SELECT
                TO_CHAR(
                    DATE_TRUNC(
                        'month',
                        {self.ident(date_column)}
                    ),
                    'YYYY-MM'
                ) AS period,
                COALESCE(
                    SUM({self.ident(value_col)}),
                    0
                )::numeric AS value
            FROM {self.ident(table)}
            WHERE {self.ident(date_column)} IS NOT NULL
            GROUP BY 1
            ORDER BY 1
            """)

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
        value_col: str | None,
        date_candidates: tuple[str, ...],
        label: str,
    ):
        return self.monthly_sum_series(
            table,
            value_col,
            date_candidates,
            label,
        )

    # ------------------------------------------------------------------
    # Disease breakdown
    # ------------------------------------------------------------------

    def disease_breakdown(self):
        table = "gis_disease_reports"

        if not self.has_table(table):
            return []

        disease_id = self.pick(
            table,
            "disease_id",
        )

        if not disease_id:
            return []

        if self.has_table("gis_diseases"):
            name = self.pick(
                "gis_diseases",
                "name_fa",
                "name",
                "title",
                "disease_name",
                "label",
            )

            if name:
                rows = self._rows(f"""
                    SELECT
                        d.{self.ident(name)} AS name,
                        COUNT(r.id)::numeric AS value
                    FROM {self.ident(table)} r
                    LEFT JOIN gis_diseases d
                      ON d.id = r.{self.ident(disease_id)}
                    GROUP BY d.{self.ident(name)}
                    ORDER BY value DESC
                    LIMIT 10
                    """)

                return [
                    {
                        "name": row["name"] or "بدون نام",
                        "value": float(row["value"]),
                    }
                    for row in rows
                ]

        rows = self._rows(f"""
            SELECT
                CAST(
                    {self.ident(disease_id)}
                    AS text
                ) AS name,
                COUNT(*)::numeric AS value
            FROM {self.ident(table)}
            GROUP BY 1
            ORDER BY value DESC
            LIMIT 10
            """)

        return [
            {
                "name": row["name"],
                "value": float(row["value"]),
            }
            for row in rows
        ]

    # ------------------------------------------------------------------
    # Vaccination by county
    # ------------------------------------------------------------------

    def vaccination_by_county(
        self,
        table: str = "gis_vaccination_performances",
        vaccinated_col: str | None = None,
        eligible_col: str | None = None,
    ):
        """
        County vaccination breakdown.

        IMPORTANT:
        `eligible_col` is deliberately ignored as the current database
        contains zero eligible_animals.

        Coverage is based on master livestock population.
        """

        if not self.has_table(table):
            return []

        units = "gis_epidemiology_units"

        if not self.has_table(units):
            return []

        unit_col = self.pick(
            table,
            "epidemiology_unit_id",
        )

        vaccinated_col = vaccinated_col or self.pick(
            table,
            "vaccinated_animals",
            "vaccinated_count",
            "performed_count",
        )

        animal_col = self.pick(
            table,
            "animal_type",
        )

        county_id_col = self.pick(
            units,
            "county_id",
        )

        if not unit_col or not vaccinated_col or not animal_col or not county_id_col:
            return []

        # We first aggregate vaccination by:
        #
        # county + unit + animal group
        #
        # Then population is added once per unit/group.
        rows = self._rows(f"""
            SELECT
                u.{self.ident(county_id_col)} AS county_id,
                v.{self.ident(unit_col)} AS unit_id,
                v.{self.ident(animal_col)} AS animal_type,
                COALESCE(
                    SUM(
                        v.{self.ident(vaccinated_col)}
                    ),
                    0
                )::numeric AS vaccinated
            FROM {self.ident(table)} v
            JOIN {self.ident(units)} u
              ON u.id = v.{self.ident(unit_col)}
            WHERE v.{self.ident(unit_col)} IS NOT NULL
            GROUP BY
                u.{self.ident(county_id_col)},
                v.{self.ident(unit_col)},
                v.{self.ident(animal_col)}
            """)

        if not rows:
            return []

        county_unit_groups: dict[
            tuple[Any, int, str],
            float,
        ] = {}

        for row in rows:
            group = self.vaccination_animal_group(row["animal_type"])

            if not group:
                continue

            key = (
                row["county_id"],
                int(row["unit_id"]),
                group,
            )

            county_unit_groups[key] = county_unit_groups.get(key, 0.0) + float(
                row["vaccinated"] or 0
            )

        if not county_unit_groups:
            return []

        unit_ids = sorted({unit_id for _, unit_id, _ in county_unit_groups})

        population_rows = self._rows(
            f"""
            SELECT
                id,
                sheep_count,
                goat_count,
                cattle_count,
                dog_count,
                horse_count,
                camel_count,
                buffalo_count
            FROM {self.ident(units)}
            WHERE id = ANY(:unit_ids)
            """,
            {"unit_ids": unit_ids},
        )

        population_by_unit = {int(row["id"]): row for row in population_rows}

        result: dict[
            Any,
            dict[str, float],
        ] = {}

        for (
            county_id,
            unit_id,
            group,
        ), vaccinated in county_unit_groups.items():

            unit = population_by_unit.get(unit_id)

            if not unit:
                continue

            if group == "گاو و گوساله":
                population = float(unit["cattle_count"] or 0)

            elif group == "گوسفند":
                population = float(unit["sheep_count"] or 0)

            elif group == "بز":
                population = float(unit["goat_count"] or 0)

            elif group == "گوسفند و بز":
                population = float(unit["sheep_count"] or 0) + float(
                    unit["goat_count"] or 0
                )

            elif group == "سگ":
                population = float(unit["dog_count"] or 0)

            elif group == "اسب":
                population = float(unit["horse_count"] or 0)

            elif group == "شتر":
                population = float(unit["camel_count"] or 0)

            elif group == "گاومیش":
                population = float(unit["buffalo_count"] or 0)

            else:
                continue

            if county_id not in result:
                result[county_id] = {
                    "vaccinated": 0.0,
                    "population": 0.0,
                }

            result[county_id]["vaccinated"] += vaccinated

            result[county_id]["population"] += population

        county_name_column = None

        if self.has_table("gis_counties"):
            county_name_column = self.pick(
                "gis_counties",
                "name_fa",
                "name",
                "title",
                "county_name",
                "label",
            )

        output = []

        for county_id, values in result.items():
            vaccinated = values["vaccinated"]
            population = values["population"]

            coverage = (
                round(
                    vaccinated / population * 100,
                    2,
                )
                if population
                else 0
            )

            name = None

            if county_name_column:
                name_rows = self._rows(
                    f"""
                    SELECT
                        {self.ident(county_name_column)}
                        AS name
                    FROM gis_counties
                    WHERE id = :county_id
                    LIMIT 1
                    """,
                    {"county_id": county_id},
                )

                if name_rows:
                    name = name_rows[0]["name"]

            output.append(
                {
                    "county_id": county_id,
                    "name": name or "بدون نام",
                    "vaccinated": vaccinated,
                    "population": population,
                    "eligible": population,
                    "coverage": coverage,
                    "coverage_percent": coverage,
                    "remaining": max(
                        population - vaccinated,
                        0,
                    ),
                }
            )

        output.sort(
            key=lambda item: item["vaccinated"],
            reverse=True,
        )

        return output[:12]

    # ------------------------------------------------------------------
    # Unit drill-down
    # ------------------------------------------------------------------

    def unit_detail(
        self,
        unit_id: int,
    ):
        units = "gis_epidemiology_units"

        if not self.has_table(units):
            return {
                "unit": None,
                "error": "gis_epidemiology_units not found",
            }

        name_col = self.pick(
            units,
            "unit_name",
            "name",
            "title",
            "name_fa",
            "unit_title",
        )

        province_col = self.pick(
            units,
            "province_id",
        )

        county_col = self.pick(
            units,
            "county_id",
        )

        unit_type_col = self.pick(
            units,
            "unit_type_id",
        )

        select_parts = ["u.id"]

        if name_col:
            select_parts.append(f"""
                u.{self.ident(name_col)}
                AS unit_name
                """)

        if province_col:
            select_parts.append(f"""
                u.{self.ident(province_col)}
                AS province_id
                """)

        if county_col:
            select_parts.append(f"""
                u.{self.ident(county_col)}
                AS county_id
                """)

        if unit_type_col:
            select_parts.append(f"""
                u.{self.ident(unit_type_col)}
                AS unit_type_id
                """)

        rows = self._rows(
            f"""
            SELECT
                {', '.join(select_parts)}
            FROM {self.ident(units)} u
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

        # --------------------------------------------------------------
        # Vaccination
        # --------------------------------------------------------------

        vaccination = self.vaccination_kpi(unit_id=unit_id)

        operations = self.operation_history(unit_id)

        operation_counts: dict[
            str,
            int,
        ] = {}

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
                    "eligible": vaccination.get(
                        "population",
                        0,
                    ),
                    "population": vaccination.get(
                        "population",
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
                    "coverage_percent": vaccination.get(
                        "coverage_percent",
                        0,
                    ),
                    "by_animal_type": vaccination.get(
                        "groups",
                        [],
                    ),
                    "target_source": "gis_epidemiology_units",
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

    # ------------------------------------------------------------------
    # County predictions
    # ------------------------------------------------------------------

    def county_predictions(
        self,
        county_id: int | None,
    ):
        table = "gis_vaccination_predictions"

        if not self.has_table(table) or county_id is None:
            return []

        county_col = self.pick(
            table,
            "county_id",
        )

        value_col = self.pick(
            table,
            "prediction_value",
            "predicted_value",
            "target_value",
            "value",
        )

        year_col = self.pick(
            table,
            "prediction_year",
            "year",
        )

        category_col = self.pick(
            table,
            "prediction_category",
            "category",
        )

        if not county_col or not value_col:
            return []

        select_parts = [f"{self.ident(value_col)} AS value"]

        if year_col:
            select_parts.append(f"{self.ident(year_col)} AS year")

        if category_col:
            select_parts.append(f"{self.ident(category_col)} AS category")

        order_sql = self.ident(year_col) if year_col else "1"

        rows = self._rows(
            f"""
            SELECT
                {', '.join(select_parts)}
            FROM {self.ident(table)}
            WHERE {self.ident(county_col)}
                = :county_id
            ORDER BY {order_sql} DESC
            """,
            {"county_id": county_id},
        )

        return rows

    # ------------------------------------------------------------------
    # Operation history
    # ------------------------------------------------------------------

    def operation_history(
        self,
        unit_id: int,
    ):
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

        for (
            table,
            preferred_date,
            label,
        ) in specs:

            if not self.has_table(table):
                continue

            fk = self.pick(
                table,
                "epidemiology_unit_id",
            )

            if not fk:
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
                    :operation_label
                    AS operation_type
                FROM {self.ident(table)}
                WHERE {self.ident(fk)}
                    = :unit_id
                  AND {self.ident(date_column)}
                    IS NOT NULL
                """)

        if not union_parts:
            return []

        # Every UNION branch uses the same bind parameters.
        params = {
            "unit_id": unit_id,
            "operation_label": "",
        }

        # PostgreSQL UNION with one parameter for label is awkward when
        # different labels are required. Replace each branch's parameter
        # with a literal only after validation: labels are hard-coded here.
        union_parts = []

        for (
            table,
            preferred_date,
            label,
        ) in specs:

            if not self.has_table(table):
                continue

            fk = self.pick(
                table,
                "epidemiology_unit_id",
            )

            if not fk:
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

            escaped_label = label.replace(
                "'",
                "''",
            )

            union_parts.append(f"""
                SELECT
                    {self.ident(date_column)}
                    AS event_date,
                    '{escaped_label}'
                    AS operation_type
                FROM {self.ident(table)}
                WHERE {self.ident(fk)}
                    = :unit_id
                  AND {self.ident(date_column)}
                    IS NOT NULL
                """)

        sql = " UNION ALL ".join(union_parts) + """
            ORDER BY event_date DESC
            LIMIT 500
            """

        return self._rows(
            sql,
            {"unit_id": unit_id},
        )

    # ------------------------------------------------------------------
    # County drill-down
    # ------------------------------------------------------------------

    def county_detail(
        self,
        county_id: int,
    ):
        units = "gis_epidemiology_units"

        if not self.has_table(units):
            return {
                "county_id": county_id,
                "units": [],
            }

        county_col = self.pick(
            units,
            "county_id",
        )

        name_col = self.pick(
            units,
            "unit_name",
            "name",
            "title",
            "name_fa",
            "unit_title",
        )

        if not county_col:
            return {
                "county_id": county_id,
                "units": [],
            }

        name_sql = f"u.{self.ident(name_col)}" if name_col else "CAST(u.id AS text)"

        rows = self._rows(
            f"""
            SELECT
                u.id,
                {name_sql} AS name
            FROM {self.ident(units)} u
            WHERE u.{self.ident(county_col)}
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
                    "name": row["name"] or "بدون نام",
                    "eligible": vaccination.get(
                        "eligible",
                        0,
                    ),
                    "population": vaccination.get(
                        "population",
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

    # ------------------------------------------------------------------
    # KPI drill-down to units
    # ------------------------------------------------------------------

    def metric_units(
        self,
        metric: str,
    ):
        """
        Return unit-level values for the selected KPI.

        Vaccination is calculated using master population rather than
        eligible_animals.
        """

        if not self.has_table("gis_epidemiology_units"):
            return []

        units = "gis_epidemiology_units"

        name = self.pick(
            units,
            "unit_name",
            "name",
            "title",
            "name_fa",
            "unit_title",
        )

        county = self.pick(
            units,
            "county_id",
        )

        province = self.pick(
            units,
            "province_id",
        )

        name_sql = f"u.{self.ident(name)}" if name else "CAST(u.id AS text)"

        base = [
            "u.id AS unit_id",
            f"{name_sql} AS unit_name",
        ]

        if county:
            base.append(f"u.{self.ident(county)} AS county_id")

        if province:
            base.append(f"u.{self.ident(province)} AS province_id")

        # --------------------------------------------------------------
        # Vaccination
        # --------------------------------------------------------------

        if metric == "vaccination":
            rows = self._rows(f"""
                SELECT
                    u.id AS unit_id,
                    {name_sql} AS unit_name,
                    {
                        f"u.{self.ident(county)} AS county_id,"
                        if county
                        else ""
                    }
                    {
                        f"u.{self.ident(province)} AS province_id,"
                        if province
                        else ""
                    }
                    u.sheep_count,
                    u.goat_count,
                    u.cattle_count,
                    u.dog_count,
                    u.horse_count,
                    u.camel_count,
                    u.buffalo_count
                FROM {self.ident(units)} u
                ORDER BY u.id
                """)

            result = []

            for row in rows:
                unit_id = int(row["unit_id"])

                vaccination = self.vaccination_kpi(unit_id=unit_id)

                result.append(
                    {
                        "unit_id": unit_id,
                        "unit_name": row["unit_name"],
                        "county_id": row.get("county_id"),
                        "province_id": row.get("province_id"),
                        "value": vaccination.get(
                            "vaccinated",
                            0,
                        ),
                        "target": vaccination.get(
                            "population",
                            0,
                        ),
                        "population": vaccination.get(
                            "population",
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
                        "progress_percent": vaccination.get(
                            "coverage_percent",
                            0,
                        ),
                        "by_animal_type": vaccination.get(
                            "groups",
                            [],
                        ),
                    }
                )

            result.sort(
                key=lambda item: float(item["value"] or 0),
                reverse=True,
            )

            return result

        # --------------------------------------------------------------
        # Other metrics
        # --------------------------------------------------------------

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
            table, preferred_date = metric_specs[metric]

            if self.has_table(table):
                fk = self.pick(
                    table,
                    "epidemiology_unit_id",
                )

                date_column = self.pick(
                    table,
                    preferred_date,
                    "operation_date",
                    "date",
                    "created_at",
                    "event_date",
                )

                if fk:
                    group_parts = [
                        "u.id",
                        name_sql,
                    ]

                    if county:
                        group_parts.append(f"u.{self.ident(county)}")

                    if province:
                        group_parts.append(f"u.{self.ident(province)}")

                    sql = f"""
                        SELECT
                            {', '.join(base)},
                            COUNT(x.id)::numeric
                                AS value
                        FROM gis_epidemiology_units u
                        LEFT JOIN {self.ident(table)} x
                          ON x.{self.ident(fk)} = u.id
                        GROUP BY
                            {', '.join(group_parts)}
                        ORDER BY value DESC
                    """

                    return self._rows(sql)

        # --------------------------------------------------------------
        # All operations
        # --------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Map data
    # ------------------------------------------------------------------

    def map_points(self):
        table = "gis_epidemiology_units"

        if not self.has_table(table):
            return []

        lat = self.pick(
            table,
            "latitude",
            "lat",
        )

        lon = self.pick(
            table,
            "longitude",
            "lon",
            "lng",
        )

        name = self.pick(
            table,
            "unit_name",
            "name",
            "title",
            "name_fa",
            "unit_title",
        )

        county = self.pick(
            table,
            "county_id",
        )

        province = self.pick(
            table,
            "province_id",
        )

        if not lat or not lon:
            return []

        rows = self._rows(f"""
            SELECT
                id,

                {
                    self.ident(name)
                    if name
                    else "CAST(id AS text)"
                } AS name,

                {self.ident(lat)}
                    AS latitude,

                {self.ident(lon)}
                    AS longitude,

                {
                    self.ident(county)
                    if county
                    else "NULL"
                } AS county_id,

                {
                    self.ident(province)
                    if province
                    else "NULL"
                } AS province_id

            FROM {self.ident(table)}

            WHERE
                {self.ident(lat)}
                    IS NOT NULL
                AND
                {self.ident(lon)}
                    IS NOT NULL

            LIMIT 20000
            """)

        return rows
