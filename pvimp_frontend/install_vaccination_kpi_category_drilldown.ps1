# PVIMP installer - compatible with Windows PowerShell 5.1
<#
    PVIMP - Vaccination KPI Category / Drill-down installer
    Project root: D:\pvimp_backend

    This script:
      1) Reads the supplied 10-sheet Excel workbook.
      2) Generates a typed TS data catalog from the workbook.
      3) Creates a chart-first vaccination KPI category page.
      4) Adds drill-down routes:
           category -> indicator -> county -> units
      5) Adds a period selector (3 / 4 / 5 / 12 months).
         4-month values come from the workbook (source date: 1405/05/01).
         3/5/12-month editable values are stored locally until backend
         persistence is added.
      6) Uses the existing vaccination KPI API for unit-level drill-down
         whenever an API vaccine type can be matched.
      7) Adds a safe entry button to the existing KPIAnalysis page.
      8) Creates backups before changing existing frontend files.
      9) Runs TypeScript build at the end.

    IMPORTANT:
      - Existing KPI endpoints/pages are not replaced.
      - VaccinationVaccineReport.tsx is not replaced.
      - The workbook is treated as the source of the category structure,
        targets and current 4-month performance.
#>

$ErrorActionPreference = "Stop"

$ProjectRoot = "D:\pvimp_backend"
$FrontendRoot = Join-Path $ProjectRoot "pvimp_frontend"
$SrcRoot = Join-Path $FrontendRoot "src"
$DataRoot = Join-Path $SrcRoot "data"
$PagesRoot = Join-Path $SrcRoot "pages"
$RouterFile = Join-Path $SrcRoot "router\AppRouter.tsx"
$KpiFile = Join-Path $PagesRoot "KPIAnalysis.tsx"

if (-not (Test-Path $ProjectRoot)) {
    throw "Project root not found: $ProjectRoot"
}

if (-not (Test-Path $FrontendRoot)) {
    throw "Frontend root not found: $FrontendRoot"
}

$python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    $python = "python"
}

New-Item -ItemType Directory -Force -Path $DataRoot | Out-Null
New-Item -ItemType Directory -Force -Path $PagesRoot | Out-Null

# ------------------------------------------------------------
# 1. Locate workbook
# ------------------------------------------------------------
$workbookCandidates = @(
    (Join-Path $ProjectRoot "عملکرد واکسيناسيون، پايش و مراقبت استان و شهرستان.xlsx"),
    (Join-Path $ProjectRoot "xlsx\عملکرد واکسيناسيون، پايش و مراقبت استان و شهرستان.xlsx"),
    (Join-Path $ProjectRoot "docs\عملکرد واکسيناسيون، پايش و مراقبت استان و شهرستان.xlsx"),
    (Join-Path $ProjectRoot "uploads\عملکرد واکسيناسيون، پايش و مراقبت استان و شهرستان.xlsx")
)

$workbook = $workbookCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $workbook) {
    $workbook = Get-ChildItem $ProjectRoot -Recurse -File -Filter "*.xlsx" -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -eq "عملکرد واکسيناسيون، پايش و مراقبت استان و شهرستان.xlsx" } |
        Select-Object -ExpandProperty FullName -First 1
}

