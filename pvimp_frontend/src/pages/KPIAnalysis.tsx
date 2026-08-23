import React, { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
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

function fmt(v: number | string | null | undefined) { return new Intl.NumberFormat("fa-IR").format(Number(v || 0)); }
function pct(v: number | string | null | undefined) { return `${Number(v || 0).toFixed(1)}%`; }
function dateFa(v: string | null | undefined) { if (!v) return "-"; const d = new Date(v); return Number.isNaN(d.getTime()) ? v : new Intl.DateTimeFormat("fa-IR").format(d); }
function normalize(s: string | null | undefined) { return String(s || "").replace(/\u200c/g, "").toLowerCase(); }
function statusText(s: string) { return ({ EXCELLENT: "عالی", ON_TRACK: "در مسیر", WARNING: "نیازمند توجه", CRITICAL: "بحرانی", NO_TARGET: "بدون جمعیت هدف", NO_COVERAGE: "بدون پوشش" } as Record<string,string>)[s] || s || "-"; }
function statusClass(s: string) { return s === "CRITICAL" || s === "NO_COVERAGE" ? "danger" : s === "WARNING" ? "warning" : s === "ON_TRACK" ? "info" : "success"; }

function matchesExecutive(label: string, v: Vaccine) {
  const type = normalize(v.vaccine_type); const brand = normalize(v.vaccine_brand); const disease = normalize(v.disease_name);
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
  const [selectedVaccine, setSelectedVaccine] = useState("تب برفکی");
  const [openCounty, setOpenCounty] = useState<string | number | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    async function load() {
      try {
        setLoading(true); setError("");
        const response = await fetch(`${API_BASE}/gis/kpi/vaccination/overview`, { headers: { Accept: "application/json", Authorization: `Bearer ${getToken()}` }, signal: controller.signal });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        setData(await response.json());
      } catch (e: any) { if (e?.name !== "AbortError") setError("خطا در دریافت داشبورد واکسیناسیون"); }
      finally { if (!controller.signal.aborted) setLoading(false); }
    }
    load(); return () => controller.abort();
  }, []);

  const executiveCards = useMemo(() => EXECUTIVE.map((label) => {
    const rows = (data?.vaccines || []).filter((v) => matchesExecutive(label, v));
    if (!rows.length) return { label, data: null };
    const target = rows.reduce((s, r) => s + Number(r.target_population || 0), 0);
    const vaccinated = rows.reduce((s, r) => s + Number(r.vaccinated_animals || 0), 0);
    const coverage = target ? vaccinated * 100 / target : 0;
    return { label, data: { ...rows[0], target_population: target, vaccinated_animals: vaccinated, remaining_animals: Math.max(target - vaccinated, 0), coverage_percent: coverage, progress_percent: coverage, status: coverage >= 90 ? "EXCELLENT" : coverage >= 75 ? "ON_TRACK" : coverage >= 50 ? "WARNING" : coverage > 0 ? "CRITICAL" : "NO_COVERAGE" } as Vaccine };
  }), [data]);

  const selectedRows = useMemo(() => (data?.vaccines || []).filter(v => normalize(v.vaccine_type).includes(normalize(selectedVaccine)) || normalize(v.disease_name).includes(normalize(selectedVaccine))), [data, selectedVaccine]);
  const chart = useMemo(() => (data?.counties || []).map(c => ({ ...c, label: c.county_name || "بدون نام", coverage: c.coverage_percent })), [data]);

  if (loading) return <div className="vaccination-overview" dir="rtl"><div className="section-block loading"><div className="loader" /><h2>در حال بارگذاری داشبورد واکسیناسیون…</h2><p>داده‌های KPI، موجودی و آلارم‌ها در یک درخواست مدیریتی در حال دریافت است.</p></div></div>;
  if (error || !data) return <div className="vaccination-overview" dir="rtl"><div className="section-block error"><h2>{error || "اطلاعاتی برای نمایش وجود ندارد"}</h2><button onClick={() => window.location.reload()}>تلاش مجدد</button></div></div>;

  return (
    <div className="vaccination-overview" dir="rtl">
      <header className="overview-header">
        <div><div className="eyebrow">GIS-VET · داشبورد مدیریتی استان</div><h1>تحلیل KPI واکسیناسیون و عملکرد مبارزه با بیماری‌های واگیر و مشترک</h1><p>پوشش و پیشرفت نسبت به جمعیت دامی، نوع دام، پایش بیماری‌های مشترک، موجودی واکسن و موعد ایمنی‌سازی.</p></div>
        <div className="header-meta"><span>استان: {data.summary.province_names.join("، ") || "-"}</span><span>آخرین به‌روزرسانی: {dateFa(data.generated_at)}</span><span>آلارم موعد: {data.booster_alert_days} روز قبل</span></div>
      </header>

      <section className="summary-grid">
        <div className="summary-card"><span>واحدهای درگیر</span><strong>{fmt(data.summary.units)}</strong><small>واحد اپیدمیولوژیک</small></div>
        <div className="summary-card"><span>شهرستان‌های درگیر</span><strong>{fmt(data.summary.counties)}</strong><small>در سطح داده موجود</small></div>
        <div className="summary-card"><span>دام واکسینه‌شده</span><strong>{fmt(data.summary.vaccinated_animals)}</strong><small>جمع رکوردهای واکسیناسیون</small></div>
        <div className="summary-card"><span>هشدارهای ایمنی‌سازی</span><strong>{fmt(data.booster_alerts.length)}</strong><small>موعد رسیده یا تا ۳ هفته آینده</small></div>
      </section>

      <section className="section-block">
        <div className="section-head"><div><h2>واکسیناسیون و عملکرد مبارزه</h2><p>هر کارت با جمعیت هدف همان گروه دام محاسبه شده است؛ پوشش واکسن‌های مختلف با هم تجمیع نمی‌شود.</p></div></div>
        <div className="vaccine-grid">
          {executiveCards.map(({ label, data: v }) => (
            <button key={label} className={`vaccine-card ${v ? "has-data" : "no-data"}`} onClick={() => v && (setSelectedVaccine(v.vaccine_type || label), navigate(`/gis/kpi/vaccination/vaccine/${encodeURIComponent(v.vaccine_type || label)}?animal_group=${encodeURIComponent(v.animal_group || "")}`))}>
              <div className="vaccine-top"><span className="vaccine-name">{label}</span>{v && <span className={`status-badge ${statusClass(v.status)}`}>{statusText(v.status)}</span>}</div>
              {v ? <><div className="vaccine-coverage">{pct(v.coverage_percent)}</div><div className="progress-track"><span style={{ width: `${Math.min(100, Math.max(0, Number(v.coverage_percent || 0)))}%` }} /></div><div className="vaccine-stats"><span>هدف <b>{fmt(v.target_population)}</b></span><span>واکسینه <b>{fmt(v.vaccinated_animals)}</b></span><span>باقی‌مانده <b>{fmt(v.remaining_animals)}</b></span></div><div className="vaccine-meta">نوع دام: {v.animal_group_name || "-"} · پیشرفت: {pct(v.progress_percent)}</div></> : <div className="missing">داده مطابق این نام در KPI نرمال‌شده پیدا نشد.</div>}
            </button>
          ))}
        </div>
      </section>

      <section className="two-column">
        <div className="section-block">
          <div className="section-head"><div><h2>پوشش به تفکیک شهرستان</h2><p>نمودار با انتخاب واکسن/برنامه تغییر می‌کند و کلیک روی شهرستان Drill-down را باز می‌کند.</p></div><select value={selectedVaccine} onChange={e => setSelectedVaccine(e.target.value)}>{EXECUTIVE.map(x => <option key={x}>{x}</option>)}</select></div>
          <div className="chart-wrap"><ResponsiveContainer width="100%" height={360}><BarChart data={chart} layout="vertical" margin={{ top: 8, right: 20, left: 20, bottom: 8 }}><CartesianGrid strokeDasharray="3 3" /><XAxis type="number" domain={[0, 100]} tickFormatter={x => `${x}%`} /><YAxis type="category" dataKey="label" width={100} /><Tooltip formatter={(x) => pct(Number(x || 0))} /><Bar dataKey="coverage" name="پوشش" fill="#20a4ff" radius={[0, 5, 5, 0]} onClick={(entry: any) => { const code = entry?.payload?.county_code; if (code != null) setOpenCounty(code); }} /></BarChart></ResponsiveContainer></div>
          {selectedRows.length > 0 && <div className="selected-note">ردیف‌های KPI مرتبط با «{selectedVaccine}»: {selectedRows.length} گروه دام</div>}
        </div>
        <div className="section-block alert-panel"><div className="section-head"><div><h2>آلارم‌های موعد ایمنی‌سازی</h2><p>ایمنی یک‌ساله؛ تب برفکی ۶ ماهه. آلارم از ۳ هفته قبل فعال می‌شود.</p></div></div>{data.booster_alerts.length ? data.booster_alerts.slice(0, 8).map(a => <button key={`${a.unit_code}-${a.vaccine_type}-${a.animal_group_name}`} className={`alert-row ${a.severity === "OVERDUE" ? "danger" : "warning"}`} onClick={() => navigate(`/gis/kpi/vaccination/unit/${encodeURIComponent(a.unit_code || "")}`)}><span><b>{a.unit_name || a.unit_code}</b><small>{a.county_name || "-"} · {a.vaccine_type || "-"} · {a.animal_group_name || "-"}</small></span><strong>{a.severity === "OVERDUE" ? "رسیده" : `${Math.max(0, a.days_until_due)} روز مانده`}</strong></button>) : <div className="empty-state">در بازه ۳ هفته آینده و موارد عقب‌افتاده، هشداری ثبت نشده است.</div>}</div>
      </section>

      <section className="section-block" style={{ marginTop: 14 }}>
        <div className="section-head"><div><h2>موعد تزریق بعدی به تفکیک شهرستان و واحد</h2><p>ابتدا شهرستان را باز کنید؛ سپس واحدهای دارای موعد رسیده/نزدیک نمایش داده می‌شوند.</p></div></div>
        <div className="county-drill">{data.booster_by_county.length ? data.booster_by_county.map(c => <div key={String(c.county_code)} className="county-row"><button className="county-summary" onClick={() => setOpenCounty(openCounty === c.county_code ? null : c.county_code)}><span>{openCounty === c.county_code ? "−" : "+"}</span><b>{c.county_name || c.county_code || "-"}</b><em>{fmt(c.total_alerts)} هشدار</em><small>عقب‌افتاده: {fmt(c.overdue)} · نزدیک موعد: {fmt(c.due_soon)}</small></button>{openCounty === c.county_code && <div className="unit-drill">{c.units.map(u => <button key={`${u.unit_code}-${u.vaccine_type}-${u.animal_group_name}`} onClick={() => navigate(`/gis/kpi/vaccination/unit/${encodeURIComponent(u.unit_code || "")}`)}><span>{u.unit_name || u.unit_code}</span><small>{u.vaccine_type || "-"} · {u.animal_group_name || "-"}</small><strong className={u.severity === "OVERDUE" ? "danger-text" : "warning-text"}>{u.severity === "OVERDUE" ? "موعد گذشته" : `${Math.max(0, u.days_until_due)} روز مانده`} · {dateFa(u.due_date)}</strong></button>)}</div>}</div>) : <div className="empty-state">واحدی با موعد تزریق در بازه هشدار پیدا نشد.</div>}</div>
      </section>

      <section className="three-column">{data.surveillance.map(s => <div className="surveillance-card" key={s.label}><span>{s.label}</span><strong>{fmt(s.total_animals)}</strong><small>مجموع دام/تست ثبت‌شده</small><div className="surveillance-stats"><i>مثبت {fmt(s.positive_count)}</i><i>منفی {fmt(s.negative_count)}</i><i>مشکوک {fmt(s.suspicious_count)}</i></div></div>)}</section>

      <section className="two-column inventory-grid">
        <div className="section-block"><div className="section-head"><div><h2>موجودی واکسن‌ها</h2><p>مجموع سری‌ها و بسته‌های موجود در داده فعلی.</p></div></div><div className="inventory-summary"><div><b>{fmt(data.inventory_summary.total_lots)}</b><span>سری موجودی</span></div><div><b>{fmt(data.inventory_summary.total_packages)}</b><span>بسته</span></div><div className="expiry"><b>{fmt(data.inventory_summary.near_expiry_lots)}</b><span>نزدیک انقضا</span></div></div><div className="table-wrap"><table><thead><tr><th>واکسن</th><th>برند</th><th>موجودی</th><th>انقضا</th><th>واحد</th></tr></thead><tbody>{data.inventory_summary.inventory.slice(0, 10).map((x,i) => <tr key={`${x.batch_number}-${i}`}><td>{x.vaccine_type || "-"}</td><td>{x.vaccine_brand || "-"}</td><td>{fmt(x.package_count)}</td><td>{dateFa(x.expiration_date)} {x.days_to_expiry != null && <small>({x.days_to_expiry} روز)</small>}</td><td>{x.unit_name || x.county_name || "-"}</td></tr>)}</tbody></table></div></div>
        <div className="section-block expiry-panel"><div className="section-head"><div><h2>واکسن‌های نزدیک انقضا</h2><p>آستانه فعلی {data.inventory_summary.near_expiry_days} روز است و از API قابل تنظیم است.</p></div></div>{data.inventory_summary.near_expiry.length ? data.inventory_summary.near_expiry.slice(0, 10).map((x,i) => <div className="expiry-row" key={`${x.batch_number}-${i}`}><span><b>{x.vaccine_type || "-"}</b><small>{x.vaccine_brand || "-"} · سری {x.batch_number || "-"}</small></span><strong className={Number(x.days_to_expiry) <= 0 ? "danger-text" : "warning-text"}>{x.days_to_expiry == null ? "-" : x.days_to_expiry <= 0 ? "منقضی" : `${x.days_to_expiry} روز`}</strong></div>) : <div className="empty-state">موردی در آستانه فعلی پیدا نشد.</div>}</div>
      </section>

      <section className="section-block" style={{ marginTop: 14 }}><div className="section-head"><div><h2>قواعد محاسبه ایمنی‌سازی</h2><p>تاریخ آخرین تزریق هر واحد/واکسن/گروه دام از KPI نرمال‌شده گرفته شده و موعد بعدی محاسبه می‌شود.</p></div></div><div className="rule-grid"><div><b>واکسن‌های عادی</b><span>{fmt(data.default_immunity_days)} روز</span></div><div><b>تب برفکی</b><span>{fmt(data.fmd_immunity_days)} روز</span></div><div><b>شروع آلارم</b><span>{fmt(data.booster_alert_days)} روز قبل</span></div></div></section>
    </div>
  );
}
