#requires -Version 5.1
<#
PVIMP - Live KPI Dashboard Builder
----------------------------------
Target:
  D:\pvimp_backend
  D:\pvimp_backend\pvimp_frontend

What this script does:
  1) Creates a non-destructive backup of files it changes.
  2) Creates a live PostgreSQL-backed KPI service/router.
  3) Creates a React KPI dashboard with SVG charts and unit drill-down.
  4) Adds a route /live-kpi when a conventional React-Router <Routes> setup is detected.
  5) Runs Python compile/import checks and frontend build.
  6) Does NOT create cached KPI values: every API request reads the current DB.

Important:
  - It does not delete data.
  - It does not create fake KPI rows.
  - Empty source tables produce zero/empty charts.
  - Vaccination predictions are kept at their real scope (county/disease); they
    are never falsely attributed to an individual unit.
#>

$ErrorActionPreference = "Stop"

$BackendRoot  = "D:\pvimp_backend"
$FrontendRoot = Join-Path $BackendRoot "pvimp_frontend"
$ApiDir       = Join-Path $BackendRoot "app\api\v1\endpoints"
$ServiceDir   = Join-Path $BackendRoot "app\services\gis"
$PageDir      = Join-Path $FrontendRoot "src\pages"
$BackupRoot   = Join-Path $BackendRoot "_dashboard_kpi_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

if (-not (Test-Path $BackendRoot)) {
    throw "Backend path not found: $BackendRoot"
}
if (-not (Test-Path $FrontendRoot)) {
    throw "Frontend path not found: $FrontendRoot"
}

New-Item -ItemType Directory -Force -Path $ApiDir,$ServiceDir,$PageDir | Out-Null
New-Item -ItemType Directory -Force -Path $BackupRoot | Out-Null