if (-not $workbook) {
    throw "Workbook not found. Put 'عملکرد واکسيناسيون، پايش و مراقبت استان و شهرستان.xlsx' under D:\pvimp_backend and run again."
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " PVIMP - VACCINATION KPI CATEGORY INSTALLER" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Workbook: $workbook" -ForegroundColor Gray

# ------------------------------------------------------------
# 2. Backup existing files
# ------------------------------------------------------------
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupRoot = Join-Path $FrontendRoot "_backup_kpi_categories_$stamp"
New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null

foreach ($file in @($RouterFile, $KpiFile)) {
    if (Test-Path $file) {
        $relative = $file.Substring($FrontendRoot.Length).TrimStart("\")
        $dest = Join-Path $backupRoot $relative
        New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
        Copy-Item $file $dest -Force
    }
}

Write-Host "Backup created: $backupRoot" -ForegroundColor Green

# ------------------------------------------------------------
# 3. Generate workbook catalog using Python/openpyxl
# ------------------------------------------------------------
$parser = Join-Path $env:TEMP "pvimp_parse_kpi_workbook_$stamp.py"
$catalogFile = Join-Path $DataRoot "vaccinationKpiCatalog.ts"

$pythonCode = @'
from pathlib import Path
from openpyxl import load_workbook
import json
import re
import sys

workbook = Path(sys.argv[1])
output = Path(sys.argv[2])

expected = [
    "استان",
    "آبله",
    "بروسلوز دام سبک",
    "بروسلوز دام سنگین",
    "شاربن",
    "PPR",
    "هاری",
    "لمپی اسکین",
    "تب برفکی خارج از فاز",
    "تست سل، بروسلوز و مشمشه",
]

category_map = {
    "شاربن": "infectious",
    "تب برفکی خارج از فاز": "infectious",
    "آبله": "infectious",
    "لمپی اسکین": "infectious",
    "PPR": "infectious",
    "بروسلوز دام سبک": "zoonotic",
    "بروسلوز دام سنگین": "zoonotic",
    "هاری": "zoonotic",
    "تست سل، بروسلوز و مشمشه": "surveillance",
}

category_labels = {
    "infectious": "الف- عملکرد مبارزه با بیماری‌های واگیر",
    "zoonotic": "ب- عملکرد مبارزه با بیماری‌های مشترک",
    "surveillance": "ج- عملکرد پایش و مراقبت بیماری‌های مشترک",
}

def slug(value: str) -> str:
    value = value.strip()
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"[^0-9A-Za-z\u0600-\u06FF]+", "-", value)
    value = value.strip("-")
    return value or "indicator"

def num(value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except Exception:
        return None

def achievement(actual, target):
    a = num(actual)
    t = num(target)
    if a is None or t in (None, 0):
        return None
    return round(a * 100.0 / t, 2)

wb_formula = load_workbook(workbook, data_only=False)
wb_values = load_workbook(workbook, data_only=True)

missing = [x for x in expected if x not in wb_formula.sheetnames]
if missing:
    raise RuntimeError("Missing expected workbook sheets: " + ", ".join(missing))

blocks = []

for sheet_name in expected:
    if sheet_name == "استان":
        continue

    ws = wb_formula[sheet_name]
    wsv = wb_values[sheet_name]

    for r in range(1, ws.max_row + 1):
        headers = [ws.cell(r, c).value for c in range(1, ws.max_column + 1)]
        if not any(isinstance(v, str) and "نام شهرستان" in v for v in headers):
            continue

        title_row = r - 1
        title_values = [
            ws.cell(title_row, c).value for c in range(1, ws.max_column + 1)
        ]

        starts = [
            i + 1
            for i, v in enumerate(title_values)
            if isinstance(v, str) and v.strip()
        ]

        for start in starts:
            if ws.cell(r, start).value != "نام شهرستان":
                continue

            title = ws.cell(title_row, start).value
            title = str(title or "").strip()

            next_starts = [s for s in starts if s > start]
            end = min(next_starts) - 1 if next_starts else ws.max_column

            rows = []

            rr = r + 1
            while rr <= ws.max_row:
                county = ws.cell(rr, start).value
                if county in (None, ""):
                    break

                target_annual = wsv.cell(rr, start + 1).value
                target_period = wsv.cell(rr, start + 2).value
                actual = wsv.cell(rr, start + 3).value

                rows.append({
                    "county": str(county).strip(),
                    "annualTarget": num(target_annual),
                    "periodTarget": num(target_period),
                    "actual": num(actual),
                    "annualAchievement": achievement(actual, target_annual),
                    "periodAchievement": achievement(actual, target_period),
                })

                rr += 1

            indicator = title
            indicator = re.sub(r"^عملکرد واکسیناسیون\s+", "", indicator)
            indicator = re.sub(r"^عملکرد\s+", "", indicator)
            indicator = re.sub(r"\s+شهرستان$", "", indicator)
            indicator = re.sub(r"\s+", " ", indicator).strip()

            livestock = "سایر"
            low = title.lower()
            if "دام سبک" in title or "بره" in title or "میش" in title or "گوسفند" in title or "بزی" in title or "بز" in title:
                livestock = "دام سبک"
            if "گاو" in title or "گوساله" in title or "دام سنگین" in title:
                livestock = "دام سنگین"
            if "تک سمی" in title or "مشمشه" in title:
                livestock = "تک سمی"

            if "خونگیری" in title or "خـونگيري" in title:
                livestock = "دام سبک و سنگین"
            if "تست سل" in title:
                livestock = "دام سنگین"

            base_id = slug(sheet_name + "-" + title)

            blocks.append({
                "id": base_id,
                "categoryId": category_map.get(sheet_name, "surveillance"),
                "categoryLabel": category_labels.get(
                    category_map.get(sheet_name, "surveillance"),
                    ""
                ),
                "sheet": sheet_name,
                "title": title,
                "indicator": indicator,
                "livestockGroup": livestock,
                "sourcePeriodMonths": 4,
                "sourceAsOf": "1405/05/01",
                "rows": rows,
            })

catalog = {
    "sourceWorkbook": workbook.name,
    "generatedAt": __import__("datetime").datetime.now().isoformat(),
    "sourcePeriodMonths": 4,
    "sourceAsOf": "1405/05/01",
    "categories": [
        {
            "id": "infectious",
            "title": category_labels["infectious"],
            "description": "واکسن‌های بیماری‌های واگیر مطابق ساختار شیت‌های منبع",
        },
        {
            "id": "zoonotic",
            "title": category_labels["zoonotic"],
            "description": "واکسیناسیون بیماری‌های مشترک مطابق ساختار شیت‌های منبع",
        },
        {
            "id": "surveillance",
            "title": category_labels["surveillance"],
            "description": "پایش، مراقبت، خونگیری و آزمون‌های بیماری‌های مشترک",
        },
    ],
    "indicators": blocks,
}

typescript = (
    "/* AUTO-GENERATED FROM WORKBOOK - DO NOT EDIT MANUALLY */\n"
    "export type VaccinationKpiRow = {\n"
    "  county: string;\n"
    "  annualTarget: number | null;\n"
    "  periodTarget: number | null;\n"
    "  actual: number | null;\n"
    "  annualAchievement: number | null;\n"
    "  periodAchievement: number | null;\n"
    "};\n\n"
    "export type VaccinationKpiIndicator = {\n"
    "  id: string;\n"
    "  categoryId: string;\n"
    "  categoryLabel: string;\n"
    "  sheet: string;\n"
    "  title: string;\n"
    "  indicator: string;\n"
    "  livestockGroup: string;\n"
    "  sourcePeriodMonths: number;\n"
    "  sourceAsOf: string;\n"
    "  rows: readonly VaccinationKpiRow[];\n"
    "};\n\n"
    "export type VaccinationKpiCategory = {\n"
    "  id: string;\n"
    "  title: string;\n"
    "  description: string;\n"
    "};\n\n"
    f"export const vaccinationKpiSource = {json.dumps(catalog, ensure_ascii=False, indent=2)} as const;\n\n"
    "export const vaccinationKpiCategories = vaccinationKpiSource.categories as readonly VaccinationKpiCategory[];\n"
    "export const vaccinationKpiIndicators = vaccinationKpiSource.indicators as readonly VaccinationKpiIndicator[];\n"
)

output.write_text(typescript, encoding="utf-8")
print("Generated:", output)
print("Sheets:", ", ".join(expected))
print("Indicators:", len(blocks))
'@

[System.IO.File]::WriteAllText(
    $parser,
    $pythonCode,
    [System.Text.UTF8Encoding]::new($false)
)

& $python $parser $workbook $catalogFile

if ($LASTEXITCODE -ne 0) {
    throw "Workbook parser failed."
}

Remove-Item $parser -Force -ErrorAction SilentlyContinue

# ------------------------------------------------------------
# 4. Create frontend page
# ------------------------------------------------------------
$pageFile = Join-Path $PagesRoot "VaccinationKpiCategories.tsx"
$cssFile = Join-Path $PagesRoot "VaccinationKpiCategories.css"

$page = @'
import React, { useEffect, useMemo, useState } from "react";
import {
  Bar,
  BarChart,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import {
  useNavigate,
  useParams,
} from "react-router-dom";

import api from "../services/api";
import {
  vaccinationKpiCategories,
  vaccinationKpiIndicators,
  type VaccinationKpiIndicator,
  type VaccinationKpiRow,
} from "../data/vaccinationKpiCatalog";

import "./VaccinationKpiCategories.css";

type Period = 3 | 4 | 5 | 12;

type PeriodOverride = {
  annualTarget?: number;
  target3?: number;
  actual3?: number;
  target5?: number;
  actual5?: number;
  target12?: number;
  actual12?: number;
};

type UnitRow = {
  unit_code: string;
  unit_name: string;
  county_name: string | null;
  unit_type: string | null;
  total_animals: number;
  vaccinated_animals: number;
  remaining_animals: number;
  coverage_percent: number;
  status: string;
  priority: string;
};

const COLORS = {
  critical: "#dc2626",
  warning: "#f59e0b",
  track: "#2563eb",
  excellent: "#16a34a",
  neutral: "#64748b",
};

const PERIOD_LABELS: Record<Period, string> = {
  3: "۳ ماهه",
  4: "۴ ماهه - منبع Excel",
  5: "۵ ماهه",
  12: "سالانه",
};

function fmt(value: number | null | undefined) {
  return new Intl.NumberFormat("fa-IR").format(Number(value ?? 0));
}

function pct(value: number | null | undefined) {
  return `${Number(value ?? 0).toFixed(1)}%`;
}

function normalize(text: string) {
  return text
    .replace(/\u200c/g, "")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();
}

function statusForAchievement(value: number | null) {
  const x = Number(value ?? 0);
  if (x >= 90) return "EXCELLENT";
  if (x >= 75) return "ON_TRACK";
  if (x >= 50) return "WARNING";
  return "CRITICAL";
}

function statusLabel(status: string) {
  switch (status) {
    case "EXCELLENT":
      return "عالی";
    case "ON_TRACK":
      return "مطلوب";
    case "WARNING":
      return "نیازمند توجه";
    case "CRITICAL":
      return "بحرانی";
    case "NO_COVERAGE":
      return "بدون پوشش";
    default:
      return status || "-";
  }
}

function statusColor(status: string) {
  switch (status) {
    case "EXCELLENT":
      return COLORS.excellent;
    case "ON_TRACK":
      return COLORS.track;
    case "WARNING":
      return COLORS.warning;
    case "CRITICAL":
    case "NO_COVERAGE":
      return COLORS.critical;
    default:
      return COLORS.neutral;
  }
}

function indicatorPeriodValue(
  indicator: VaccinationKpiIndicator,
  row: VaccinationKpiRow,
  period: Period,
  overrides: Record<string, PeriodOverride>,
) {
  const key = `${indicator.id}::${row.county}`;

  if (period === 4) {
    return row.actual;
  }

  const override = overrides[key];

  if (!override) return null;

  if (period === 3) return override.actual3 ?? null;
  if (period === 5) return override.actual5 ?? null;
  if (period === 12) return override.actual12 ?? null;

  return null;
}

function indicatorTarget(
  indicator: VaccinationKpiIndicator,
  row: VaccinationKpiRow,
  period: Period,
  overrides: Record<string, PeriodOverride>,
) {
  const key = `${indicator.id}::${row.county}`;
  const override = overrides[key];

  if (period === 4) return row.periodTarget;
  if (period === 12) return override?.annualTarget ?? row.annualTarget;
  if (period === 3) return override?.target3 ?? null;
  if (period === 5) return override?.target5 ?? null;

  return null;
}

function achievement(
  actual: number | null,
  target: number | null,
) {
  if (actual == null || target == null || target === 0) {
    return null;
  }

  return (actual * 100) / target;
}

function loadOverrides(): Record<string, PeriodOverride> {
  try {
    return JSON.parse(
      localStorage.getItem("pvimp_vaccination_kpi_period_overrides_v1") ||
        "{}",
    );
  } catch {
    return {};
  }
}

function saveOverrides(
  value: Record<string, PeriodOverride>,
) {
  localStorage.setItem(
    "pvimp_vaccination_kpi_period_overrides_v1",
    JSON.stringify(value),
  );
}

function getApiTerms(indicator: VaccinationKpiIndicator) {
  const text = normalize(
    `${indicator.sheet} ${indicator.title} ${indicator.indicator}`,
  );

  const terms: string[] = [];

  if (text.includes("شاربن")) terms.push("شاربن");
  if (text.includes("ppr")) terms.push("ppr");
  if (text.includes("آبله")) terms.push("آبله");
  if (text.includes("لمپی")) terms.push("لمپی");
  if (text.includes("تب برفکی")) terms.push("تب برفکی");
  if (text.includes("هاری")) terms.push("هاری");
  if (text.includes("rev1")) terms.push("rev1", "بروسلوز");
  if (text.includes("fd iriba")) terms.push("fd iriba", "بروسلوز");
  if (text.includes("rd iriba")) terms.push("rd iriba", "بروسلوز");

  return terms.length ? terms : [indicator.indicator];
}

export default function VaccinationKpiCategories() {
  const {
    categoryId = "infectious",
    indicatorId,
    countyCode,
  } = useParams<{
    categoryId: string;
    indicatorId?: string;
    countyCode?: string;
  }>();

  const navigate = useNavigate();

  const [period, setPeriod] = useState<Period>(4);
  const [overrides, setOverrides] =
    useState<Record<string, PeriodOverride>>(loadOverrides);

  const [units, setUnits] = useState<UnitRow[]>([]);
  const [unitsLoading, setUnitsLoading] = useState(false);
  const [unitStatusFilter, setUnitStatusFilter] =
    useState<string | null>(null);

  const category = vaccinationKpiCategories.find(
    (x) => x.id === categoryId,
  ) ?? vaccinationKpiCategories[0];

  const categoryIndicators =
    vaccinationKpiIndicators.filter(
      (x) => x.categoryId === category.id,
    );

  const selectedIndicator =
    vaccinationKpiIndicators.find(
      (x) => x.id === indicatorId,
    ) ?? categoryIndicators[0] ?? null;

  const selectedRows = selectedIndicator?.rows ?? [];

  const saveOverride = (
    key: string,
    field: keyof PeriodOverride,
    value: string,
  ) => {
    const next = {
      ...overrides,
      [key]: {
        ...(overrides[key] ?? {}),
        [field]:
          value === ""
            ? undefined
            : Number(value),
      },
    };

    setOverrides(next);
    saveOverrides(next);
  };

  const indicatorChart = useMemo(() => {
    return categoryIndicators.map((indicator) => {
      const actuals = indicator.rows
        .map((row) =>
          indicatorPeriodValue(
            indicator,
            row,
            period,
            overrides,
          ),
        )
        .filter((x): x is number => x != null);

      const targets = indicator.rows
        .map((row) =>
          indicatorTarget(
            indicator,
            row,
            period,
            overrides,
          ),
        )
        .filter((x): x is number => x != null);

      const actual = actuals.reduce(
        (sum, value) => sum + value,
        0,
      );

      const target = targets.reduce(
        (sum, value) => sum + value,
        0,
      );

      const achievementValue =
        target > 0
          ? (actual * 100) / target
          : null;

      return {
        id: indicator.id,
        name: indicator.indicator,
        livestock: indicator.livestockGroup,
        achievement: achievementValue,
        actual,
        target,
        status: statusForAchievement(
          achievementValue,
        ),
      };
    });
  }, [
    categoryIndicators,
    period,
    overrides,
  ]);

  const livestockCharts = useMemo(() => {
    if (!selectedIndicator) return [];

    return [selectedIndicator].map((indicator) => {
      const rows = indicator.rows.map((row) => {
        const actual = indicatorPeriodValue(
          indicator,
          row,
          period,
          overrides,
        );

        const target = indicatorTarget(
          indicator,
          row,
          period,
          overrides,
        );

        return {
          county: row.county,
          actual,
          target,
          achievement: achievement(
            actual,
            target,
          ),
          status: statusForAchievement(
            achievement(actual, target),
          ),
        };
      });

      return {
        indicator,
        rows,
      };
    });
  }, [
    selectedIndicator,
    period,
    overrides,
  ]);

  const selectedCounty = selectedRows.find(
    (x) =>
      normalize(x.county) ===
      normalize(countyCode ?? ""),
  );

  const countyChart = useMemo(() => {
    if (!selectedIndicator) return [];

    return selectedIndicator.rows.map((row) => {
      const actual = indicatorPeriodValue(
        selectedIndicator,
        row,
        period,
        overrides,
      );

      const target = indicatorTarget(
        selectedIndicator,
        row,
        period,
        overrides,
      );

      return {
        county: row.county,
        achievement:
          achievement(actual, target),
        actual,
        target,
      };
    });
  }, [
    selectedIndicator,
    period,
    overrides,
  ]);

  const unitStatusData = useMemo(() => {
    const groups: Record<string, number> = {
      EXCELLENT: 0,
      ON_TRACK: 0,
      WARNING: 0,
      CRITICAL: 0,
      NO_COVERAGE: 0,
    };

    units.forEach((unit) => {
      const key =
        unit.status in groups
          ? unit.status
          : unit.coverage_percent >= 90
            ? "EXCELLENT"
            : unit.coverage_percent >= 75
              ? "ON_TRACK"
              : unit.coverage_percent >= 50
                ? "WARNING"
                : "CRITICAL";

      groups[key] += 1;
    });

    return Object.entries(groups)
      .filter(([, value]) => value > 0)
      .map(([status, value]) => ({
        status,
        name: statusLabel(status),
        value,
        fill: statusColor(status),
      }));
  }, [units]);

  const filteredUnits = useMemo(() => {
    if (!unitStatusFilter) return units;

    return units.filter((unit) => {
      const status =
        unit.status ||
        statusForAchievement(
          unit.coverage_percent,
        );

      return status === unitStatusFilter;
    });
  }, [units, unitStatusFilter]);

  useEffect(() => {
    if (!selectedIndicator) return;

    let cancelled = false;

    async function loadUnits() {
      setUnits([]);
      setUnitStatusFilter(null);
      setUnitsLoading(true);

      try {
        const vaccineResponse =
          await api.get(
            "/api/v1/gis/kpi/vaccination/vaccines",
          );

        const vaccines =
          Array.isArray(vaccineResponse.data)
            ? vaccineResponse.data
            : [];

        const terms =
          getApiTerms(selectedIndicator);

        const matched =
          vaccines.find((item: any) => {
            const value = normalize(
              String(item?.vaccine_type ?? ""),
            );

            return terms.some((term) =>
              value.includes(normalize(term)),
            );
          }) ?? null;

        if (!matched?.vaccine_type) {
          return;
        }

        const response =
          await api.get(
            `/api/v1/gis/kpi/vaccination/vaccine/${encodeURIComponent(
              matched.vaccine_type,
            )}/units-paginated`,
            {
              params: {
                page: 1,
                page_size: 500,
              },
            },
          );

        const items =
          Array.isArray(response.data?.items)
            ? response.data.items
            : [];

        if (!cancelled) {
          setUnits(
            items.map((item: any) => ({
              unit_code: String(
                item?.unit_code ?? "",
              ),
              unit_name: String(
                item?.unit_name ?? "",
              ),
              county_name:
                item?.county_name ?? null,
              unit_type:
                item?.unit_type ?? null,
              total_animals: Number(
                item?.total_animals ?? 0,
              ),
              vaccinated_animals: Number(
                item?.vaccinated_animals ?? 0,
              ),
              remaining_animals: Number(
                item?.remaining_animals ?? 0,
              ),
              coverage_percent: Number(
                item?.coverage_percent ?? 0,
              ),
              status: String(
                item?.status ?? "CRITICAL",
              ),
              priority: String(
                item?.priority ?? "HIGH",
              ),
            })),
          );
        }
      } catch (error) {
        console.warn(
          "[VACCINATION KPI] unit drilldown unavailable",
          error,
        );
      } finally {
        if (!cancelled) {
          setUnitsLoading(false);
        }
      }
    }

    loadUnits();

    return () => {
      cancelled = true;
    };
  }, [selectedIndicator]);

  if (!category) {
    return null;
  }

  return (
    <div
      className="vaccination-kpi-categories"
      dir="rtl"
    >
      <header className="vkc-header">
        <div>
          <div className="vkc-eyebrow">
            سامانه مدیریت یکپارچه دامپزشکی
          </div>

          <h1>
            گزارش نموداری عملکرد واکسیناسیون،
            پایش و مراقبت
          </h1>

          <p>
            ساختار دسته‌بندی بر اساس فایل عملکرد
            واکسیناسیون، پایش و مراقبت استان و شهرستان
          </p>
        </div>

        <button
          type="button"
          onClick={() =>
            navigate("/gis/kpi/vaccination")
          }
        >
          بازگشت به KPI اصلی
        </button>
      </header>

      <section className="vkc-toolbar">
        <div>
          <strong>دوره گزارش:</strong>
          <select
            value={period}
            onChange={(event) =>
              setPeriod(
                Number(event.target.value) as Period,
              )
            }
          >
            <option value={3}>۳ ماهه</option>
            <option value={4}>
              ۴ ماهه - داده منبع
            </option>
            <option value={5}>۵ ماهه</option>
            <option value={12}>سالانه</option>
          </select>
        </div>

        <div className="vkc-source-note">
          داده منبع این فایل تا تاریخ
          <strong> ۱۴۰۵/۰۵/۰۱ </strong>
          برای دوره ۴ ماهه است؛ دوره‌های ۳، ۵ و
          سالانه قابل ورود/اصلاح هستند.
        </div>
      </section>

      <nav className="vkc-category-tabs">
        {vaccinationKpiCategories.map((item) => (
          <button
            key={item.id}
            className={
              item.id === category.id
                ? "active"
                : ""
            }
            type="button"
            onClick={() =>
              navigate(
                `/gis/kpi/vaccination/categories/${item.id}`,
              )
            }
          >
            {item.title}
          </button>
        ))}
      </nav>

      <section className="vkc-panel">
        <div className="vkc-panel-title">
          <div>
            <h2>{category.title}</h2>
            <p>{category.description}</p>
          </div>
        </div>

        <div className="vkc-chart-grid">
          <div className="vkc-chart-card">
            <h3>
              عملکرد شاخص‌های این گروه -{" "}
              {PERIOD_LABELS[period]}
            </h3>

            <div className="vkc-chart">
              <ResponsiveContainer>
                <BarChart
                  data={indicatorChart}
                  onClick={(state: any) => {
                    const active =
                      state?.activePayload?.[0]
                        ?.payload;

                    if (active?.id) {
                      navigate(
                        `/gis/kpi/vaccination/categories/${category.id}/${encodeURIComponent(
                          active.id,
                        )}`,
                      );
                    }
                  }}
                >
                  <XAxis
                    dataKey="name"
                    interval={0}
                    angle={-25}
                    textAnchor="end"
                    height={90}
                  />
                  <YAxis
                    domain={[0, 100]}
                    tickFormatter={(value) =>
                      `${value}%`
                    }
                  />
                  <Tooltip
                    formatter={(value: any) =>
                      pct(Number(value ?? 0))
                    }
                  />
                  <Legend />
                  <Bar
                    dataKey="achievement"
                    name="درصد تحقق"
                    cursor="pointer"
                  >
                    {indicatorChart.map(
                      (entry) => (
                        <Cell
                          key={entry.id}
                          fill={statusColor(
                            entry.status,
                          )}
                        />
                      ),
                    )}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="vkc-chart-card">
            <h3>وضعیت شاخص‌ها</h3>

            <div className="vkc-chart">
              <ResponsiveContainer>
                <PieChart>
                  <Pie
                    data={[
                      "EXCELLENT",
                      "ON_TRACK",
                      "WARNING",
                      "CRITICAL",
                    ].map((status) => ({
                      status,
                      name: statusLabel(status),
                      value:
                        indicatorChart.filter(
                          (x) =>
                            x.status === status,
                        ).length,
                      fill: statusColor(status),
                    })).filter(
                      (x) => x.value > 0,
                    )}
                    dataKey="value"
                    nameKey="name"
                    outerRadius={105}
                    label={({ name, value }) =>
                      `${name}: ${value}`
                    }
                    onClick={(entry: any) => {
                      const item =
                        indicatorChart.find(
                          (x) =>
                            x.status ===
                            entry?.status,
                        );

                      if (item) {
                        navigate(
                          `/gis/kpi/vaccination/categories/${category.id}/${encodeURIComponent(
                            item.id,
                          )}`,
                        );
                      }
                    }}
                  />
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </section>

      {selectedIndicator && (
        <>
          <section className="vkc-panel">
            <div className="vkc-panel-title">
              <div>
                <h2>
                  {selectedIndicator.indicator}
                </h2>
                <p>
                  شیت منبع:{" "}
                  {selectedIndicator.sheet}
                </p>
              </div>
            </div>

            <div className="vkc-livestock-grid">
              {livestockCharts.map(
                ({ indicator, rows }) => (
                  <div
                    className="vkc-chart-card"
                    key={indicator.id}
                  >
                    <h3>
                      گروه دام:{" "}
                      {indicator.livestockGroup}
                    </h3>

                    <div className="vkc-chart">
                      <ResponsiveContainer>
                        <BarChart
                          data={rows}
                          onClick={(
                            state: any,
                          ) => {
                            const active =
                              state?.activePayload?.[0]
                                ?.payload;

                            if (
                              active?.county
                            ) {
                              navigate(
                                `/gis/kpi/vaccination/categories/${category.id}/${encodeURIComponent(
                                  indicator.id,
                                )}/county/${encodeURIComponent(
                                  active.county,
                                )}`,
                              );
                            }
                          }}
                        >
                          <XAxis
                            dataKey="county"
                            interval={0}
                            angle={-35}
                            textAnchor="end"
                            height={95}
                          />
                          <YAxis
                            domain={[0, 100]}
                            tickFormatter={(v) =>
                              `${v}%`
                            }
                          />
                          <Tooltip
                            formatter={(
                              value: any,
                            ) =>
                              pct(
                                Number(
                                  value ?? 0,
                                ),
                              )
                            }
                          />
                          <Bar
                            dataKey="achievement"
                            name="درصد تحقق"
                            cursor="pointer"
                          >
                            {rows.map(
                              (row) => (
                                <Cell
                                  key={
                                    row.county
                                  }
                                  fill={statusColor(
                                    row.status,
                                  )}
                                />
                              ),
                            )}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                ),
              )}
            </div>
          </section>

          {countyCode && selectedCounty && (
            <section className="vkc-panel">
              <div className="vkc-panel-title">
                <div>
                  <h2>
                    جزئیات شهرستان{" "}
                    {selectedCounty.county}
                  </h2>
                  <p>
                    {selectedIndicator.indicator}
                    {" - "}
                    {PERIOD_LABELS[period]}
                  </p>
                </div>

                <button
                  type="button"
                  onClick={() =>
                    navigate(
                      `/gis/kpi/vaccination/categories/${category.id}/${encodeURIComponent(
                        selectedIndicator.id,
                      )}`,
                    )
                  }
                >
                  بازگشت به نمودار شهرستان‌ها
                </button>
              </div>

              <div className="vkc-chart-grid">
                <div className="vkc-chart-card">
                  <h3>
                    تحقق دوره انتخاب‌شده
                  </h3>

                  <div className="vkc-single-kpi">
                    {pct(
                      achievement(
                        indicatorPeriodValue(
                          selectedIndicator,
                          selectedCounty,
                          period,
                          overrides,
                        ),
                        indicatorTarget(
                          selectedIndicator,
                          selectedCounty,
                          period,
                          overrides,
                        ),
                      ),
                    )}
                  </div>
                </div>

                <div className="vkc-chart-card">
                  <h3>
                    عملکرد در برابر هدف
                  </h3>

                  <div className="vkc-chart">
                    <ResponsiveContainer>
                      <BarChart
                        data={[
                          {
                            name: "هدف",
                            value:
                              indicatorTarget(
                                selectedIndicator,
                                selectedCounty,
                                period,
                                overrides,
                              ) ?? 0,
                          },
                          {
                            name: "عملکرد",
                            value:
                              indicatorPeriodValue(
                                selectedIndicator,
                                selectedCounty,
                                period,
                                overrides,
                              ) ?? 0,
                          },
                        ]}
                      >
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Bar
                          dataKey="value"
                          name="تعداد"
                          fill={COLORS.track}
                        />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>
            </section>
          )}

          {!countyCode && (
            <section className="vkc-panel">
              <div className="vkc-panel-title">
                <div>
                  <h2>
                    عملکرد شهرستان‌ها
                  </h2>
                  <p>
                    کلیک روی هر شهرستان، وارد
                    جزئیات همان شهرستان می‌شود.
                  </p>
                </div>
              </div>

              <div className="vkc-chart">
                <ResponsiveContainer>
                  <BarChart
                    data={countyChart}
                    onClick={(state: any) => {
                      const active =
                        state?.activePayload?.[0]
                          ?.payload;

                      if (active?.county) {
                        navigate(
                          `/gis/kpi/vaccination/categories/${category.id}/${encodeURIComponent(
                            selectedIndicator.id,
                          )}/county/${encodeURIComponent(
                            active.county,
                          )}`,
                        );
                      }
                    }}
                  >
                    <XAxis
                      dataKey="county"
                      interval={0}
                      angle={-35}
                      textAnchor="end"
                      height={100}
                    />
                    <YAxis
                      domain={[0, 100]}
                      tickFormatter={(v) =>
                        `${v}%`
                      }
                    />
                    <Tooltip
                      formatter={(v: any) =>
                        pct(Number(v ?? 0))
                      }
                    />
                    <Bar
                      dataKey="achievement"
                      name="درصد تحقق"
                      cursor="pointer"
                    >
                      {countyChart.map(
                        (entry) => (
                          <Cell
                            key={entry.county}
                            fill={statusColor(
                              statusForAchievement(
                                entry.achievement,
                              ),
                            )}
                          />
                        ),
                      )}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </section>
          )}

          <section className="vkc-panel">
            <div className="vkc-panel-title">
              <div>
                <h2>
                  ورود و اصلاح پیش‌بینی‌های دوره‌ای
                </h2>
                <p>
                  دوره ۴ ماهه از فایل منبع خوانده شده
                  است. مقادیر ۳، ۵ و سالانه قابل ورود
                  هستند و در مرورگر ذخیره می‌شوند.
                </p>
              </div>
            </div>

            <div className="vkc-table-wrap">
              <table className="vkc-table">
                <thead>
                  <tr>
                    <th>شهرستان</th>
                    <th>هدف سالانه منبع</th>
                    <th>هدف ۴ ماهه منبع</th>
                    <th>عملکرد ۴ ماهه منبع</th>
                    <th>هدف ۳ ماهه</th>
                    <th>عملکرد ۳ ماهه</th>
                    <th>هدف ۵ ماهه</th>
                    <th>عملکرد ۵ ماهه</th>
                    <th>هدف سالانه</th>
                    <th>عملکرد سالانه</th>
                  </tr>
                </thead>

                <tbody>
                  {selectedIndicator.rows.map(
                    (row) => {
                      const key =
                        `${selectedIndicator.id}::${row.county}`;

                      const override =
                        overrides[key] ?? {};

                      return (
                        <tr key={key}>
                          <td>
                            <button
                              type="button"
                              className="vkc-link-button"
                              onClick={() =>
                                navigate(
                                  `/gis/kpi/vaccination/categories/${category.id}/${encodeURIComponent(
                                    selectedIndicator.id,
                                  )}/county/${encodeURIComponent(
                                    row.county,
                                  )}`,
                                )
                              }
                            >
                              {row.county}
                            </button>
                          </td>

                          <td>
                            {fmt(
                              row.annualTarget,
                            )}
                          </td>

                          <td>
                            {fmt(
                              row.periodTarget,
                            )}
                          </td>

                          <td>
                            {fmt(row.actual)}
                          </td>

                          <td>
                            <input
                              type="number"
                              value={
                                override.target3 ??
                                ""
                              }
                              onChange={(e) =>
                                saveOverride(
                                  key,
                                  "target3",
                                  e.target.value,
                                )
                              }
                            />
                          </td>

                          <td>
                            <input
                              type="number"
                              value={
                                override.actual3 ??
                                ""
                              }
                              onChange={(e) =>
                                saveOverride(
                                  key,
                                  "actual3",
                                  e.target.value,
                                )
                              }
                            />
                          </td>

                          <td>
                            <input
                              type="number"
                              value={
                                override.target5 ??
                                ""
                              }
                              onChange={(e) =>
                                saveOverride(
                                  key,
                                  "target5",
                                  e.target.value,
                                )
                              }
                            />
                          </td>

                          <td>
                            <input
                              type="number"
                              value={
                                override.actual5 ??
                                ""
                              }
                              onChange={(e) =>
                                saveOverride(
                                  key,
                                  "actual5",
                                  e.target.value,
                                )
                              }
                            />
                          </td>

                          <td>
                            <input
                              type="number"
                              value={
                                override.annualTarget ??
                                row.annualTarget ??
                                ""
                              }
                              onChange={(e) =>
                                saveOverride(
                                  key,
                                  "annualTarget",
                                  e.target.value,
                                )
                              }
                            />
                          </td>

                          <td>
                            <input
                              type="number"
                              value={
                                override.actual12 ??
                                ""
                              }
                              onChange={(e) =>
                                saveOverride(
                                  key,
                                  "actual12",
                                  e.target.value,
                                )
                              }
                            />
                          </td>
                        </tr>
                      );
                    },
                  )}
                </tbody>
              </table>
            </div>
          </section>

          <section className="vkc-panel">
            <div className="vkc-panel-title">
              <div>
                <h2>
                  وضعیت واحدهای شهرستان
                </h2>
                <p>
                  اگر نوع واکسن شاخص در API فعلی پیدا
                  شود، واحدها از همان KPI موجود خوانده
                  می‌شوند.
                </p>
              </div>

              {unitsLoading && (
                <span>در حال دریافت واحدها...</span>
              )}
            </div>

            <div className="vkc-chart-grid">
              <div className="vkc-chart-card">
                <h3>
                  توزیع وضعیت واحدها
                </h3>

                <div className="vkc-chart">
                  {units.length > 0 ? (
                    <ResponsiveContainer>
                      <PieChart>
                        <Pie
                          data={unitStatusData}
                          dataKey="value"
                          nameKey="name"
                          outerRadius={105}
                          label={({ name, value }) =>
                            `${name}: ${value}`
                          }
                          onClick={(entry: any) =>
                            setUnitStatusFilter(
                              entry?.status ?? null,
                            )
                          }
                        >
                          {unitStatusData.map(
                            (entry) => (
                              <Cell
                                key={entry.status}
                                fill={entry.fill}
                                cursor="pointer"
                              />
                            ),
                          )}
                        </Pie>

                        <Tooltip />
                        <Legend />
                      </PieChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="vkc-empty">
                      برای این شاخص هنوز نوع واکسن
                      متناظر در API پیدا نشد.
                    </div>
                  )}
                </div>
              </div>

              <div className="vkc-chart-card">
                <h3>
                  واحدهای باقیمانده
                </h3>

                <div className="vkc-big-number">
                  {fmt(
                    units.filter(
                      (x) =>
                        x.remaining_animals > 0,
                    ).length,
                  )}
                </div>

                <p>
                  واحد دارای دام واکسینه‌نشده
                </p>
              </div>
            </div>

            {unitStatusFilter && (
              <div className="vkc-unit-status-result">
                <h3>
                  جدول واحدهای{" "}
                  {statusLabel(
                    unitStatusFilter,
                  )}
                </h3>

                <div className="vkc-table-wrap">
                  <table className="vkc-table">
                    <thead>
                      <tr>
                        <th>واحد</th>
                        <th>شهرستان</th>
                        <th>نوع واحد</th>
                        <th>کل دام</th>
                        <th>واکسینه</th>
                        <th>باقی‌مانده</th>
                        <th>پوشش</th>
                        <th>وضعیت</th>
                        <th>جزییات</th>
                      </tr>
                    </thead>

                    <tbody>
                      {filteredUnits.map(
                        (unit) => (
                          <tr
                            key={
                              unit.unit_code
                            }
                          >
                            <td>
                              {unit.unit_name}
                            </td>
                            <td>
                              {unit.county_name ||
                                "-"}
                            </td>
                            <td>
                              {unit.unit_type ||
                                "-"}
                            </td>
                            <td>
                              {fmt(
                                unit.total_animals,
                              )}
                            </td>
                            <td>
                              {fmt(
                                unit.vaccinated_animals,
                              )}
                            </td>
                            <td>
                              {fmt(
                                unit.remaining_animals,
                              )}
                            </td>
                            <td>
                              {pct(
                                unit.coverage_percent,
                              )}
                            </td>
                            <td>
                              {statusLabel(
                                unit.status,
                              )}
                            </td>
                            <td>
                              <button
                                type="button"
                                onClick={() =>
                                  navigate(
                                    `/gis/kpi/vaccination/unit/${encodeURIComponent(
                                      unit.unit_code,
                                    )}`,
                                  )
                                }
                              >
                                مشاهده تاریخچه واحد
                              </button>
                            </td>
                          </tr>
                        ),
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </section>
        </>
      )}
    </div>
  );
}
'@

$css = @'
.vaccination-kpi-categories {
  min-height: 100vh;
  padding: 24px;
  background: #f5f7fb;
  color: #172033;
}

.vkc-header {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  align-items: flex-start;
  margin-bottom: 20px;
}

.vkc-header h1 {
  margin: 4px 0 8px;
  font-size: 26px;
}

.vkc-header p,
.vkc-panel-title p {
  margin: 0;
  color: #64748b;
}

.vkc-eyebrow {
  color: #2563eb;
  font-weight: 700;
}

.vkc-header button,
.vkc-toolbar button,
.vkc-panel button,
.vkc-table button {
  border: 0;
  border-radius: 8px;
  padding: 9px 14px;
  cursor: pointer;
  background: #1d4ed8;
  color: #fff;
}

.vkc-toolbar {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  flex-wrap: wrap;
  align-items: center;
  background: #fff;
  border-radius: 14px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 2px 12px rgba(15, 23, 42, 0.06);
}

.vkc-toolbar select {
  margin-right: 10px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 8px 12px;
}

.vkc-source-note {
  color: #475569;
}

.vkc-category-tabs {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 18px;
}

.vkc-category-tabs button {
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  padding: 14px;
  background: #fff;
  color: #334155;
  cursor: pointer;
  font-weight: 700;
}

.vkc-category-tabs button.active {
  background: #1d4ed8;
  color: #fff;
  border-color: #1d4ed8;
}

.vkc-panel {
  background: #fff;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 18px;
  box-shadow: 0 2px 12px rgba(15, 23, 42, 0.06);
}

.vkc-panel-title {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 14px;
  margin-bottom: 16px;
}

.vkc-panel-title h2 {
  margin: 0 0 6px;
}

.vkc-chart-grid,
.vkc-livestock-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
  gap: 16px;
}

.vkc-chart-card {
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 14px;
  background: #fbfdff;
}

.vkc-chart-card h3 {
  margin: 0 0 12px;
}

.vkc-chart {
  width: 100%;
  height: 360px;
}

.vkc-single-kpi,
.vkc-big-number {
  font-size: 42px;
  font-weight: 800;
  text-align: center;
  padding: 42px 12px;
  color: #1d4ed8;
}

.vkc-empty {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #64748b;
  padding: 30px;
}

.vkc-table-wrap {
  width: 100%;
  overflow-x: auto;
}

.vkc-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 1100px;
}

.vkc-table th,
.vkc-table td {
  border-bottom: 1px solid #e2e8f0;
  padding: 10px;
  text-align: right;
  white-space: nowrap;
}

.vkc-table th {
  background: #f8fafc;
}

.vkc-table input {
  width: 110px;
  border: 1px solid #cbd5e1;
  border-radius: 7px;
  padding: 7px;
}

.vkc-link-button {
  background: transparent !important;
  color: #1d4ed8 !important;
  padding: 0 !important;
}

.vkc-unit-status-result {
  margin-top: 18px;
}

@media (max-width: 900px) {
  .vaccination-kpi-categories {
    padding: 14px;
  }

  .vkc-header {
    flex-direction: column;
  }

  .vkc-category-tabs {
    grid-template-columns: 1fr;
  }

  .vkc-chart-grid,
  .vkc-livestock-grid {
    grid-template-columns: 1fr;
  }
}
'@

$utf8 = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::WriteAllText($pageFile, $page, $utf8)
[System.IO.File]::WriteAllText($cssFile, $css, $utf8)

# ------------------------------------------------------------
# 5. Patch AppRouter.tsx safely
# ------------------------------------------------------------
if (-not (Test-Path $RouterFile)) {
    throw "AppRouter.tsx not found: $RouterFile"
}

$routerText = [System.IO.File]::ReadAllText($RouterFile, $utf8)

if ($routerText -notmatch 'VaccinationKpiCategories') {
    $importAnchor = 'import KPIAnalysis from "../pages/KPIAnalysis";'

    if ($routerText.Contains($importAnchor)) {
        $routerText = $routerText.Replace(
            $importAnchor,
            $importAnchor + [Environment]::NewLine +
            'import VaccinationKpiCategories from "../pages/VaccinationKpiCategories";'
        )
    } else {
        throw "Could not locate KPIAnalysis import in AppRouter.tsx. No router changes were written."
    }

    $routeBlock = @'
      <Route
        path="/gis/kpi/vaccination/categories"
        element={<VaccinationKpiCategories />}
      />
      <Route
        path="/gis/kpi/vaccination/categories/:categoryId"
        element={<VaccinationKpiCategories />}
      />
      <Route
        path="/gis/kpi/vaccination/categories/:categoryId/:indicatorId"
        element={<VaccinationKpiCategories />}
      />
      <Route
        path="/gis/kpi/vaccination/categories/:categoryId/:indicatorId/county/:countyCode"
        element={<VaccinationKpiCategories />}
      />
'@

    if ($routerText -match '</Routes>') {
        $routerText = [regex]::Replace(
            $routerText,
            '</Routes>',
            ($routeBlock + [Environment]::NewLine + '    </Routes>'),
            1
        )
    } else {
        throw "Could not locate </Routes> in AppRouter.tsx. No router changes were written."
    }

    [System.IO.File]::WriteAllText($RouterFile, $routerText, $utf8)
}

# ------------------------------------------------------------
# 6. Add navigation button to existing KPIAnalysis
# ------------------------------------------------------------
if (Test-Path $KpiFile) {
    $kpiText = [System.IO.File]::ReadAllText($KpiFile, $utf8)

    if ($kpiText -notmatch 'گزارش تفکیکی بیماری') {
        $button = @'
        <button
          type="button"
          onClick={() =>
            navigate("/gis/kpi/vaccination/categories")
          }
        >
          گزارش تفکیکی بیماری‌ها
        </button>
'@

        $pattern = '(<div\s+className="dashboard-header"[^>]*>)'
        $matches = [regex]::Matches(
            $kpiText,
            $pattern,
            [System.Text.RegularExpressions.RegexOptions]::IgnoreCase
        )

        if ($matches.Count -gt 0) {
            $insertAt = $matches[0].Index + $matches[0].Length
            $kpiText =
                $kpiText.Substring(0, $insertAt) +
                [Environment]::NewLine +
                $button +
                $kpiText.Substring($insertAt)

            [System.IO.File]::WriteAllText(
                $KpiFile,
                $kpiText,
                $utf8
            )
        } else {
            Write-Warning "dashboard-header was not found in KPIAnalysis.tsx. The new page is still available at /gis/kpi/vaccination/categories."
        }
    }
}

# ------------------------------------------------------------
# 7. Build
# ------------------------------------------------------------
Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host " BUILD CHECK" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow

Set-Location $FrontendRoot
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "BUILD FAILED. Restoring existing files from backup..." -ForegroundColor Red

    foreach ($file in @($RouterFile, $KpiFile)) {
        $relative = $file.Substring($FrontendRoot.Length).TrimStart("\")
        $backup = Join-Path $backupRoot $relative
        if (Test-Path $backup) {
            Copy-Item $backup $file -Force
        }
    }

    throw "Frontend build failed. Existing KPI files were restored from $backupRoot."
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host " INSTALLATION COMPLETED" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "New page:" -ForegroundColor Cyan
Write-Host "http://localhost:5173/gis/kpi/vaccination/categories" -ForegroundColor White
Write-Host ""
Write-Host "Backup:" -ForegroundColor Cyan
Write-Host $backupRoot -ForegroundColor White
Write-Host ""
Write-Host "Existing vaccination KPI pages were preserved." -ForegroundColor Green
Write-Host "Workbook structure was imported from all 10 sheets." -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT:" -ForegroundColor Yellow
Write-Host "4-month values are source values from 1405/05/01." -ForegroundColor Yellow
Write-Host "3/5/12-month editable values are currently browser-local." -ForegroundColor Yellow
Write-Host "Unit drill-down uses the existing vaccination KPI API when a vaccine type can be matched." -ForegroundColor Yellow
