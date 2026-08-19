
$ErrorActionPreference = "Stop"

$frontendRoot = "D:\pvimp_backend\pvimp_frontend"
$pages = Join-Path $frontendRoot "src\pages"

if (-not (Test-Path $pages)) {
    throw "Frontend pages directory not found: $pages"
}

$manager = Join-Path $pages "DiseaseControlManager.tsx"
$managerCss = Join-Path $pages "DiseaseControlManager.css"

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"

if (Test-Path $manager) {
    Copy-Item $manager "$manager.bak_$stamp" -Force
}
if (Test-Path $managerCss) {
    Copy-Item $managerCss "$managerCss.bak_$stamp" -Force
}

$managerContent = @'
import React, { useEffect, useMemo, useState } from "react";
import {
    BarChart,
    Bar,
    CartesianGrid,
    Cell,
    Legend,
    LineChart,
    Line,
    PieChart,
    Pie,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";
import "./DiseaseControlManager.css";

const API = "http://localhost:8000";

type AnyRecord = Record<string, unknown>;

function numberOf(value: unknown): number {
    const n = Number(value);
    return Number.isFinite(n) ? n : 0;
}

function textOf(value: unknown): string {
    if (value === null || value === undefined) return "-";
    return String(value);
}

function arrayOf(value: unknown): AnyRecord[] {
    if (Array.isArray(value)) return value.filter(x => x && typeof x === "object") as AnyRecord[];
    if (value && typeof value === "object") {
        const obj = value as AnyRecord;
        for (const key of ["data", "items", "results", "rows", "diseases", "vaccinations", "surveillance"]) {
            if (Array.isArray(obj[key])) return obj[key] as AnyRecord[];
        }
    }
    return [];
}

function valueFrom(obj: AnyRecord, keys: string[]): unknown {
    for (const key of keys) {
        if (obj[key] !== undefined && obj[key] !== null) return obj[key];
    }
    return undefined;
}

function countFrom(value: unknown, keys: string[] = []): number {
    if (typeof value === "number") return numberOf(value);
    if (value && typeof value === "object") {
        const obj = value as AnyRecord;
        for (const key of keys) {
            if (obj[key] !== undefined) return numberOf(obj[key]);
        }
        for (const key of ["count", "total", "value", "number"]) {
            if (obj[key] !== undefined) return numberOf(obj[key]);
        }
    }
    return 0;
}

function normalizeDiseaseData(value: unknown) {
    return arrayOf(value).map((r, i) => ({
        name: textOf(valueFrom(r, ["disease_name", "disease", "name", "title"]) ?? `بیماری ${i + 1}`),
        value: countFrom(r, ["count", "cases", "case_count", "total", "occurrences", "value"]),
    })).filter(x => x.value > 0);
}

function normalizeVaccinationData(value: unknown) {
    return arrayOf(value).map((r, i) => ({
        name: textOf(valueFrom(r, ["vaccine_type", "vaccine", "disease_name", "disease", "name", "title"]) ?? `مورد ${i + 1}`),
        value: countFrom(r, ["vaccinated_animals", "vaccinated", "animal_count", "count", "total", "value"]),
    })).filter(x => x.value > 0);
}

function normalizeCountyData(value: unknown) {
    return arrayOf(value).map((r, i) => ({
        name: textOf(valueFrom(r, ["county_name", "county", "name", "title"]) ?? `شهرستان ${i + 1}`),
        value: countFrom(r, ["count", "cases", "case_count", "total", "value"]),
    })).filter(x => x.value > 0);
}

function KPI({ title, value, hint, tone }: { title: string; value: number | string; hint: string; tone?: string }) {
    return (
        <div className={`dc-kpi ${tone || ""}`}>
            <div className="dc-kpi-title">{title}</div>
            <div className="dc-kpi-value">{typeof value === "number" ? value.toLocaleString("fa-IR") : value}</div>
            <div className="dc-kpi-hint">{hint}</div>
        </div>
    );
}

export default function DiseaseControlManager() {
    const [diseaseRaw, setDiseaseRaw] = useState<unknown>(null);
    const [vaccinationRaw, setVaccinationRaw] = useState<unknown>(null);
    const [surveillanceRaw, setSurveillanceRaw] = useState<unknown>(null);
    const [lastImportRaw, setLastImportRaw] = useState<unknown>(null);
    const [countyRaw, setCountyRaw] = useState<unknown>(null);
    const [loading, setLoading] = useState(true);
    const [errors, setErrors] = useState<string[]>([]);

    useEffect(() => {
        let active = true;

        async function get(path: string) {
            const response = await fetch(`${API}${path}`);
            if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
            return response.json();
        }

        async function load() {
            setLoading(true);
            const nextErrors: string[] = [];

            const jobs = await Promise.allSettled([
                get("/gis-dashboard/disease-summary"),
                get("/gis-dashboard/vaccination-summary"),
                get("/gis-dashboard/surveillance-summary"),
                get("/gis-dashboard/last-import"),
                get("/gis-county-analysis/diseases"),
            ]);

            if (!active) return;

            const values = jobs.map(x => x.status === "fulfilled" ? x.value : null);
            jobs.forEach((x, i) => {
                if (x.status === "rejected") {
                    nextErrors.push(`منبع ${i + 1} در دسترس نیست`);
                    console.warn(x.reason);
                }
            });

            setDiseaseRaw(values[0]);
            setVaccinationRaw(values[1]);
            setSurveillanceRaw(values[2]);
            setLastImportRaw(values[3]);
            setCountyRaw(values[4]);
            setErrors(nextErrors);
            setLoading(false);
        }

        load();
        const timer = window.setInterval(load, 120000);

        return () => {
            active = false;
            window.clearInterval(timer);
        };
    }, []);

    const diseases = useMemo(() => normalizeDiseaseData(diseaseRaw), [diseaseRaw]);
    const vaccinations = useMemo(() => normalizeVaccinationData(vaccinationRaw), [vaccinationRaw]);
    const counties = useMemo(() => normalizeCountyData(countyRaw), [countyRaw]);

    const diseaseTotal = useMemo(() => diseases.reduce((s, x) => s + x.value, 0), [diseases]);
    const vaccinationTotal = useMemo(() => vaccinations.reduce((s, x) => s + x.value, 0), [vaccinations]);

    const surveillanceCount = useMemo(() => countFrom(
        surveillanceRaw,
        ["count", "total", "active", "surveillance_count", "records"]
    ) || arrayOf(surveillanceRaw).length, [surveillanceRaw]);

    const importLabel = useMemo(() => {
        if (!lastImportRaw) return "اطلاعات آخرین بارگذاری در دسترس نیست";
        if (typeof lastImportRaw === "string") return lastImportRaw;
        const obj = lastImportRaw as AnyRecord;
        return textOf(valueFrom(obj, ["file", "filename", "name", "created_at", "last_import", "message"]) ?? "آخرین وضعیت ثبت شد");
    }, [lastImportRaw]);

    const alerts = useMemo(() => {
        const result: { title: string; detail: string; level: "high" | "medium" | "info" }[] = [];

        if (diseases.length > 0) {
            const top = [...diseases].sort((a, b) => b.value - a.value)[0];
            result.push({
                title: "بیشترین تمرکز بیماری",
                detail: `${top.name} با ${top.value.toLocaleString("fa-IR")} مورد`,
                level: "high",
            });
        }

        if (counties.length > 0) {
            const top = [...counties].sort((a, b) => b.value - a.value)[0];
            result.push({
                title: "شهرستان نیازمند توجه",
                detail: `${top.name} با ${top.value.toLocaleString("fa-IR")} مورد`,
                level: "medium",
            });
        }

        if (vaccinationTotal > 0) {
            result.push({
                title: "پوشش عملیات واکسیناسیون",
                detail: `${vaccinationTotal.toLocaleString("fa-IR")} رکورد/مورد واکسیناسیون در داده GIS`,
                level: "info",
            });
        }

        return result;
    }, [diseases, counties, vaccinationTotal]);

    return (
        <main className="dc-page" dir="rtl">
            <header className="dc-header">
                <div>
                    <div className="dc-eyebrow">معاونت سلامت ← اداره بهداشت و مدیریت بیماری‌های دامی</div>
                    <h1>داشبورد مدیریتی بیماری‌های دامی</h1>
                    <p>تحلیل داده‌های GIS، وضعیت بیماری‌ها، واکسیناسیون، پایش و هشدارهای مدیریتی</p>
                </div>
                <div className="dc-status">
                    <span className={loading ? "dc-dot loading" : "dc-dot"} />
                    {loading ? "در حال دریافت اطلاعات" : "اتصال به داده‌های GIS"}
                </div>
            </header>

            {errors.length > 0 && (
                <div className="dc-warning">
                    <strong>برخی منابع هنوز پاسخ مدیریتی ندارند.</strong>
                    <span>{errors.join(" · ")}</span>
                </div>
            )}

            <section className="dc-kpi-grid">
                <KPI title="کل موارد بیماری" value={diseaseTotal} hint="بر اساس داده‌های موجود GIS" tone="danger" />
                <KPI title="عملیات واکسیناسیون" value={vaccinationTotal} hint="مجموع رکوردهای قابل تحلیل" tone="success" />
                <KPI title="رکوردهای پایش" value={surveillanceCount} hint="داده‌های مراقبت و پایش" tone="info" />
                <KPI title="شهرستان‌های دارای داده" value={counties.length} hint="شهرستان‌های حاضر در تحلیل" tone="neutral" />
            </section>

            <section className="dc-grid dc-grid-main">
                <article className="dc-card">
                    <div className="dc-card-head">
                        <h2>توزیع بیماری‌ها</h2>
                        <span>کانون‌ها / موارد ثبت‌شده</span>
                    </div>
                    <div className="dc-chart">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={diseases.slice(0, 10)} layout="vertical" margin={{ top: 8, right: 24, left: 70, bottom: 8 }}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis type="number" />
                                <YAxis type="category" dataKey="name" width={110} tick={{ fontSize: 12 }} />
                                <Tooltip />
                                <Bar dataKey="value" name="تعداد" radius={[0, 6, 6, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </article>

                <article className="dc-card">
                    <div className="dc-card-head">
                        <h2>وضعیت واکسیناسیون</h2>
                        <span>بر مبنای داده GIS</span>
                    </div>
                    <div className="dc-chart">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={vaccinations.slice(0, 8)}
                                    dataKey="value"
                                    nameKey="name"
                                    cx="50%"
                                    cy="50%"
                                    outerRadius={105}
                                    label
                                >
                                    {vaccinations.slice(0, 8).map((_, i) => <Cell key={i} />)}
                                </Pie>
                                <Tooltip />
                                <Legend />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </article>
            </section>

            <section className="dc-grid">
                <article className="dc-card">
                    <div className="dc-card-head">
                        <h2>مقایسه شهرستان‌ها</h2>
                        <span>تمرکز موارد بیماری</span>
                    </div>
                    <div className="dc-chart dc-chart-short">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={counties.slice(0, 12)} margin={{ top: 10, right: 20, left: 10, bottom: 50 }}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" angle={-35} textAnchor="end" interval={0} height={65} />
                                <YAxis />
                                <Tooltip />
                                <Bar dataKey="value" name="موارد" radius={[6, 6, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </article>

                <article className="dc-card">
                    <div className="dc-card-head">
                        <h2>هشدارهای مدیریتی</h2>
                        <span>اولویت اقدام</span>
                    </div>
                    <div className="dc-alerts">
                        {alerts.length === 0 && <div className="dc-empty">برای تولید هشدار، داده تحلیلی بیشتری لازم است.</div>}
                        {alerts.map((a, i) => (
                            <div key={i} className={`dc-alert ${a.level}`}>
                                <div className="dc-alert-title">{a.title}</div>
                                <div>{a.detail}</div>
                            </div>
                        ))}
                    </div>
                </article>
            </section>

            <section className="dc-card dc-bottom">
                <div className="dc-card-head">
                    <h2>آخرین وضعیت بارگذاری GIS</h2>
                    <span>منبع تغذیه داشبورد مدیریتی</span>
                </div>
                <div className="dc-import">
                    <span className="dc-import-label">وضعیت:</span>
                    <strong>{importLabel}</strong>
                </div>
                <div className="dc-note">
                    این صفحه مصرف‌کننده داده است؛ ورودی GIS در مسیر «بهداشت و مدیریت بیماری‌های دامی» باقی می‌ماند و خروجی تحلیلی آن در داشبورد اداره نمایش داده می‌شود.
                </div>
            </section>
        </main>
    );
}
'@

$cssContent = @'
.dc-page {
    min-height: 100%;
    padding: 24px;
    background: var(--color-background, #f5f7fa);
    color: var(--color-text, #1f2937);
}

.dc-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 20px;
}

.dc-eyebrow {
    font-size: 13px;
    opacity: .7;
    margin-bottom: 6px;
}

.dc-header h1 {
    margin: 0;
    font-size: 28px;
}

.dc-header p {
    margin: 8px 0 0;
    opacity: .72;
}

.dc-status {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 9px 13px;
    border-radius: 999px;
    background: white;
    box-shadow: 0 4px 18px rgba(0,0,0,.06);
    white-space: nowrap;
}

.dc-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #16a34a;
}

.dc-dot.loading {
    background: #f59e0b;
}

.dc-warning {
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin-bottom: 18px;
    padding: 13px 16px;
    border-radius: 12px;
    background: #fff7ed;
    border: 1px solid #fed7aa;
}

.dc-kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    margin-bottom: 18px;
}

.dc-kpi {
    background: white;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 5px 22px rgba(0,0,0,.06);
    border-right: 4px solid #64748b;
}

.dc-kpi.danger { border-right-color: #dc2626; }
.dc-kpi.success { border-right-color: #16a34a; }
.dc-kpi.info { border-right-color: #2563eb; }

.dc-kpi-title {
    font-size: 14px;
    opacity: .72;
}

.dc-kpi-value {
    font-size: 30px;
    font-weight: 800;
    margin: 8px 0 4px;
}

.dc-kpi-hint {
    font-size: 12px;
    opacity: .58;
}

.dc-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
    margin-bottom: 18px;
}

.dc-card {
    background: white;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 5px 22px rgba(0,0,0,.06);
}

.dc-card-head {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 12px;
}

.dc-card-head h2 {
    margin: 0;
    font-size: 18px;
}

.dc-card-head span {
    font-size: 12px;
    opacity: .55;
}

.dc-chart {
    height: 330px;
}

.dc-chart-short {
    height: 300px;
}

.dc-alerts {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.dc-alert {
    padding: 13px 15px;
    border-radius: 12px;
    border-right: 4px solid #64748b;
    background: #f8fafc;
}

.dc-alert.high {
    border-right-color: #dc2626;
    background: #fef2f2;
}

.dc-alert.medium {
    border-right-color: #f59e0b;
    background: #fffbeb;
}

.dc-alert.info {
    border-right-color: #2563eb;
    background: #eff6ff;
}

.dc-alert-title {
    font-weight: 800;
    margin-bottom: 4px;
}

.dc-empty {
    padding: 25px;
    text-align: center;
    opacity: .6;
}

.dc-import {
    display: flex;
    gap: 8px;
    align-items: center;
    padding: 14px;
    border-radius: 12px;
    background: #f8fafc;
}

.dc-import-label {
    opacity: .65;
}

.dc-note {
    margin-top: 12px;
    font-size: 12px;
    opacity: .6;
}

@media (max-width: 1000px) {
    .dc-kpi-grid,
    .dc-grid {
        grid-template-columns: 1fr 1fr;
    }

    .dc-header {
        flex-direction: column;
    }
}

@media (max-width: 650px) {
    .dc-page {
        padding: 14px;
    }

    .dc-kpi-grid,
    .dc-grid {
        grid-template-columns: 1fr;
    }
}
'@

[System.IO.File]::WriteAllText($manager, $managerContent, [System.Text.UTF8Encoding]::new($false))
[System.IO.File]::WriteAllText($managerCss, $cssContent, [System.Text.UTF8Encoding]::new($false))

Push-Location $frontendRoot
try {
    npm run build
    if ($LASTEXITCODE -ne 0) {
        throw "Frontend build failed with exit code $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "DISEASE CONTROL GIS DASHBOARD - PHASE 1 COMPLETE" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "Updated:" -ForegroundColor Yellow
Write-Host "  src\pages\DiseaseControlManager.tsx"
Write-Host "  src\pages\DiseaseControlManager.css"
Write-Host ""
Write-Host "Backup files were created beside the originals." -ForegroundColor Gray
Write-Host "No backend files, migrations, or database structures were changed." -ForegroundColor Cyan