function Backup-IfExists([string]$Path) {
    if (Test-Path $Path) {
        $relative = $Path.Substring($BackendRoot.Length).TrimStart('\')
        $dest = Join-Path $BackupRoot $relative
        $destDir = Split-Path $dest -Parent
        New-Item -ItemType Directory -Force -Path $destDir | Out-Null
        Copy-Item $Path $dest -Force
        Write-Host "Backup: $Path -> $dest" -ForegroundColor DarkGray
    }
}

function Write-Utf8([string]$Path,[string]$Content) {
    $dir = Split-Path $Path -Parent
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    # UTF-8 without BOM; safe for Python and TypeScript.
    [System.IO.File]::WriteAllText($Path,$Content,(New-Object System.Text.UTF8Encoding($false)))
    Write-Host "Wrote: $Path" -ForegroundColor Green
}

$ServiceFile = Join-Path $ServiceDir "live_dashboard_kpi_service.py"
$RouterFile  = Join-Path $ApiDir "gis_dashboard_kpi.py"
$PageFile    = Join-Path $PageDir "LiveKpiDashboard.tsx"
$CssFile     = Join-Path $PageDir "LiveKpiDashboard.css"

Backup-IfExists $ServiceFile
Backup-IfExists $RouterFile
Backup-IfExists $PageFile
Backup-IfExists $CssFile

$service = @'
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
                f"OR LOWER(COALESCE({self.ident(lab_status)},'')) LIKE '%مثبت%'"
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
                return [{"name": r["name"] or "بدون نام", "value": float(r["value"])} for r in rows]
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
                    "name": r["name"] or "بدون نام",
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
            return {"unit": None, "error": "واحد پیدا نشد"}
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
            ("gis_enable_cares", "care_date", "مراقبت"),
            ("gis_vaccination_performances", "vaccination_date", "واکسیناسیون"),
            ("gis_laboratory_results", "sampling_date", "آزمایشگاه"),
            ("gis_send_sample_details", "sampling_date", "ارسال نمونه"),
            ("gis_slaughter_disposals", "disposal_date", "کشتار/امحاء"),
            ("gis_spraying", "spraying_date", "سمپاشی"),
            ("gis_vaccine_distributions", "distribution_date", "توزیع واکسن"),
            ("gis_vaccine_disposals", "disposal_date", "دفع واکسن"),
            ("gis_disease_reports", "report_date", "گزارش بیماری"),
            ("gis_disease_occurrences", "occurrence_date", "وقوع بیماری"),
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
                "name": r["name"] or "بدون نام",
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
'@

$router = @'
from __future__ import annotations

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.gis.live_dashboard_kpi_service import LiveDashboardKPIService

router = APIRouter(prefix="/gis/dashboard/kpi", tags=["GIS Dashboard KPI"])


@router.get("/overview")
def dashboard_overview(
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    return LiveDashboardKPIService(db).overview(start, end)


@router.get("/units/{unit_id}")
def dashboard_unit(unit_id: int, db: Session = Depends(get_db)):
    return LiveDashboardKPIService(db).unit_detail(unit_id)


@router.get("/counties/{county_id}")
def dashboard_county(county_id: int, db: Session = Depends(get_db)):
    return LiveDashboardKPIService(db).county_detail(county_id)


@router.get("/drilldown/{metric}")
def dashboard_metric_drilldown(metric: str, db: Session = Depends(get_db)):
    allowed = {"all","vaccination","disease_reports","care","lab","samples","spraying","operations"}
    if metric not in allowed:
        return {"metric": metric, "units": [], "error": "unsupported metric"}
    return {"metric": metric, "units": LiveDashboardKPIService(db).metric_units(metric)}


@router.get("/map")
def dashboard_map(db: Session = Depends(get_db)):
    return {"live": True, "points": LiveDashboardKPIService(db).map_points()}
'@

$css = @'
:root {
  --kpi-bg:#061526;
  --kpi-panel:#091d31;
  --kpi-border:#0b78a5;
  --kpi-cyan:#19d9ff;
  --kpi-green:#35e28b;
  --kpi-yellow:#f4c542;
  --kpi-red:#ff476b;
  --kpi-text:#eaf8ff;
  --kpi-muted:#88a9ba;
}
.live-kpi-page{direction:rtl;min-height:100vh;padding:18px;background:radial-gradient(circle at 50% 0,#0a2740 0,#03101d 52%,#020a12 100%);color:var(--kpi-text);font-family:Tahoma,Arial,sans-serif}
.live-kpi-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:14px}
.live-kpi-head h1{font-size:24px;margin:0}
.live-kpi-head p{margin:5px 0 0;color:var(--kpi-muted);font-size:12px}
.live-kpi-live{border:1px solid #1e9cbd;border-radius:999px;padding:7px 12px;color:#77ffd1;background:#062c2b;font-size:12px}
.kpi-grid{display:grid;grid-template-columns:repeat(6,minmax(145px,1fr));gap:10px;margin-bottom:12px}
.kpi-card,.kpi-panel{background:linear-gradient(180deg,rgba(10,34,54,.96),rgba(4,20,34,.96));border:1px solid rgba(20,150,190,.5);border-radius:10px;box-shadow:0 0 22px rgba(0,170,220,.08)}
.kpi-card{padding:13px;min-height:92px}
.kpi-card .label{color:#9fc2d0;font-size:12px}
.kpi-card .value{font-size:25px;font-weight:800;margin-top:9px;color:#9beeff}
.kpi-card .sub{font-size:11px;color:var(--kpi-green);margin-top:5px}
.kpi-layout{display:grid;grid-template-columns:2fr 1fr;gap:12px}
.kpi-panel{padding:13px;margin-bottom:12px}
.kpi-panel h2{font-size:15px;margin:0 0 10px}
.chart-box{height:240px;position:relative}
.chart-box.tall{height:310px}
.kpi-tabs{display:flex;gap:7px;overflow:auto;margin-bottom:12px}
.kpi-tab{border:1px solid #145a78;background:#061827;color:#c7e7f1;border-radius:7px;padding:8px 12px;cursor:pointer;white-space:nowrap}
.kpi-tab.active{background:#0a4260;border-color:#20c9f1;color:#fff}
.kpi-two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.kpi-three{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.kpi-table{width:100%;border-collapse:collapse;font-size:12px}
.kpi-table th,.kpi-table td{padding:8px;border-bottom:1px solid #153b50;text-align:right}
.kpi-table th{color:#84c7d9}
.kpi-click{cursor:pointer}
.kpi-click:hover{background:#0b2a3d}
.unit-search{display:flex;gap:8px;margin-bottom:10px}
.unit-search input{flex:1;background:#04111d;border:1px solid #15536c;color:#fff;border-radius:6px;padding:9px}
.unit-list{max-height:430px;overflow:auto}
.unit-row{display:flex;justify-content:space-between;gap:10px;padding:9px;border-bottom:1px solid #153548;cursor:pointer}
.unit-row:hover{background:#0a2639}
.badge{border-radius:999px;padding:4px 8px;font-size:10px}
.badge.good{background:#073e30;color:#6ff0bb}
.badge.warn{background:#4b3c08;color:#ffe37a}
.badge.bad{background:#4b1020;color:#ff9ab0}
.back{cursor:pointer;color:#5be5ff;margin-bottom:10px;display:inline-block}
@media(max-width:1100px){.kpi-grid{grid-template-columns:repeat(3,1fr)}.kpi-layout,.kpi-two,.kpi-three{grid-template-columns:1fr}}
@media(max-width:650px){.kpi-grid{grid-template-columns:repeat(2,1fr)}}
'@

$tsx = @'
import React, { useEffect, useMemo, useState } from "react";
import "./LiveKpiDashboard.css";

const API_BASE = "/api/v1/gis/dashboard/kpi";

type AnyObj = Record<string, any>;

const nf = new Intl.NumberFormat("fa-IR", { maximumFractionDigits: 1 });
const pct = (v:number) => `${nf.format(Number(v||0))}%`;
const num = (v:number) => nf.format(Number(v||0));

function api(path:string){
  return fetch(`${API_BASE}${path}`, { credentials:"include" }).then(async r => {
    if(!r.ok) throw new Error(`${r.status} ${await r.text()}`);
    return r.json();
  });
}

function LineChart({data, color="#19d9ff", height=220}:{data:any[],color?:string,height?:number}){
  const w=760,h=height,p=34;
  if(!data?.length) return <div style={{padding:30,color:"#789"}}>داده‌ای برای نمودار وجود ندارد</div>;
  const vals=data.map(x=>Number(x.value||0)); const max=Math.max(...vals,1);
  const pts=data.map((x,i)=>{
    const xx=p+(i*Math.max(1,(w-2*p)/(Math.max(1,data.length-1))));
    const yy=h-p-(Number(x.value||0)/max)*(h-2*p);
    return `${xx},${yy}`;
  }).join(" ");
  return <svg viewBox={`0 0 ${w} ${h}`} width="100%" height={height}>
    <line x1={p} x2={w-p} y1={h-p} y2={h-p} stroke="#173b50"/>
    <polyline points={pts} fill="none" stroke={color} strokeWidth="4"/>
    {data.map((x,i)=>{const [xx,yy]=pts.split(" ")[i].split(",");return <circle key={i} cx={xx} cy={yy} r="4" fill={color}/>})}
    {data.map((x,i)=><text key={`t${i}`} x={p+i*Math.max(1,(w-2*p)/(Math.max(1,data.length-1)))} y={h-10} fill="#7195a8" fontSize="11" textAnchor="middle">{String(x.period).slice(5)}</text>)}
  </svg>;
}

function BarChart({data, valueKey="value", color="#19d9ff"}:{data:any[],valueKey?:string,color?:string}){
  if(!data?.length) return <div style={{padding:30,color:"#789"}}>داده‌ای برای نمودار وجود ندارد</div>;
  const max=Math.max(...data.map(x=>Number(x[valueKey]||0)),1);
  return <div style={{display:"flex",alignItems:"end",gap:10,height:220,padding:"10px 5px 20px"}}>
    {data.slice(0,12).map((x,i)=>{
      const v=Number(x[valueKey]||0); const h=Math.max(5,v/max*165);
      return <div key={i} style={{flex:1,textAlign:"center",minWidth:35}}>
        <div title={num(v)} style={{height:h,background:`linear-gradient(180deg,${color},#07506b)`,borderRadius:"5px 5px 0 0"}}/>
        <div style={{fontSize:10,color:"#8caebe",marginTop:5,overflow:"hidden"}}>{String(x.name||x.period||"").slice(0,12)}</div>
      </div>
    })}
  </div>;
}

function Donut({value,max,color="#19d9ff"}:{value:number,max:number,color?:string}){
  const p=Math.min(100,max?value/max*100:0);
  return <div style={{display:"flex",justifyContent:"center",alignItems:"center",height:220}}>
    <div style={{width:140,height:140,borderRadius:"50%",background:`conic-gradient(${color} ${p}%,#183748 0)` ,display:"grid",placeItems:"center"}}>
      <div style={{width:96,height:96,borderRadius:"50%",background:"#071b2c",display:"grid",placeItems:"center",textAlign:"center"}}>
        <strong style={{fontSize:22}}>{pct(p)}</strong><small style={{color:"#779"}}>پیشرفت</small>
      </div>
    </div>
  </div>;
}

function Card({label,value,sub,onClick}:{label:string,value:any,sub?:string,onClick?:()=>void}){
  return <div className="kpi-card" onClick={onClick} style={onClick?{cursor:"pointer"}:undefined}>
    <div className="label">{label}</div><div className="value">{value}</div>{sub&&<div className="sub">{sub}</div>}
  </div>
}

export default function LiveKpiDashboard(){
  const [data,setData]=useState<AnyObj|null>(null);
  const [tab,setTab]=useState("overview");
  const [unitId,setUnitId]=useState<number|null>(null);
  const [unit,setUnit]=useState<AnyObj|null>(null);
  const [unitMetric,setUnitMetric]=useState("all");
  const [loading,setLoading]=useState(true);
  const [error,setError]=useState("");
  const [refresh,setRefresh]=useState(0);

  useEffect(()=>{
    setLoading(true); setError("");
    api("/overview").then(setData).catch(e=>setError(String(e))).finally(()=>setLoading(false));
  },[refresh]);

  useEffect(()=>{
    if(unitId==null){setUnit(null);return}
    setLoading(true); api(`/units/${unitId}`).then(setUnit).catch(e=>setError(String(e))).finally(()=>setLoading(false));
  },[unitId]);

  const c=data?.cards||{};
  const series=data?.series||{};
  const diseases=data?.breakdowns?.disease_by_name||[];
  const counties=data?.breakdowns?.vaccination_by_county||[];

  const openMetric=(metric:string)=>{setUnitMetric(metric);setTab("units")};

  const tabs=[
    ["overview","نمای کلی"],
    ["disease","بیماری و اپیدمیولوژی"],
    ["care","مراقبت فعال"],
    ["lab","آزمایشگاه و نمونه"],
    ["vaccination","واکسیناسیون"],
    ["inventory","زنجیره واکسن"],
    ["units","واحدها و Drill-down"],
  ];

  if(loading && !data && !unit) return <div className="live-kpi-page">در حال دریافت KPIهای زنده از PostgreSQL...</div>;
  if(error && !data) return <div className="live-kpi-page"><div className="kpi-panel"><b>خطا:</b> {error}</div></div>;

  if(unitId!=null && unit){
    const v=unit.vaccination||{};
    const ops=unit.operation_counts||[];
    return <div className="live-kpi-page">
      <span className="back" onClick={()=>setUnitId(null)}>← بازگشت به داشبورد</span>
      <div className="live-kpi-head">
        <div><h1>داشبورد واحد: {unit.unit?.unit_name||`واحد ${unitId}`}</h1><p>تمام عملیات ثبت‌شده برای این واحد + وضعیت پیشرفت واقعی</p></div>
        <span className="live-kpi-live">● LIVE</span>
      </div>
      <div className="kpi-grid">
        <Card label="دام واجد شرایط واکسیناسیون" value={num(v.eligible)}/>
        <Card label="دام واکسینه‌شده" value={num(v.vaccinated)}/>
        <Card label="باقی‌مانده" value={num(v.remaining)}/>
        <Card label="پیشرفت واکسیناسیون" value={pct(v.coverage_percent)} sub="از داده واقعی واحد"/>
        <Card label="تعداد عملیات ثبت‌شده" value={num(unit.operation_history?.length||0)}/>
        <Card label="پیش‌بینی شهرستان" value={num((unit.county_predictions||[])[0]?.value||0)} sub="scope: شهرستان"/>
      </div>
      <div className="kpi-two">
        <div className="kpi-panel"><h2>پیشرفت واکسیناسیون واحد</h2><Donut value={v.vaccinated||0} max={v.eligible||0}/></div>
        <div className="kpi-panel"><h2>تعداد عملیات به تفکیک نوع</h2><BarChart data={ops} color="#35e28b"/></div>
      </div>
      <div className="kpi-panel"><h2>تاریخچه عملیات واحد</h2>
        <table className="kpi-table"><thead><tr><th>تاریخ</th><th>عملیات</th></tr></thead>
        <tbody>{(unit.operation_history||[]).map((x:any,i:number)=><tr key={i}><td>{String(x.event_date||"").slice(0,19)}</td><td>{x.operation_type}</td></tr>)}</tbody></table>
      </div>
    </div>
  }

  return <div className="live-kpi-page">
    <div className="live-kpi-head">
      <div><h1>داشبورد زنده کنترل بیماری و عملیات دامپزشکی</h1><p>تمام اعداد در هر درخواست مستقیماً از PostgreSQL خوانده می‌شوند.</p></div>
      <button className="kpi-tab" onClick={()=>setRefresh(x=>x+1)}>↻ بروزرسانی</button>
    </div>

    <div className="kpi-tabs">{tabs.map(t=><button key={t[0]} className={`kpi-tab ${tab===t[0]?"active":""}`} onClick={()=>setTab(t[0])}>{t[1]}</button>)}</div>

    {tab==="overview" && <><div className="kpi-grid">
      <Card label="واحدهای اپیدمیولوژیک" value={num(c.total_units)} onClick={()=>openMetric("all")}/>
      <Card label="واحدهای فعال" value={num(c.active_units)}/>
      <Card label="جمعیت دام تحت پوشش" value={num(c.total_livestock)}/>
      <Card label="گزارش بیماری" value={num(c.disease_reports)} onClick={()=>openMetric("disease_reports")}/>
      <Card label="مراقبت فعال" value={num(c.care_records)} onClick={()=>openMetric("care")}/>
      <Card label="واکسیناسیون انجام‌شده" value={num(c.vaccinated_animals)} onClick={()=>openMetric("vaccination")}/>
      <Card label="پوشش واکسیناسیون" value={pct(c.vaccination_coverage)}/>
      <Card label="باقی‌مانده واکسیناسیون" value={num(c.vaccination_remaining)} onClick={()=>openMetric("vaccination")}/>
      <Card label="نتایج آزمایشگاهی" value={num(c.lab_results)} onClick={()=>openMetric("lab")}/>
      <Card label="نرخ مثبت آزمایشگاه" value={pct(c.lab_positive_rate)}/>
      <Card label="موجودی واکسن" value={num(c.inventory_packages)}/>
      <Card label="واکسن نزدیک انقضا" value={num(c.expiring_30_days)}/>
    </div>
    <div className="kpi-layout">
      <div><div className="kpi-panel"><h2>روند واکسیناسیون</h2><div className="chart-box"><LineChart data={series.vaccination}/></div></div>
      <div className="kpi-two"><div className="kpi-panel"><h2>روند گزارش بیماری</h2><LineChart data={series.disease_reports} color="#ff476b"/></div><div className="kpi-panel"><h2>موارد مثبت مراقبت</h2><LineChart data={series.care_positive} color="#35e28b"/></div></div></div>
      <div><div className="kpi-panel"><h2>پوشش واکسیناسیون</h2><Donut value={c.vaccinated_animals||0} max={c.eligible_animals||0}/></div>
      <div className="kpi-panel"><h2>بیماری‌های پرتکرار</h2><BarChart data={diseases} color="#ff476b"/></div></div>
    </div>
    <div className="kpi-panel"><h2>مقایسه عملکرد واکسیناسیون شهرستان‌ها</h2><BarChart data={counties.map((x:any)=>({...x,value:x.coverage}))} color="#f4c542"/></div>
    </>}

    {tab==="disease" && <div className="kpi-layout"><div><div className="kpi-grid"><Card label="گزارش بیماری" value={num(c.disease_reports)} onClick={()=>openMetric("disease_reports")}/><Card label="وقوع بیماری" value={num(c.disease_occurrences)}/><Card label="بیماری‌های ثبت‌شده" value={num(c.diseases)}/><Card label="کانون فعال" value={num(c.active_outbreaks)}/></div><div className="kpi-panel"><h2>روند گزارش‌های بیماری</h2><LineChart data={series.disease_reports} color="#ff476b" height={300}/></div></div><div className="kpi-panel"><h2>توزیع بیماری‌ها</h2><BarChart data={diseases} color="#ff476b"/></div></div>}

    {tab==="care" && <><div className="kpi-grid"><Card label="رکورد مراقبت" value={num(c.care_records)}/><Card label="دام بررسی‌شده" value={num(c.care_animals)}/><Card label="مثبت" value={num(c.care_positive)}/><Card label="منفی" value={num(c.care_negative)}/><Card label="مشکوک" value={num(c.care_suspicious)}/><Card label="نرخ مثبت" value={pct(c.care_positive_rate)}/></div><div className="kpi-panel"><h2>روند موارد مثبت مراقبت</h2><LineChart data={series.care_positive} color="#35e28b" height={300}/></div></>}

    {tab==="lab" && <><div className="kpi-grid"><Card label="نتایج آزمایشگاهی" value={num(c.lab_results)} onClick={()=>openMetric("lab")}/><Card label="نمونه آزمایشگاه" value={num(c.lab_samples)}/><Card label="نمونه ارسال‌شده" value={num(c.sent_samples)}/><Card label="مثبت" value={num(c.lab_positive)}/><Card label="نرخ مثبت" value={pct(c.lab_positive_rate)}/></div><div className="kpi-two"><div className="kpi-panel"><h2>وضعیت نمونه و نتیجه</h2><BarChart data={[{name:"نتیجه",value:c.lab_results},{name:"ارسال",value:c.sent_samples},{name:"مثبت",value:c.lab_positive}]} color="#19d9ff"/></div><div className="kpi-panel"><h2>توضیح Drill-down</h2><p style={{lineHeight:2,color:"#9eb9c5"}}>از صفحه واحدها می‌توان تا واحد اپیدمیولوژیک رفت و تاریخچه عملیات همان واحد را دید. جدول فقط در انتهای Drill-down استفاده شده است.</p></div></div></>}

    {tab==="vaccination" && <><div className="kpi-grid"><Card label="دام واجد شرایط" value={num(c.eligible_animals)}/><Card label="واکسینه‌شده" value={num(c.vaccinated_animals)}/><Card label="باقی‌مانده" value={num(c.vaccination_remaining)}/><Card label="پوشش" value={pct(c.vaccination_coverage)}/><Card label="توزیع بسته" value={num(c.distributed_packages)}/><Card label="دفع بسته" value={num(c.disposed_packages)}/></div><div className="kpi-two"><div className="kpi-panel"><h2>روند واکسیناسیون</h2><LineChart data={series.vaccination} height={300}/></div><div className="kpi-panel"><h2>پیشرفت</h2><Donut value={c.vaccinated_animals||0} max={c.eligible_animals||0} color="#35e28b"/></div></div><div className="kpi-panel"><h2>مقایسه شهرستان‌ها</h2><BarChart data={counties.map((x:any)=>({...x,value:x.coverage}))} color="#f4c542"/></div></>}

    {tab==="inventory" && <><div className="kpi-grid"><Card label="موجودی بسته" value={num(c.inventory_packages)}/><Card label="توزیع‌شده" value={num(c.distributed_packages)}/><Card label="دفع‌شده" value={num(c.disposed_packages)}/><Card label="نزدیک انقضا (۳۰ روز)" value={num(c.expiring_30_days)}/></div><div className="kpi-panel"><h2>جریان زنجیره واکسن</h2><BarChart data={[{name:"موجودی",value:c.inventory_packages},{name:"توزیع",value:c.distributed_packages},{name:"دفع",value:c.disposed_packages},{name:"انقضای نزدیک",value:c.expiring_30_days}]} color="#19d9ff"/></div></>}

    {tab==="units" && <UnitExplorer onOpen={setUnitId} metric={unitMetric}/>}
  </div>
}

function UnitExplorer({onOpen,metric}:{onOpen:(id:number)=>void,metric:string}){
  const [q,setQ]=useState("");
  const [rows,setRows]=useState<any[]>([]);
  const [loading,setLoading]=useState(false);

  useEffect(()=>{
    setLoading(true);
    api(`/drilldown/${metric}`).then(x=>setRows(x.units||[])).finally(()=>setLoading(false))
  },[metric]);

  const list=useMemo(()=>rows.filter(x=>!q||String(x.unit_name||"").includes(q)).slice(0,1000),[rows,q]);
  const title={
    all:"همه عملیات",
    vaccination:"واکسیناسیون",
    disease_reports:"گزارش بیماری",
    care:"مراقبت",
    lab:"آزمایشگاه",
    samples:"ارسال نمونه",
    spraying:"سمپاشی",
    operations:"تاریخچه عملیات",
  }[metric]||"واحدها";

  return <div>
    <div className="kpi-panel">
      <h2>Drill-down واحدها — {title}</h2>
      <p style={{color:"#789",fontSize:12}}>کلیک روی هر KPI، واحدهای تشکیل‌دهنده همان KPI را نشان می‌دهد. با کلیک روی واحد، تاریخچه عملیات و پیشرفت فیزیکی نمایش داده می‌شود.</p>
      <div className="unit-search"><input value={q} onChange={e=>setQ(e.target.value)} placeholder="جستجوی نام واحد..."/></div>
      {loading?<div>در حال دریافت داده زنده...</div>:
       <div className="unit-list">{list.map(x=>
         <div className="unit-row" key={x.unit_id} onClick={()=>onOpen(Number(x.unit_id))}>
           <span>{x.unit_name||`واحد ${x.unit_id}`}</span>
           <span>{num(x.value)} {metric==="vaccination"&&<span className={`badge ${Number(x.progress_percent||0)>=80?"good":Number(x.progress_percent||0)>=50?"warn":"bad"}`}>{pct(x.progress_percent||0)}</span>}</span>
         </div>)}
       </div>}
    </div>
  </div>
}

'@

Write-Utf8 $ServiceFile $service
Write-Utf8 $RouterFile $router
Write-Utf8 $CssFile $css
Write-Utf8 $PageFile $tsx

# ---------------- API router auto-registration ----------------
$apiCandidates = @(
    (Join-Path $BackendRoot "app\api\v1\api.py"),
    (Join-Path $BackendRoot "app\api\v1\router.py"),
    (Join-Path $BackendRoot "app\api\v1\__init__.py")
)
$apiTarget = $apiCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if ($apiTarget) {
    Backup-IfExists $apiTarget
    $apiText = Get-Content $apiTarget -Raw -Encoding UTF8
    $importLine = "from app.api.v1.endpoints.gis_dashboard_kpi import router as gis_dashboard_kpi_router"
    $includeLine = "api_router.include_router(gis_dashboard_kpi_router)"

    if ($apiText -notmatch "gis_dashboard_kpi_router") {
        if ($apiText -notmatch [regex]::Escape($importLine)) {
            $apiText = $importLine + "`r`n" + $apiText
        }

        if ($apiText -match "api_router\.include_router\(") {
            $apiText = $apiText.TrimEnd() + "`r`n" + $includeLine + "`r`n"
        } elseif ($apiText -match "router\.include_router\(") {
            $apiText = $apiText.TrimEnd() + "`r`n" + $includeLine + "`r`n"
        } else {
            $apiText = $apiText.TrimEnd() + "`r`n" + $includeLine + "`r`n"
        }
        Write-Utf8 $apiTarget $apiText
        Write-Host "Registered KPI router in $apiTarget" -ForegroundColor Green
    } else {
        Write-Host "KPI router already registered in $apiTarget" -ForegroundColor Yellow
    }
} else {
    Write-Host "WARNING: Could not auto-detect app/api/v1 router file." -ForegroundColor Yellow
    Write-Host "The KPI files were created; router registration must be added manually."
}

# ---------------- Frontend route auto-registration ----------------
$appCandidates = Get-ChildItem (Join-Path $FrontendRoot "src") -Recurse -File -Include *.tsx,*.jsx -ErrorAction SilentlyContinue |
    Select-String -Pattern "<Routes|createBrowserRouter|createHashRouter" -List |
    Select-Object -ExpandProperty Path

$appTarget = $appCandidates | Where-Object { $_ -match "\\App\.(tsx|jsx)$" } | Select-Object -First 1
if (-not $appTarget) { $appTarget = $appCandidates | Select-Object -First 1 }

if ($appTarget) {
    Backup-IfExists $appTarget
    $appText = Get-Content $appTarget -Raw -Encoding UTF8
    if ($appText -notmatch "LiveKpiDashboard") {
        $import = 'import LiveKpiDashboard from "../pages/LiveKpiDashboard";'
        if ($appText -notmatch [regex]::Escape($import)) {
            $lastImport = [regex]::Matches($appText, '(?m)^import .+;$') | Select-Object -Last 1
            if ($lastImport) {
                $idx = $lastImport.Index + $lastImport.Length
                $appText = $appText.Insert($idx, "`r`n$import")
            } else {
                $appText = $import + "`r`n" + $appText
            }
        }

        if ($appText -match "<Routes") {
            $route = '<Route path="/live-kpi" element={<LiveKpiDashboard />} />'
            $pos = $appText.IndexOf("</Routes>")
            if ($pos -ge 0) {
                $appText = $appText.Insert($pos, "    $route`r`n")
                Write-Utf8 $appTarget $appText
                Write-Host "Registered frontend route /live-kpi in $appTarget" -ForegroundColor Green
            } else {
                Write-Host "WARNING: <Routes> found but </Routes> was not found." -ForegroundColor Yellow
            }
        } else {
            Write-Utf8 $appTarget $appText
            Write-Host "Frontend import added; router style is not conventional <Routes>." -ForegroundColor Yellow
        }
    } else {
        Write-Host "LiveKpiDashboard already registered." -ForegroundColor Yellow
    }
} else {
    Write-Host "WARNING: Could not detect React router file. Page was created at:" -ForegroundColor Yellow
    Write-Host $PageFile
}

# ---------------- Validation ----------------
Push-Location $BackendRoot
try {
    Write-Host "`n=== Python compile check ===" -ForegroundColor Cyan
    py -3.12 -m py_compile $ServiceFile $RouterFile
    if ($LASTEXITCODE -ne 0) {
        throw "Python compile failed with exit code $LASTEXITCODE"
    }
    Write-Host "Python compile: OK" -ForegroundColor Green

    Write-Host "`n=== FastAPI import check ===" -ForegroundColor Cyan
    py -3.12 -c "from app.api.v1.endpoints.gis_dashboard_kpi import router; print('router import OK:', router.prefix)"
    if ($LASTEXITCODE -ne 0) {
        throw "FastAPI router import failed with exit code $LASTEXITCODE"
    }
    Write-Host "FastAPI router import: OK" -ForegroundColor Green
}
finally {
    Pop-Location
}

Push-Location $FrontendRoot
try {
    Write-Host "`n=== Frontend build ===" -ForegroundColor Cyan
    if (Test-Path "package.json") {
        npm run build
        if ($LASTEXITCODE -ne 0) {
            throw "Frontend build failed with exit code $LASTEXITCODE"
        }
        Write-Host "Frontend build: OK" -ForegroundColor Green
    } else {
        Write-Host "package.json not found; frontend build skipped." -ForegroundColor Yellow
    }
}
finally {
    Pop-Location
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "LIVE KPI DASHBOARD BUILD FINISHED" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Backup: $BackupRoot"
Write-Host "Backend service: $ServiceFile"
Write-Host "Backend router : $RouterFile"
Write-Host "Frontend page  : $PageFile"
Write-Host ""
Write-Host "API:"
Write-Host "  /api/v1/gis/dashboard/kpi/overview"
Write-Host "  /api/v1/gis/dashboard/kpi/drilldown/{metric}"
Write-Host "  /api/v1/gis/dashboard/kpi/units/{unit_id}"
Write-Host "  /api/v1/gis/dashboard/kpi/counties/{county_id}"
Write-Host "  /api/v1/gis/dashboard/kpi/map"
Write-Host ""
Write-Host "Frontend:"
Write-Host "  /live-kpi"
Write-Host ""
Write-Host "IMPORTANT: restart Uvicorn after the script finishes."
Write-Host "============================================================" -ForegroundColor Cyan
