import React, { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  LabelList,
  Legend,
  Pie,
  PieChart,
  PolarAngleAxis,
  RadialBar,
  RadialBarChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { getToken } from "../utils/token";
import "./VaccinationKpiOverview.css";

type Vaccine = { vaccine_type: string | null; disease_name: string | null; animal_group: string | null; animal_group_name: string | null; vaccine_brand: string | null; units: number; counties: number; target_population: number; vaccinated_animals: number; remaining_animals: number; coverage_percent: number; progress_percent: number; status: string };
type County = { county_code: string | number | null; county_name: string | null; units: number; target_population: number; vaccinated_animals: number; remaining_animals: number; coverage_percent: number; progress_percent: number; status: string };
type Surveillance = { label: string; records: number; total_animals: number; positive_count: number; negative_count: number; suspicious_count: number };
type InventoryItem = { vaccine_type: string | null; vaccine_brand: string | null; manufacturer: string | null; batch_number: string | null; province_name: string | null; county_name: string | null; unit_code: string | null; unit_name: string | null; package_count: number; expiration_date: string | null; days_to_expiry: number | null };
type Booster = { severity: "OVERDUE" | "DUE_SOON"; county_code: string | number | null; county_name: string | null; unit_code: string | null; unit_name: string | null; vaccine_type: string | null; animal_group_name: string | null; last_vaccination_date: string; due_date: string; days_until_due: number; immunity_days: number };
type Overview = { summary: { units: number; counties: number; vaccine_types: number; target_population: number; vaccinated_animals: number; remaining_animals: number; coverage_percent: number; coverage_is_valid: boolean; province_names: string[] }; executive_vaccines: string[]; vaccines: Vaccine[]; counties: County[]; booster_alerts: Booster[]; booster_by_county: Array<{ county_code: string | number | null; county_name: string | null; due_soon: number; overdue: number; total_alerts: number; units: Booster[] }>; booster_alert_days: number; fmd_immunity_days: number; default_immunity_days: number; inventory_summary: { total_lots: number; total_packages: number; near_expiry_days: number; near_expiry_lots: number; near_expiry: InventoryItem[]; inventory: InventoryItem[] }; surveillance: Surveillance[]; generated_at: string };

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";
const EXECUTIVE = ["شاربن", "تب برفکی", "آبله", "لمپی‌اسکین", "PPR", "FD REV1", "بروسلوز میش", "RD IRIBA", "FD IRIBA", "هاری"];
const COLORS = ["#18d7f5", "#38a8ff", "#7b8cff", "#35e28b", "#f6c453", "#ff6b86", "#b084ff", "#2dd4bf", "#55d98a", "#ff9d5c"];
const fmt = (v: number | string | null | undefined) => new Intl.NumberFormat("fa-IR").format(Number(v || 0));
const pct = (v: number | string | null | undefined) => `${Number(v || 0).toFixed(1)}%`;
const normalize = (s: string | null | undefined) => String(s || "").replace(/\u200c/g, "").toLowerCase();
const statusText = (s: string) => ({ EXCELLENT: "عالی", ON_TRACK: "در مسیر", WARNING: "نیازمند توجه", CRITICAL: "بحرانی", NO_TARGET: "بدون هدف", NO_COVERAGE: "بدون پوشش" } as Record<string, string>)[s] || s || "-";
const statusClass = (s: string) => s === "CRITICAL" || s === "NO_COVERAGE" ? "danger" : s === "WARNING" ? "warning" : s === "ON_TRACK" ? "info" : "success";
const statusColor = (s: string) => s === "CRITICAL" || s === "NO_COVERAGE" ? "#ff5f7d" : s === "WARNING" ? "#f6c453" : s === "ON_TRACK" ? "#38a8ff" : "#35e28b";
const dateFa = (v: string | null | undefined) => { if (!v) return "-"; const d = new Date(v); return Number.isNaN(d.getTime()) ? v : new Intl.DateTimeFormat("fa-IR").format(d); };

function matchesExecutive(label: string, v: Vaccine) {
  const type = normalize(v.vaccine_type), brand = normalize(v.vaccine_brand), disease = normalize(v.disease_name);
  if (label === "شاربن") return type.includes("شاربن") || disease.includes("شاربن");
  if (label === "تب برفکی") return type.includes("تب برفکی") || disease.includes("تب برفکی");
  if (label === "آبله") return type.includes("آبله") || disease.includes("آبله");
  if (label === "لمپی‌اسکین") return type.includes("لمپی") || type.includes("لامپی") || disease.includes("لمپی") || disease.includes("لامپی");
  if (label === "PPR") return type === "ppr" || type.includes("طاعون نشخوارکنندگان کوچک") || disease.includes("طاعون نشخوارکنندگان کوچک");
  if (label === "FD REV1") return type.includes("rev1") || brand.includes("rev1") || brand.includes("ریو وان");
  if (label === "بروسلوز میش") return type.includes("بروسلوز دام سبک") || (type.includes("بروسلوز") && v.animal_group === "LIGHT_LIVESTOCK");
  if (label === "RD IRIBA") return (type.includes("iriba") || brand.includes("iriba")) && (type.includes("rd") || brand.includes("rd"));
  if (label === "FD IRIBA") return (type.includes("iriba") || brand.includes("iriba")) && (type.includes("fd") || brand.includes("fd"));
  if (label === "هاری") return type.includes("هاری") || disease.includes("هاری");
  return false;
}

export default function KPIAnalysis() {
  const navigate = useNavigate();
  const [data, setData] = useState<Overview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [openCounty, setOpenCounty] = useState<string | number | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    fetch(`${API_BASE}/gis/kpi/vaccination/overview`, { headers: { Accept: "application/json", Authorization: `Bearer ${getToken()}` }, signal: controller.signal })
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then(setData)
      .catch(e => { if (e?.name !== "AbortError") setError("خطا در دریافت داشبورد واکسیناسیون"); })
      .finally(() => { if (!controller.signal.aborted) setLoading(false); });
    return () => controller.abort();
  }, []);

  const executiveCards = useMemo(() => EXECUTIVE.map(label => {
    const rows = (data?.vaccines || []).filter(v => matchesExecutive(label, v));
    if (!rows.length) return { label, data: null as Vaccine | null };
    const target = rows.reduce((s, r) => s + Number(r.target_population || 0), 0);
    const vaccinated = rows.reduce((s, r) => s + Number(r.vaccinated_animals || 0), 0);
    const coverage = target ? vaccinated * 100 / target : 0;
    const status = coverage >= 90 ? "EXCELLENT" : coverage >= 75 ? "ON_TRACK" : coverage >= 50 ? "WARNING" : coverage > 0 ? "CRITICAL" : "NO_COVERAGE";
    return { label, data: { ...rows[0], target_population: target, vaccinated_animals: vaccinated, remaining_animals: Math.max(target - vaccinated, 0), coverage_percent: coverage, progress_percent: coverage, status } as Vaccine };
  }), [data]);

  const vaccineChart = useMemo(() => executiveCards.filter(x => x.data).map((x, i) => ({ name: x.label, coverage: Number(x.data?.coverage_percent || 0), color: COLORS[i % COLORS.length], status: x.data?.status || "" })), [executiveCards]);
  const countyChart = useMemo(() => [...(data?.counties || [])].sort((a, b) => Number(b.coverage_percent || 0) - Number(a.coverage_percent || 0)).slice(0, 12).map(c => ({ ...c, label: c.county_name || "بدون نام", coverage: Number(c.coverage_percent || 0), fill: statusColor(c.status) })), [data]);
  const coverageSplit = useMemo(() => [{ name: "واکسینه‌شده", value: Number(data?.summary.vaccinated_animals || 0) }, { name: "باقی‌مانده", value: Number(data?.summary.remaining_animals || 0) }].filter(x => x.value > 0), [data]);
  const statusSummary = useMemo(() => {
    const rows = (data?.vaccines || []).filter(v => v.target_population > 0);
    return ["EXCELLENT", "ON_TRACK", "WARNING", "CRITICAL"].map((status, i) => ({ name: statusText(status), value: rows.filter(v => v.status === status).length, fill: ["#35e28b", "#38a8ff", "#f6c453", "#ff5f7d"][i] })).filter(x => x.value);
  }, [data]);
  const alertCountyChart = useMemo(() => (data?.booster_by_county || []).slice(0, 10).map(x => ({ name: x.county_name || "-", overdue: x.overdue, dueSoon: x.due_soon })), [data]);
  const selectedCounty = useMemo(() => data?.booster_by_county.find(c => String(c.county_code) === String(openCounty)) || null, [data, openCounty]);
  const coverageGauge = Math.min(100, Math.max(0, Number(data?.summary.coverage_percent || 0)));

  if (loading) return <div className="vaccination-overview" dir="rtl"><div className="section-block loading"><div className="loader" /><h2>در حال ساخت مرکز فرماندهی واکسیناسیون…</h2><p>شاخص‌ها و نمودارهای مدیریتی در حال دریافت هستند.</p></div></div>;
  if (error || !data) return <div className="vaccination-overview" dir="rtl"><div className="section-block error"><h2>{error || "اطلاعاتی برای نمایش وجود ندارد"}</h2><button onClick={() => window.location.reload()}>تلاش مجدد</button></div></div>;

  return <div className="vaccination-overview" dir="rtl">
    <header className="overview-header">
      <div className="overview-title-wrap">
        <div className="eyebrow">GIS-VET · مرکز فرماندهی واکسیناسیون</div>
        <h1>داشبورد مدیریتی پوشش واکسیناسیون</h1>
        <p>یک نمای عملیاتی برای دیدن پوشش، شکاف جمعیت هدف، رتبه شهرستان‌ها، هشدارهای ایمنی‌سازی و موجودی واکسن؛ بدون شلوغی و با تمرکز روی تصمیم مدیریتی.</p>
        <div className="header-chips"><span>استان: {data.summary.province_names.join("، ") || "-"}</span><span>آخرین داده: {dateFa(data.generated_at)}</span><span>آستانه هشدار: {data.booster_alert_days} روز</span></div>
      </div>
      <div className="hero-gauge">
        <div className="gauge-chart"><ResponsiveContainer width="100%" height="100%"><RadialBarChart innerRadius="70%" outerRadius="100%" startAngle={210} endAngle={-30} data={[{ value: coverageGauge, fill: "#22d3ee" }]}><PolarAngleAxis type="number" domain={[0, 100]} tick={false} /><RadialBar dataKey="value" cornerRadius={18} background={{ fill: "#12364b" }} /></RadialBarChart></ResponsiveContainer><div className="gauge-center"><strong>{pct(coverageGauge)}</strong><span>پوشش کل</span></div></div>
        <div className="gauge-copy"><b>{data.summary.coverage_is_valid ? "پوشش معتبر" : "پوشش نیازمند بررسی"}</b><span>{data.summary.coverage_is_valid ? "مخرج شاخص از جمعیت هدف واقعی ساخته شده است." : "جمعیت هدف برای این نما کامل نیست."}</span></div>
      </div>
    </header>

    <section className="summary-grid">
      <div className="summary-card"><span>واحدهای درگیر</span><strong>{fmt(data.summary.units)}</strong><small>واحد اپیدمیولوژیک</small><b className="summary-icon">◈</b></div>
      <div className="summary-card"><span>شهرستان‌های درگیر</span><strong>{fmt(data.summary.counties)}</strong><small>شهرستان دارای داده KPI</small><b className="summary-icon">⌖</b></div>
      <div className="summary-card"><span>دام واکسینه‌شده</span><strong>{fmt(data.summary.vaccinated_animals)}</strong><small>از {fmt(data.summary.target_population)} دام هدف</small><b className="summary-icon">✓</b></div>
      <div className="summary-card alert-summary"><span>هشدار ایمنی‌سازی</span><strong>{fmt(data.booster_alerts.length)}</strong><small>{fmt(data.booster_alerts.filter(x => x.severity === "OVERDUE").length)} مورد سررسید گذشته</small><b className="summary-icon">!</b></div>
    </section>

    <section className="section-block executive-block">
      <div className="section-head"><div><h2>شاخص‌های اجرایی واکسن</h2><p>کارت‌ها قابل کلیک‌اند؛ برای هر برنامه مستقیماً وارد گزارش جزئیات شوید.</p></div><span className="section-kicker">{vaccineChart.length} برنامه دارای داده</span></div>
      <div className="vaccine-grid">{executiveCards.map(({ label, data: v }, index) => <button key={label} className={`vaccine-card ${v ? "has-data" : "no-data"}`} onClick={() => v && navigate(`/gis/kpi/vaccination/vaccine/${encodeURIComponent(v.vaccine_type || label)}?animal_group=${encodeURIComponent(v.animal_group || "")}`)}><div className="vaccine-accent" style={{ background: COLORS[index % COLORS.length] }} /><div className="vaccine-top"><span className="vaccine-name">{label}</span>{v && <span className={`status-badge ${statusClass(v.status)}`}>{statusText(v.status)}</span>}</div>{v ? <><div className="vaccine-coverage">{pct(v.coverage_percent)}</div><div className="progress-track"><span style={{ width: `${Math.min(100, Math.max(0, Number(v.coverage_percent || 0)))}%`, background: COLORS[index % COLORS.length] }} /></div><div className="vaccine-stats"><span>هدف<b>{fmt(v.target_population)}</b></span><span>واکسینه<b>{fmt(v.vaccinated_animals)}</b></span><span>باقی‌مانده<b>{fmt(v.remaining_animals)}</b></span></div><div className="vaccine-meta">{v.animal_group_name || "گروه نامشخص"} · {v.vaccine_brand || "برند نامشخص"}</div></> : <div className="missing">برای این برنامه داده KPI نرمال‌شده پیدا نشد.</div>}</button>)}</div>
    </section>

    <section className="dashboard-charts main-charts">
      <div className="section-block chart-card-large"><div className="section-head"><div><h2>رتبه پوشش برنامه‌ها</h2><p>محور ۱۰۰٪ ثابت است تا تفاوت عملکرد واقعاً دیده شود.</p></div><span className="chart-badge">مقایسه اجرایی</span></div><div className="chart-wrap tall"><ResponsiveContainer width="100%" height="100%"><BarChart data={vaccineChart} layout="vertical" margin={{ top: 8, right: 18, left: 24, bottom: 8 }} barCategoryGap="18%"><CartesianGrid strokeDasharray="3 3" horizontal={false} /><XAxis type="number" domain={[0, 100]} tickFormatter={x => `${x}%`} tickLine={false} /><YAxis type="category" dataKey="name" width={100} tickLine={false} axisLine={false} /><ReferenceLine x={80} stroke="#f6c453" strokeDasharray="6 5" label={{ value: "هدف ۸۰٪", fill: "#f6c453", fontSize: 10, position: "insideTop" }} /><Tooltip formatter={value => pct(Number(value || 0))} /><Bar dataKey="coverage" name="پوشش" radius={[0, 9, 9, 0]}>{vaccineChart.map(x => <Cell key={x.name} fill={x.color} />)}<LabelList dataKey="coverage" position="right" formatter={(v: any) => pct(Number(v || 0))} fill="#dff9ff" fontSize={10} /></Bar></BarChart></ResponsiveContainer></div></div>
      <div className="section-block chart-card-small"><div className="section-head"><div><h2>ترکیب جمعیت هدف</h2><p>نسبت دام واکسینه‌شده به باقی‌مانده.</p></div></div><div className="donut-wrap"><ResponsiveContainer width="100%" height="100%"><PieChart><Pie data={coverageSplit} dataKey="value" nameKey="name" innerRadius="62%" outerRadius="82%" paddingAngle={5} stroke="none">{coverageSplit.map((_, i) => <Cell key={i} fill={i === 0 ? "#22d3ee" : "#243e54"} />)}</Pie><Tooltip formatter={value => fmt(Number(value || 0))} /><Legend verticalAlign="bottom" height={30} /></PieChart></ResponsiveContainer><div className="donut-center"><strong>{pct(data.summary.coverage_percent)}</strong><span>پوشش</span></div></div><div className="mini-metrics"><div><b>{fmt(data.summary.target_population)}</b><span>جمعیت هدف</span></div><div><b>{fmt(data.summary.remaining_animals)}</b><span>باقی‌مانده</span></div></div></div>
    </section>

    <section className="dashboard-split">
      <div className="section-block"><div className="section-head"><div><h2>عملکرد شهرستان‌ها</h2><p>رتبه‌بندی ۱۲ شهرستان اول؛ رنگ هر ستون وضعیت مدیریتی را نشان می‌دهد.</p></div><span className="section-kicker">{fmt(data.counties.length)} شهرستان</span></div><div className="chart-wrap county-chart"><ResponsiveContainer width="100%" height="100%"><BarChart data={countyChart} layout="vertical" margin={{ top: 8, right: 18, left: 12, bottom: 8 }} barCategoryGap="16%"><CartesianGrid strokeDasharray="3 3" horizontal={false} /><XAxis type="number" domain={[0, 100]} tickFormatter={x => `${x}%`} tickLine={false} /><YAxis type="category" dataKey="label" width={92} tickLine={false} axisLine={false} /><ReferenceLine x={80} stroke="#f6c453" strokeDasharray="5 5" /><Tooltip formatter={value => pct(Number(value || 0))} /><Bar dataKey="coverage" name="پوشش" radius={[0, 8, 8, 0]} onClick={(entry: any) => entry?.payload?.county_code != null && setOpenCounty(entry.payload.county_code)}>{countyChart.map(x => <Cell key={String(x.county_code)} fill={x.fill} />)}<LabelList dataKey="coverage" position="right" formatter={(v: any) => pct(Number(v || 0))} fill="#dff9ff" fontSize={9} /></Bar></BarChart></ResponsiveContainer></div></div>
      <div className="section-block"><div className="section-head"><div><h2>وضعیت برنامه‌ها</h2><p>تعداد KPIهای واکسن بر اساس وضعیت عملکرد.</p></div></div><div className="status-chart"><ResponsiveContainer width="100%" height="100%"><PieChart><Pie data={statusSummary} dataKey="value" nameKey="name" innerRadius="58%" outerRadius="78%" paddingAngle={5} stroke="none">{statusSummary.map(x => <Cell key={x.name} fill={x.fill} />)}</Pie><Tooltip formatter={(v) => fmt(Number(v || 0))} /><Legend verticalAlign="bottom" height={42} /></PieChart></ResponsiveContainer><div className="status-center"><strong>{fmt(statusSummary.reduce((s, x) => s + x.value, 0))}</strong><span>KPI</span></div></div></div>
    </section>

    {selectedCounty && <section className="section-block county-alert-detail"><div className="section-head"><div><h2>هشدارهای شهرستان {selectedCounty.county_name || "-"}</h2><p>{selectedCounty.total_alerts} هشدار فعال · {selectedCounty.overdue} سررسید گذشته · {selectedCounty.due_soon} نزدیک سررسید</p></div><button className="ghost-button" onClick={() => setOpenCounty(null)}>بستن</button></div><div className="alert-grid">{selectedCounty.units.slice(0, 12).map(a => <button key={`${a.unit_code}-${a.vaccine_type}-${a.due_date}`} className={`alert-row ${a.severity === "OVERDUE" ? "overdue" : "due-soon"}`} onClick={() => navigate(`/gis/kpi/vaccination/unit/${encodeURIComponent(a.unit_code || "")}`)}><span><b>{a.unit_name || a.unit_code || "واحد نامشخص"}</b><small>{a.vaccine_type || "-"} · {a.animal_group_name || "-"}</small></span><strong>{a.severity === "OVERDUE" ? `${Math.abs(a.days_until_due)} روز گذشته` : `${a.days_until_due} روز مانده`}</strong></button>)}</div></section>}

    <section className="dashboard-split bottom-analytics">
      <div className="section-block"><div className="section-head"><div><h2>هشدار به تفکیک شهرستان</h2><p>اولویت‌بندی حجم سررسید گذشته و نزدیک به سررسید.</p></div></div><div className="chart-wrap alert-chart"><ResponsiveContainer width="100%" height="100%"><BarChart data={alertCountyChart} layout="vertical" margin={{ top: 8, right: 15, left: 12, bottom: 8 }} barCategoryGap="18%"><CartesianGrid strokeDasharray="3 3" horizontal={false} /><XAxis type="number" tickLine={false} /><YAxis type="category" dataKey="name" width={90} tickLine={false} axisLine={false} /><Tooltip /><Legend /><Bar dataKey="overdue" name="سررسید گذشته" stackId="a" fill="#ff5f7d" radius={[0, 0, 0, 0]} /><Bar dataKey="dueSoon" name="نزدیک سررسید" stackId="a" fill="#f6c453" radius={[0, 8, 8, 0]} /></BarChart></ResponsiveContainer></div></div>
      <div className="section-block"><div className="section-head"><div><h2>موجودی واکسن</h2><p>لات‌ها و اقلام نزدیک به انقضا.</p></div></div><div className="inventory-summary"><div><b>{fmt(data.inventory_summary.total_lots)}</b><span>لات</span></div><div><b>{fmt(data.inventory_summary.total_packages)}</b><span>بسته</span></div><div className="expiry"><b>{fmt(data.inventory_summary.near_expiry_lots)}</b><span>نزدیک انقضا</span></div></div><div className="expiry-list">{data.inventory_summary.near_expiry.slice(0, 6).map((x, i) => <div className="expiry-row" key={`${x.batch_number}-${i}`}><span><b>{x.vaccine_type || x.vaccine_brand || "واکسن"}</b><small>{x.batch_number || "لات نامشخص"} · {x.county_name || "-"}</small></span><strong>{x.days_to_expiry == null ? "-" : `${x.days_to_expiry} روز`}</strong></div>)}{!data.inventory_summary.near_expiry.length && <div className="empty-state">مورد نزدیک به انقضا ثبت نشده است.</div>}</div></div>
    </section>

    <section className="section-block surveillance-block"><div className="section-head"><div><h2>پایش بیماری‌های مشترک</h2><p>حجم پایش و نسبت نتایج مثبت، منفی و مشکوک.</p></div></div><div className="surveillance-grid">{data.surveillance.map(s => <div className="surveillance-card" key={s.label}><span>{s.label}</span><strong>{fmt(s.records)}</strong><small>{fmt(s.total_animals)} دام پایش‌شده · {fmt(s.positive_count)} مثبت</small><div className="surveillance-bar"><i style={{ width: `${s.total_animals ? Math.min(100, s.positive_count * 100 / s.total_animals) : 0}%` }} /></div><div className="surveillance-tags"><em>منفی {fmt(s.negative_count)}</em><em>مشکوک {fmt(s.suspicious_count)}</em></div></div>)}</div></section>

    <section className="section-block rules-block"><div className="section-head"><div><h2>قواعد محاسبه</h2><p>پارامترهای فعال برای تفسیر موعد ایمنی و هشدار.</p></div></div><div className="rule-grid"><div><span>موعد ایمنی پیش‌فرض</span><b>{data.default_immunity_days} روز</b></div><div><span>موعد ایمنی تب برفکی</span><b>{data.fmd_immunity_days} روز</b></div><div><span>شروع آلارم</span><b>{data.booster_alert_days} روز قبل</b></div></div></section>
  </div>;
}
