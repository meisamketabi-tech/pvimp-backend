import React, { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams, useSearchParams } from "react-router-dom";
import { Bar, BarChart, CartesianGrid, Cell, LabelList, Pie, PieChart, PolarAngleAxis, RadialBar, RadialBarChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import api from "../services/api";
import "./VaccinationDashboard.css";

type County = { county_code: string | number; county_name: string; units: number; target_population: number; vaccinated_animals: number; remaining_animals: number; coverage_percent: number; status: string };
type Unit = { unit_code: string; unit_name: string; county_name: string | null; animal_group: string; animal_group_name: string; target_population: number; vaccinated_animals: number; remaining_animals: number; coverage_percent: number; status: string; vaccine_brand: string | null; records: number; last_vaccination_date: string | null };
type Vaccine = { vaccine_type: string; disease_name: string | null; animal_group: string; animal_group_name: string; vaccine_brand: string | null; target_population: number; vaccinated_animals: number; remaining_animals: number; coverage_percent: number };
type Report = { dashboard: { target_population: number; vaccinated_animals: number; remaining_animals: number; coverage_percent: number; coverage_is_valid: boolean }; counties: County[]; vaccines: Vaccine[]; units: Unit[] };
const fmt = (v: number | null | undefined) => new Intl.NumberFormat("fa-IR").format(Number(v || 0));
const pct = (v: number | null | undefined) => `${Number(v || 0).toFixed(1)}%`;
const statusText = (s: string) => ({ EXCELLENT: "عالی", ON_TRACK: "در مسیر", WARNING: "نیازمند توجه", CRITICAL: "بحرانی", NO_TARGET: "بدون هدف", NO_COVERAGE: "بدون پوشش" } as Record<string, string>)[s] || s || "-";
const statusClass = (s: string) => s === "CRITICAL" || s === "NO_COVERAGE" ? "danger" : s === "WARNING" ? "warning" : s === "ON_TRACK" ? "info" : "success";
const statusColor = (s: string) => s === "CRITICAL" || s === "NO_COVERAGE" ? "#ff5f7d" : s === "WARNING" ? "#f6c453" : s === "ON_TRACK" ? "#38a8ff" : "#35e28b";

export default function VaccinationVaccineReport() {
  const { vaccineType = "" } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  const animalGroup = searchParams.get("animal_group") || "";
  const countyCode = searchParams.get("county_code") || "";
  const [report, setReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!vaccineType) return;
    const controller = new AbortController();
    api.get("/api/v1/gis/kpi/vaccination/management-report", { params: { vaccine_type: vaccineType, animal_group: animalGroup || undefined, county_code: countyCode || undefined }, signal: controller.signal })
      .then(r => setReport(r.data))
      .catch((err: any) => { if (err?.code !== "ERR_CANCELED" && err?.name !== "CanceledError") setError("خطا در دریافت گزارش واکسن"); })
      .finally(() => { if (!controller.signal.aborted) setLoading(false); });
    return () => controller.abort();
  }, [vaccineType, animalGroup, countyCode]);

  const selectedCounty = useMemo(() => report?.counties.find(c => String(c.county_code) === countyCode) || null, [report, countyCode]);
  const v = useMemo(() => report?.vaccines.find(x => x.vaccine_type === vaccineType && (!animalGroup || x.animal_group === animalGroup)) || report?.vaccines[0], [report, vaccineType, animalGroup]);
  const coverage = Number(v?.coverage_percent ?? report?.dashboard.coverage_percent ?? 0);
  const status = coverage >= 90 ? "EXCELLENT" : coverage >= 75 ? "ON_TRACK" : coverage >= 50 ? "WARNING" : coverage > 0 ? "CRITICAL" : "NO_COVERAGE";
  const chart = useMemo(() => (report?.counties || []).map(c => ({ ...c, label: c.county_name || "-", coverage: Number(c.coverage_percent || 0), fill: statusColor(c.status) })).sort((a, b) => b.coverage - a.coverage), [report]);
  const split = useMemo(() => [{ name: "واکسینه‌شده", value: Number(v?.vaccinated_animals || report?.dashboard.vaccinated_animals || 0) }, { name: "باقی‌مانده", value: Number(v?.remaining_animals || report?.dashboard.remaining_animals || 0) }].filter(x => x.value > 0), [v, report]);
  const visibleUnits = report?.units || [];
  const gauge = Math.min(100, Math.max(0, coverage));
  function selectCounty(code: string | number) { const next = new URLSearchParams(searchParams); next.set("county_code", String(code)); setSearchParams(next); }

  if (loading) return <div className="dashboard-page" dir="rtl"><div className="detail-loading"><div className="loader" /><h2>در حال آماده‌سازی گزارش تحلیلی…</h2><p>داده شهرستان‌ها و واحدهای عملیاتی در حال بارگذاری است.</p></div></div>;
  if (error || !report) return <div className="dashboard-page" dir="rtl"><div className="detail-error"><h2>{error || "گزارش پیدا نشد"}</h2><button onClick={() => navigate("/gis/kpi/vaccination")}>بازگشت به داشبورد</button></div></div>;

  return <div className="dashboard-page" dir="rtl">
    <header className="dashboard-header">
      <button className="back-button" onClick={() => navigate("/gis/kpi/vaccination")}>← بازگشت به مرکز KPI</button>
      <div className="detail-title"><span className="detail-eyebrow">گزارش تحلیلی واکسن</span><h1>{v?.disease_name || vaccineType}</h1><p>{v?.animal_group_name || animalGroup || "گروه دام"} · {v?.vaccine_brand || "برند ثبت‌شده نامشخص"}</p><div className="detail-chips"><span>وضعیت: {statusText(status)}</span><span>{report.counties.length} شهرستان</span><span>{visibleUnits.length} واحد عملیاتی</span></div></div>
      <div className="detail-gauge"><div className="detail-gauge-chart"><ResponsiveContainer width="100%" height="100%"><RadialBarChart innerRadius="68%" outerRadius="100%" startAngle={210} endAngle={-30} data={[{ value: gauge, fill: statusColor(status) }]}><PolarAngleAxis type="number" domain={[0, 100]} tick={false} /><RadialBar dataKey="value" cornerRadius={16} background={{ fill: "#14374e" }} /></RadialBarChart></ResponsiveContainer><div className="detail-gauge-center"><strong>{pct(gauge)}</strong><span>پوشش</span></div></div><b className={statusClass(status)}>{statusText(status)}</b></div>
    </header>

    <section className="kpi-grid"><div className="kpi-card"><span>جمعیت هدف</span><strong>{fmt(v?.target_population || report.dashboard.target_population)}</strong><small>دام هدف‌گذاری‌شده</small></div><div className="kpi-card positive"><span>واکسینه‌شده</span><strong>{fmt(v?.vaccinated_animals || report.dashboard.vaccinated_animals)}</strong><small>ثبت‌شده در عملیات</small></div><div className="kpi-card warning-card"><span>باقی‌مانده</span><strong>{fmt(v?.remaining_animals || report.dashboard.remaining_animals)}</strong><small>نیازمند اقدام</small></div><div className="kpi-card focus"><span>پوشش معتبر</span><strong>{report.dashboard.coverage_is_valid ? pct(coverage) : "نامعتبر"}</strong><div className="detail-progress"><i style={{ width: `${gauge}%`, background: statusColor(status) }} /></div></div></section>

    <section className="detail-chart-grid"><div className="dashboard-panel chart-panel"><div className="panel-heading"><div><h2>رتبه‌بندی شهرستان‌ها</h2><p>ستون‌ها بر اساس پوشش مرتب شده‌اند؛ کلیک روی هر شهرستان Drill-down را فعال می‌کند.</p></div><span>{chart.length} شهرستان</span></div><div className="detail-bar-chart"><ResponsiveContainer width="100%" height="100%"><BarChart data={chart} layout="vertical" margin={{ top: 8, right: 22, left: 18, bottom: 8 }} barCategoryGap="16%"><CartesianGrid strokeDasharray="3 3" horizontal={false} /><XAxis type="number" domain={[0, 100]} tickFormatter={x => `${x}%`} tickLine={false} /><YAxis type="category" dataKey="label" width={100} tickLine={false} axisLine={false} /><ReferenceLine x={80} stroke="#f6c453" strokeDasharray="6 5" label={{ value: "هدف ۸۰٪", fill: "#f6c453", fontSize: 10, position: "insideTop" }} /><Tooltip formatter={x => pct(Number(x || 0))} /><Bar dataKey="coverage" name="پوشش" radius={[0, 8, 8, 0]} onClick={(entry: any) => entry?.payload?.county_code != null && selectCounty(entry.payload.county_code)}>{chart.map(x => <Cell key={String(x.county_code)} fill={x.fill} />)}<LabelList dataKey="coverage" position="right" formatter={(x: any) => pct(Number(x || 0))} fill="#e6fbff" fontSize={9} /></Bar></BarChart></ResponsiveContainer></div></div>
      <div className="dashboard-panel distribution-panel"><div className="panel-heading"><div><h2>ترکیب جمعیت</h2><p>نمایش مستقیم سهم واکسینه‌شده و باقی‌مانده.</p></div></div><div className="detail-donut"><ResponsiveContainer width="100%" height="100%"><PieChart><Pie data={split} dataKey="value" nameKey="name" innerRadius="62%" outerRadius="84%" paddingAngle={5} stroke="none">{split.map((_, i) => <Cell key={i} fill={i === 0 ? "#22d3ee" : "#2b455b"} />)}</Pie><Tooltip formatter={x => fmt(Number(x || 0))} /></PieChart></ResponsiveContainer><div className="detail-donut-center"><strong>{pct(coverage)}</strong><span>پوشش</span></div></div><div className="distribution-legend"><span><i className="dot vaccinated" />واکسینه‌شده <b>{fmt(v?.vaccinated_animals || report.dashboard.vaccinated_animals)}</b></span><span><i className="dot remaining" />باقی‌مانده <b>{fmt(v?.remaining_animals || report.dashboard.remaining_animals)}</b></span></div></div></section>

    <section className="dashboard-panel county-panel"><div className="panel-heading"><div><h2>{selectedCounty ? `واحدهای شهرستان ${selectedCounty.county_name}` : "عملکرد همه شهرستان‌ها"}</h2><p>{selectedCounty ? "برای مشاهده سایر شهرستان‌ها فیلتر را ببندید." : "شهرستان را از جدول یا نمودار انتخاب کنید."}</p></div>{selectedCounty && <button className="ghost-button" onClick={() => { const next = new URLSearchParams(searchParams); next.delete("county_code"); setSearchParams(next); }}>نمایش همه</button>}</div><div className="detail-table-wrap"><table><thead><tr><th>شهرستان</th><th>واحد</th><th>هدف</th><th>واکسینه</th><th>باقی‌مانده</th><th>پوشش</th><th>وضعیت</th></tr></thead><tbody>{report.counties.map(c => <tr key={String(c.county_code)} className={String(c.county_code) === countyCode ? "active-row" : ""} onClick={() => selectCounty(c.county_code)}><td><b>{c.county_name}</b></td><td>{fmt(c.units)}</td><td>{fmt(c.target_population)}</td><td>{fmt(c.vaccinated_animals)}</td><td>{fmt(c.remaining_animals)}</td><td><strong className={statusClass(c.status)}>{pct(c.coverage_percent)}</strong></td><td><span className={`status-pill ${statusClass(c.status)}`}>{statusText(c.status)}</span></td></tr>)}</tbody></table></div></section>

    {selectedCounty && <section className="dashboard-panel units-panel"><div className="panel-heading"><div><h2>واحدهای عملیاتی · {selectedCounty.county_name}</h2><p>هر واحد قابل انتخاب است تا گزارش واحد باز شود.</p></div><span>{visibleUnits.length} واحد</span></div><div className="unit-grid">{visibleUnits.map(u => <button key={`${u.unit_code}-${u.animal_group}`} className="unit-card" onClick={() => navigate(`/gis/kpi/vaccination/unit/${encodeURIComponent(u.unit_code)}`)}><div className="unit-card-top"><b>{u.unit_name || u.unit_code}</b><span className={`status-pill ${statusClass(u.status)}`}>{statusText(u.status)}</span></div><small>{u.animal_group_name} · {u.vaccine_brand || "برند نامشخص"}</small><strong>{pct(u.coverage_percent)}</strong><div className="unit-progress"><i style={{ width: `${Math.min(100, Math.max(0, Number(u.coverage_percent || 0)))}%`, background: statusColor(u.status) }} /></div><div className="unit-meta"><span>هدف {fmt(u.target_population)}</span><span>واکسینه {fmt(u.vaccinated_animals)}</span><span>{u.last_vaccination_date || "بدون تاریخ"}</span></div></button>)}{!visibleUnits.length && <div className="empty-state">برای این شهرستان و واکسن، رکورد عملیاتی ثبت نشده است.</div>}</div></section>}

    <footer className="detail-footer"><span>پوشش معتبر: {report.dashboard.coverage_is_valid ? "بله" : "خیر"}</span><span>واکسن: {vaccineType}</span><span>گروه دام: {animalGroup || "همه"}</span></footer>
  </div>;
}
