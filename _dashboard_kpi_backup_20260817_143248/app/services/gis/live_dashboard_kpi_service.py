from __future__ import annotations

from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class LiveDashboardKPIService:
    """
    Live KPI service.
    Every public method queries PostgreSQL directly through the supplied
    SQLAlchemy Session. No KPI snapshot/cache is used.
    """

    _tables_cache: set[str] | None = None
    _columns_cache: dict[str, set[str]] = {}

    def __init__(self, db: Session):
        self.db = db

    # ---------- schema helpers ----------

    def _tables(self) -> set[str]:
        if self.__class__._tables_cache is None:
            rows = self.db.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema='public'
                  AND table_type='BASE TABLE'
            """)).mappings().all()
            self.__class__._tables_cache = {str(r["table_name"]) for r in rows}
        return self.__class__._tables_cache

    def has_table(self, table: str) -> bool:
        return table in self._tables()

    def cols(self, table: str) -> set[str]:
        if table in self.__class__._columns_cache:
            return self.__class__._columns_cache[table]
        if not self.has_table(table):
            return set()
        rows = self.db.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema='public' AND table_name=:t
        """), {"t": table}).mappings().all()
        result = {str(r["column_name"]) for r in rows}
        self.__class__._columns_cache[table] = result
        return result

    def pick(self, table: str, *candidates: str) -> str | None:
        c = self.cols(table)
        for x in candidates:
            if x in c:
                return x
        return None

    @staticmethod
    def ident(value: str) -> str:
        # Identifiers come only from information_schema / hard-coded names.
        if not value.replace("_", "").isalnum():
            raise ValueError(f"Unsafe identifier: {value}")
        return '"' + value + '"'

    def _scalar(self, sql: str, params: dict[str, Any] | None = None, default=0):
        v = self.db.execute(text(sql), params or {}).scalar()
        if v is None:
            return default
        if isinstance(v, Decimal):
            return float(v)
        return v

    def _rows(self, sql: str, params: dict[str, Any] | None = None):
        return [dict(r) for r in self.db.execute(text(sql), params or {}).mappings().all()]

    @staticmethod
    def _jsonable(v: Any):
        if isinstance(v, (datetime, date)):
            return v.isoformat()
        if isinstance(v, Decimal):
            return float(v)
        return v

    def _clean(self, obj: Any):
        if isinstance(obj, dict):
            return {k: self._clean(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._clean(v) for v in obj]
        return self._jsonable(obj)

    # ---------- generic aggregation helpers ----------

    def count(self, table: str, where: str = "TRUE", params=None) -> int:
        if not self.has_table(table):
            return 0
        return int(self._scalar(
            f"SELECT COUNT(*) FROM {self.ident(table)} WHERE {where}",
            params, 0
        ))

    def sum_col(self, table: str, col: str | None, where: str = "TRUE", params=None) -> float:
        if not col or not self.has_table(table) or col not in self.cols(table):
            return 0.0
        return float(self._scalar(
            f"SELECT COALESCE(SUM({self.ident(col)}),0) FROM {self.ident(table)} WHERE {where}",
            params, 0
        ))

    def date_col(self, table: str, candidates: tuple[str, ...]) -> str | None:
        return self.pick(table, *candidates)

    def _period_where(self, table: str, start: date | None, end: date | None):
        d = self.date_col(table, (
            "operation_date","vaccination_date","care_date","report_date",
            "occurrence_date","sampling_date","sample_date","answer_date",
            "spraying_date","disposal_date","distribution_date","event_date",
            "start_date","created_at","date","inspection_date"
        ))
        if not d:
            return "TRUE", {}
        parts = []
        params: dict[str, Any] = {}
        if start:
            parts.append(f"{self.ident(d)} >= :p_start")
            params["p_start"] = start
        if end:
            parts.append(f"{self.ident(d)} < :p_end")
            params["p_end"] = end
        return (" AND ".join(parts) if parts else "TRUE"), params

    # ---------- overview ----------

    def overview(self, start: date | None = None, end: date | None = None):
        units = "gis_epidemiology_units"
        u_active = self.pick(units, "is_active", "active")
        unit_where = "TRUE" if not u_active else f"{self.ident(u_active)} = TRUE"

        total_units = self.count(units)
        active_units = self.count(units, unit_where)

        # Livestock population
        livestock_cols = [
            self.pick(units, "sheep_count"),
            self.pick(units, "cattle_count"),
            self.pick(units, "goat_count"),
            self.pick(units, "horse_count"),
            self.pick(units, "dog_count"),
            self.pick(units, "camel_count"),
            self.pick(units, "buffalo_count"),
        ]
        livestock_cols = [c for c in livestock_cols if c]
        total_livestock = 0.0
        if livestock_cols:
            total_livestock = float(self._scalar(
                "SELECT COALESCE(SUM(" + " + ".join(f"COALESCE({self.ident(c)},0)" for c in livestock_cols) + "),0)"
                f" FROM {self.ident(units)}", {}, 0
            ))

        # Disease
        disease_reports = self.count("gis_disease_reports")
        disease_occurrences = self.count("gis_disease_occurrences")
        diseases = self.count("gis_diseases")
        outbreaks = 0
        if self.has_table("gis_outbreaks"):
            status = self.pick("gis_outbreaks", "status")
            outbreaks = self.count(
                "gis_outbreaks",
                f"LOWER(COALESCE({self.ident(status)},'')) IN ('active','open','ongoing')"
                if status else "TRUE"
            )

        # Care
        care = "gis_enable_cares"
        care_total = self.count(care)
        care_animals = self.sum_col(care, self.pick(care, "total_animals", "animal_count", "animals_count"))
        care_positive = self.sum_col(care, self.pick(care, "positive_count", "positive"))
        care_negative = self.sum_col(care, self.pick(care, "negative_count", "negative"))
        care_suspicious = self.sum_col(care, self.pick(care, "suspicious_count", "suspect_count", "suspected_count"))
        care_positive_rate = round((care_positive / care_animals * 100), 2) if care_animals else 0

        # Vaccination
        vp = "gis_vaccination_performances"
        vaccinated_col = self.pick(vp, "vaccinated_animals", "vaccinated_count", "performed_count")
        eligible_col = self.pick(vp, "eligible_animals", "eligible_count", "target_animals", "planned_animals")
        vaccinated = self.sum_col(vp, vaccinated_col)
        eligible = self.sum_col(vp, eligible_col)
        vaccination_coverage = round(vaccinated / eligible * 100, 2) if eligible else 0
        vaccination_remaining = max(eligible - vaccinated, 0)

        # Laboratory / samples
        lab = "gis_laboratory_results"
        sample = "gis_send_sample_details"
        lab_results = self.count(lab)
        lab_samples = self.sum_col(lab, self.pick(lab, "sample_count", "samples_count"))
        sent_samples = self.sum_col(sample, self.pick(sample, "sample_count", "samples_count"))

        # Positive laboratory results. We deliberately support common English/Persian labels.
        lab_status = self.pick(lab, "result_status", "status", "result")
        lab_positive = 0
        if lab_status:
            lab_positive = self.count(
                lab,
                f"LOWER(COALESCE({self.ident(lab_status)},'')) LIKE '%positive%' "
                f"OR LOWER(COALESCE({self.ident(lab_status)},'')) LIKE '%Ù…Ø«Ø¨Øª%'"
            )
        lab_positive_rate = round(lab_positive / lab_results * 100, 2) if lab_results else 0

        # Vaccine inventory / logistics
        inv = "gis_vaccine_inventories"
        inv_packages = self.sum_col(inv, self.pick(inv, "package_count", "packages_count", "quantity", "stock_quantity"))
        dist = "gis_vaccine_distributions"
        dist_packages = self.sum_col(dist, self.pick(dist, "package_count", "packages_count", "quantity"))
        disp = "gis_vaccine_disposals"
        disp_packages = self.sum_col(disp, self.pick(disp, "package_count", "packages_count", "quantity"))

        expiring_30 = 0
        exp_col = self.pick(inv, "expiration_date", "expiry_date", "expire_date")
        if exp_col:
            expiring_30 = self.count(
                inv,
                f"{self.ident(exp_col)} IS NOT NULL AND {self.ident(exp_col)} <= CURRENT_DATE + INTERVAL '30 days'"
            )

        # Time series for the dashboard
        vaccination_series = self.monthly_series(
            vp, vaccinated_col, ("vaccination_date","operation_date","date"), "vaccination"
        )
        disease_series = self.monthly_count_series(
            "gis_disease_reports", ("report_date","occurrence_date","created_at","date"), "reports"
        )
        care_series = self.monthly_sum_series(
            care, self.pick(care, "positive_count", "positive"), ("care_date","operation_date","date"), "positive"
        )

        # County breakdowns
        county_breakdown = self.vaccination_by_county(vp, vaccinated_col, eligible_col)
        disease_breakdown = self.disease_breakdown()

        return self._clean({
            "generated_at": datetime.utcnow(),
            "live": True,
            "cards": {
                "total_units": total_units,
                "active_units": active_units,
                "total_livestock": total_livestock,
                "disease_reports": disease_reports,
                "disease_occurrences": disease_occurrences,
                "diseases": diseases,
                "active_outbreaks": outbreaks,
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
                "inventory_packages": inv_packages,
                "distributed_packages": dist_packages,
                "disposed_packages": disp_packages,
                "expiring_30_days": expiring_30,
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
        })

    def monthly_count_series(self, table, date_candidates, label):
        if not self.has_table(table):
            return []
        d = self.pick(table, *date_candidates)
        if not d:
            return []
        rows = self._rows(f"""
            SELECT TO_CHAR(DATE_TRUNC('month',{self.ident(d)}),'YYYY-MM') AS period,
                   COUNT(*)::numeric AS value
            FROM {self.ident(table)}
            WHERE {self.ident(d)} IS NOT NULL
            GROUP BY 1 ORDER BY 1
        """)
        return [{"period": r["period"], "value": float(r["value"]), "label": label} for r in rows]

    def monthly_sum_series(self, table, value_col, date_candidates, label):
        if not value_col or not self.has_table(table):
            return []
        d = self.pick(table, *date_candidates)
        if not d:
            return []
        rows = self._rows(f"""
            SELECT TO_CHAR(DATE_TRUNC('month',{self.ident(d)}),'YYYY-MM') AS period,
                   COALESCE(SUM({self.ident(value_col)}),0)::numeric AS value
            FROM {self.ident(table)}
            WHERE {self.ident(d)} IS NOT NULL
            GROUP BY 1 ORDER BY 1
        """)
        return [{"period": r["period"], "value": float(r["value"]), "label": label} for r in rows]

    def monthly_series(self, table, value_col, date_candidates, label):
        return self.monthly_sum_series(table, value_col, date_candidates, label)

    def disease_breakdown(self):
        t = "gis_disease_reports"
        if not self.has_table(t):
            return []
        did = self.pick(t, "disease_id")
        if not did:
            return []
        if self.has_table("gis_diseases"):
            name = self.pick("gis_diseases", "name_fa","name","title","disease_name","label")
            if name:
                rows = self._rows(f"""
                    SELECT d.{self.ident(name)} AS name, COUNT(r.id)::numeric AS value
                    FROM {self.ident(t)} r
                    LEFT JOIN gis_diseases d ON d.id=r.{self.ident(did)}
                    GROUP BY d.{self.ident(name)}
                    ORDER BY value DESC
                    LIMIT 10
                """)
                return [{"name": r["name"] or "Ø¨Ø¯ÙˆÙ† Ù†Ø§Ù…", "value": float(r["value"])} for r in rows]
        rows = self._rows(f"""
            SELECT CAST({self.ident(did)} AS text) AS name, COUNT(*)::numeric AS value
            FROM {self.ident(t)}
            GROUP BY 1 ORDER BY value DESC LIMIT 10
        """)
        return [{"name": r["name"], "value": float(r["value"])} for r in rows]

    def vaccination_by_county(self, table, vaccinated_col, eligible_col):
        if not self.has_table(table):
            return []
        county_col = self.pick(table, "county_id")
        unit_col = self.pick(table, "epidemiology_unit_id")
        if not county_col and not unit_col:
            return []
        # The performance table has a unit FK in the current schema. We derive county
        # through gis_epidemiology_units, which keeps the drill-down path consistent.
        if unit_col and self.has_table("gis_epidemiology_units"):
            county_id = self.pick("gis_epidemiology_units", "county_id")
            if county_id:
                cname = self.pick("gis_counties", "name_fa","name","title","county_name","label") if self.has_table("gis_counties") else None
                name_sql = f"c.{self.ident(cname)}" if cname else f"CAST(u.{self.ident(county_id)} AS text)"
                join_name = f"LEFT JOIN gis_counties c ON c.id=u.{self.ident(county_id)}" if cname else ""
                rows = self._rows(f"""
                    SELECT {name_sql} AS name,
                           COALESCE(SUM(p.{self.ident(vaccinated_col)}),0)::numeric AS vaccinated,
                           COALESCE(SUM(p.{self.ident(eligible_col) if eligible_col else vaccinated_col}),0)::numeric AS eligible
                    FROM {self.ident(table)} p
                    JOIN gis_epidemiology_units u ON u.id=p.{self.ident(unit_col)}
                    {join_name}
                    GROUP BY {name_sql}
                    ORDER BY vaccinated DESC
                    LIMIT 12
                """)
                return [{
                    "name": r["name"] or "Ø¨Ø¯ÙˆÙ† Ù†Ø§Ù…",
                    "vaccinated": float(r["vaccinated"]),
                    "eligible": float(r["eligible"]),
                    "coverage": round(float(r["vaccinated"]) / float(r["eligible"]) * 100, 2) if float(r["eligible"]) else 0,
                } for r in rows]
        return []

    # ---------- unit drill-down ----------

    def unit_detail(self, unit_id: int):
        if not self.has_table("gis_epidemiology_units"):
            return {"unit": None, "error": "gis_epidemiology_units not found"}

        uc = self.cols("gis_epidemiology_units")
        name_col = self.pick("gis_epidemiology_units","unit_name","name","title","name_fa","unit_title")
        province_col = self.pick("gis_epidemiology_units","province_id")
        county_col = self.pick("gis_epidemiology_units","county_id")
        unit_type_col = self.pick("gis_epidemiology_units","unit_type_id")

        select_parts = ["u.id"]
        if name_col: select_parts.append(f"u.{self.ident(name_col)} AS unit_name")
        if province_col: select_parts.append(f"u.{self.ident(province_col)} AS province_id")
        if county_col: select_parts.append(f"u.{self.ident(county_col)} AS county_id")
        if unit_type_col: select_parts.append(f"u.{self.ident(unit_type_col)} AS unit_type_id")
        rows = self._rows(
            f"SELECT {', '.join(select_parts)} FROM gis_epidemiology_units u WHERE u.id=:uid",
            {"uid": unit_id}
        )
        if not rows:
            return {"unit": None, "error": "ÙˆØ§Ø­Ø¯ Ù¾ÛŒØ¯Ø§ Ù†Ø´Ø¯"}
        unit = rows[0]

        # Vaccination for this unit
        vp = "gis_vaccination_performances"
        unit_fk = self.pick(vp, "epidemiology_unit_id")
        vacc_col = self.pick(vp, "vaccinated_animals","vaccinated_count","performed_count")
        elig_col = self.pick(vp, "eligible_animals","eligible_count","target_animals","planned_animals")
        vacc_total = self.sum_col(vp, vacc_col, f"{self.ident(unit_fk)}=:uid" if unit_fk else "FALSE", {"uid":unit_id}) if unit_fk else 0
        elig_total = self.sum_col(vp, elig_col, f"{self.ident(unit_fk)}=:uid" if unit_fk else "FALSE", {"uid":unit_id}) if unit_fk else 0
        vacc_coverage = round(vacc_total / elig_total * 100, 2) if elig_total else 0

        # Operation history is a live union of real source tables.
        operations = self.operation_history(unit_id)

        # Per-operation chart counts
        op_counts = {}
        for x in operations:
            op_counts[x["operation_type"]] = op_counts.get(x["operation_type"], 0) + 1

        # Unit prediction note: current FK schema shows predictions at county_id/disease_id,
        # not epidemiology_unit_id. We therefore expose county prediction separately.
        predictions = self.county_predictions(unit.get("county_id"))

        return self._clean({
            "unit": unit,
            "vaccination": {
                "eligible": elig_total,
                "vaccinated": vacc_total,
                "remaining": max(elig_total-vacc_total,0),
                "coverage_percent": vacc_coverage,
                "target_source": "unit eligible_animals",
            },
            "county_predictions": predictions,
            "operation_history": operations,
            "operation_counts": [{"name": k, "value": v} for k,v in sorted(op_counts.items(), key=lambda z: -z[1])],
        })

    def county_predictions(self, county_id):
        t = "gis_vaccination_predictions"
        if not self.has_table(t) or county_id is None:
            return []
        cc = self.pick(t, "county_id")
        val = self.pick(t, "prediction_value","predicted_value","target_value","value")
        year = self.pick(t, "prediction_year","year")
        category = self.pick(t, "prediction_category","category")
        if not cc or not val:
            return []
        select = [f"{self.ident(val)} AS value"]
        if year: select.append(f"{self.ident(year)} AS year")
        if category: select.append(f"{self.ident(category)} AS category")
        rows = self._rows(
            f"SELECT {', '.join(select)} FROM {self.ident(t)} WHERE {self.ident(cc)}=:cid ORDER BY {self.ident(year) if year else '1'} DESC",
            {"cid": county_id}
        )
        return rows

    def operation_history(self, unit_id: int):
        specs = [
            ("gis_enable_cares", "care_date", "Ù…Ø±Ø§Ù‚Ø¨Øª"),
            ("gis_vaccination_performances", "vaccination_date", "ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†"),
            ("gis_laboratory_results", "sampling_date", "Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡"),
            ("gis_send_sample_details", "sampling_date", "Ø§Ø±Ø³Ø§Ù„ Ù†Ù…ÙˆÙ†Ù‡"),
            ("gis_slaughter_disposals", "disposal_date", "Ú©Ø´ØªØ§Ø±/Ø§Ù…Ø­Ø§Ø¡"),
            ("gis_spraying", "spraying_date", "Ø³Ù…Ù¾Ø§Ø´ÛŒ"),
            ("gis_vaccine_distributions", "distribution_date", "ØªÙˆØ²ÛŒØ¹ ÙˆØ§Ú©Ø³Ù†"),
            ("gis_vaccine_disposals", "disposal_date", "Ø¯ÙØ¹ ÙˆØ§Ú©Ø³Ù†"),
            ("gis_disease_reports", "report_date", "Ú¯Ø²Ø§Ø±Ø´ Ø¨ÛŒÙ…Ø§Ø±ÛŒ"),
            ("gis_disease_occurrences", "occurrence_date", "ÙˆÙ‚ÙˆØ¹ Ø¨ÛŒÙ…Ø§Ø±ÛŒ"),
        ]
        union_parts = []
        for table, preferred_date, label in specs:
            if not self.has_table(table):
                continue
            fk = self.pick(table, "epidemiology_unit_id")
            if not fk:
                continue
            d = self.pick(table, preferred_date, "operation_date","date","created_at","event_date")
            if not d:
                continue
            union_parts.append(
                f"SELECT {self.ident(d)} AS event_date, '{label}' AS operation_type "
                f"FROM {self.ident(table)} WHERE {self.ident(fk)}=:uid AND {self.ident(d)} IS NOT NULL"
            )
        if not union_parts:
            return []
        sql = " UNION ALL ".join(union_parts) + " ORDER BY event_date DESC LIMIT 500"
        return self._rows(sql, {"uid":unit_id})

    # ---------- county drilldown ----------

    def county_detail(self, county_id: int):
        # Return all unit IDs in this county and their current vaccination progress.
        if not self.has_table("gis_epidemiology_units"):
            return {"units":[]}
        county_col = self.pick("gis_epidemiology_units","county_id")
        name_col = self.pick("gis_epidemiology_units","unit_name","name","title","name_fa","unit_title")
        if not county_col:
            return {"units":[]}
        name_sql = f"u.{self.ident(name_col)}" if name_col else "CAST(u.id AS text)"
        rows = self._rows(
            f"SELECT u.id, {name_sql} AS name FROM gis_epidemiology_units u WHERE u.{self.ident(county_col)}=:cid ORDER BY name",
            {"cid":county_id}
        )
        result = []
        for r in rows:
            d = self.unit_detail(int(r["id"]))
            v = d.get("vaccination", {})
            result.append({
                "id": r["id"],
                "name": r["name"] or "Ø¨Ø¯ÙˆÙ† Ù†Ø§Ù…",
                "eligible": v.get("eligible",0),
                "vaccinated": v.get("vaccinated",0),
                "remaining": v.get("remaining",0),
                "coverage": v.get("coverage_percent",0),
                "operations": len(d.get("operation_history",[])),
            })
        return {"county_id": county_id, "units": result}

    # ---------- KPI drill-down to units ----------

    def metric_units(self, metric: str):
        """
        Returns unit-level values for the selected KPI.
        This is intentionally calculated live from source tables, so clicking a KPI
        always leads to the records that currently form that KPI.
        """
        if not self.has_table("gis_epidemiology_units"):
            return []

        units = "gis_epidemiology_units"
        name = self.pick(units, "unit_name","name","title","name_fa","unit_title")
        county = self.pick(units, "county_id")
        province = self.pick(units, "province_id")
        name_sql = f"u.{self.ident(name)}" if name else "CAST(u.id AS text)"
        base = [f"u.id AS unit_id", f"{name_sql} AS unit_name"]
        if county: base.append(f"u.{self.ident(county)} AS county_id")
        if province: base.append(f"u.{self.ident(province)} AS province_id")

        if metric == "vaccination" and self.has_table("gis_vaccination_performances"):
            t="gis_vaccination_performances"; fk=self.pick(t,"epidemiology_unit_id")
            v=self.pick(t,"vaccinated_animals","vaccinated_count","performed_count")
            e=self.pick(t,"eligible_animals","eligible_count","target_animals","planned_animals")
            if fk and v:
                eligible = f"COALESCE(SUM(p.{self.ident(e)}),0)" if e else "0"
                sql=f"""
                    SELECT {', '.join(base)},
                           COALESCE(SUM(p.{self.ident(v)}),0)::numeric AS value,
                           {eligible}::numeric AS target
                    FROM gis_epidemiology_units u
                    LEFT JOIN gis_vaccination_performances p ON p.{self.ident(fk)}=u.id
                    GROUP BY u.id, {name_sql}{', u.'+self.ident(county) if county else ''}{', u.'+self.ident(province) if province else ''}
                    ORDER BY value DESC
                """
                rows=self._rows(sql)
                for r in rows:
                    r["progress_percent"]=round(float(r["value"])/float(r["target"])*100,2) if float(r["target"] or 0) else 0
                return rows

        metric_specs = {
            "disease_reports": ("gis_disease_reports", "report_date"),
            "care": ("gis_enable_cares", "care_date"),
            "lab": ("gis_laboratory_results", "sampling_date"),
            "samples": ("gis_send_sample_details", "sampling_date"),
            "spraying": ("gis_spraying", "spraying_date"),
            "operations": ("gis_operation_history", "operation_date"),
        }
        if metric in metric_specs:
            t, preferred = metric_specs[metric]
            if self.has_table(t):
                fk=self.pick(t,"epidemiology_unit_id")
                d=self.pick(t,preferred,"operation_date","date","created_at","event_date")
                if fk:
                    sql=f"""
                        SELECT {', '.join(base)}, COUNT(x.id)::numeric AS value
                        FROM gis_epidemiology_units u
                        LEFT JOIN {self.ident(t)} x ON x.{self.ident(fk)}=u.id
                        GROUP BY u.id, {name_sql}{', u.'+self.ident(county) if county else ''}{', u.'+self.ident(province) if province else ''}
                        ORDER BY value DESC
                    """
                    return self._rows(sql)

        # all = all live operation events, assembled from the same source tables
        rows = []
        for r in self.map_points():
            uid=int(r["id"])
            hist=self.operation_history(uid)
            rows.append({
                "unit_id":uid,
                "unit_name":r.get("name"),
                "county_id":r.get("county_id"),
                "province_id":r.get("province_id"),
                "value":len(hist),
            })
        rows.sort(key=lambda x: x["value"], reverse=True)
        return rows

    # ---------- map data ----------

    def map_points(self):
        t = "gis_epidemiology_units"
        if not self.has_table(t):
            return []
        lat = self.pick(t, "latitude","lat")
        lon = self.pick(t, "longitude","lon","lng")
        name = self.pick(t, "unit_name","name","title","name_fa","unit_title")
        county = self.pick(t, "county_id")
        province = self.pick(t, "province_id")
        if not lat or not lon:
            return []
        rows = self._rows(f"""
            SELECT id,
                   {self.ident(name) if name else 'CAST(id AS text)'} AS name,
                   {self.ident(lat)} AS latitude,
                   {self.ident(lon)} AS longitude,
                   {self.ident(county) if county else 'NULL'} AS county_id,
                   {self.ident(province) if province else 'NULL'} AS province_id
            FROM {self.ident(t)}
            WHERE {self.ident(lat)} IS NOT NULL AND {self.ident(lon)} IS NOT NULL
            LIMIT 20000
        """)
        return rows