import React, { useEffect, useMemo, useState } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from "react-leaflet";
import { BarChart, Bar, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import "leaflet/dist/leaflet.css";
import "./DiseaseControlManagementDashboard.css";
import { getToken } from "../utils/token";

const API = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";

type Props = {
  title?: string;
  countyCode?: string;
  provinceCode?: string;
  compact?: boolean;
};

type DashboardData = any;

function FitPoints({ points }: { points: any[] }) {
  const map = useMap();
  useEffect(() => {
    if (!points.length) return;
    const bounds = points.map((p) => [p.lat, p.lng] as [number, number]);
    map.fitBounds(bounds, { padding: [30, 30], maxZoom: 11 });
  }, [map, points]);
  return null;
}

const n = (v: number | null | undefined) => new Intl.NumberFormat("fa-IR").format(v || 0);
const pct = (v: number | null | undefined) => `${Number(v || 0).toFixed(1)}٪`;

function Stat({ label, value, sub, tone = "normal" }: any) {
  return <div className={`dc-stat ${tone}`}><span>{label}</span><strong>{value}</strong>{sub && <small>{sub}</small>}</div>;
}

export default function DiseaseControlManagementDashboard({ title = "داشبورد مدیریت مبارزه با بیماری‌های دامی", countyCode, provinceCode, compact }: Props) {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [disease, setDisease] = useState("");
  const [animal, setAnimal] = useState("");
  const [operation, setOperation] = useState("all");
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");

  const url = useMemo(() => {
    const q = new URLSearchParams();
    if (provinceCode) q.set("province_code", provinceCode);
    if (countyCode) q.set("county_code", countyCode);
    if (disease) q.set("disease", disease);
    if (animal) q.set("animal_type", animal);
    if (start) q.set("start_date", start);
    if (end) q.set("end_date", end);
    return `${API}/gis/disease-control-dashboard/summary?${q.toString()}`;
  }, [provinceCode, countyCode, disease, animal, start, end]);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError(null);
    fetch(url, { headers: { Accept: "application/json", Authorization: `Bearer ${getToken()}` }, signal: controller.signal })
      .then(async (r) => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then(setData)
      .catch((e) => { if (e.name !== "AbortError") setError(e.message || "خطا در دریافت اطلاعات"); })
      .finally(() => setLoading(false));
    return () => controller.abort();
  }, [url]);

  const vaccines = data?.vaccination || [];
  const diseases = data?.disease || [];
  const points = (data?.map_points || []).filter((p: any) => operation === "all" || p.operation === operation);
  const filteredVaccines = operation === "disease" ? [] : vaccines;
  const filteredDiseases = operation === "vaccination" ? [] : diseases;

  const overallCoverage = useMemo(() => {
    const eligible = vaccines.reduce((a: number, x: any) => a + Number(x.eligible_animals || 0), 0);
    const vaccinated = vaccines.reduce((a: number, x: any) => a + Number(x.vaccinated_animals || 0), 0);
    return eligible ? (vaccinated / eligible) * 100 : 0;
  }, [vaccines]);

  return (
    <div className="dc-page" dir="rtl">
      <header className="dc-header">
        <div><div className="eyebrow">GIS • Disease Control • Management</div><h1>{title}</h1><p>رصد فنی عملیات، پوشش، بیماری، مراقبت، نمونه و زنجیره کنترل؛ با معماری آماده اتصال به بودجه و تحلیل اقتصادی</p></div>
        <div className="dc-header-meta"><span>سطح: {countyCode ? "شهرستان" : "استان"}</span><span>جمعیت مبنا: واحدهای اپیدمیولوژیک</span></div>
      </header>

      <section className="dc-toolbar">
        <label>از تاریخ<input type="date" value={start} onChange={e => setStart(e.target.value)} /></label>
        <label>تا تاریخ<input type="date" value={end} onChange={e => setEnd(e.target.value)} /></label>
        <label>بیماری/واکسن<input value={disease} onChange={e => setDisease(e.target.value)} placeholder="مثلاً تب برفکی" /></label>
        <label>نوع دام<input value={animal} onChange={e => setAnimal(e.target.value)} placeholder="گاو، گوسفند..." /></label>
        <label>نمایش نقشه<select value={operation} onChange={e => setOperation(e.target.value)}><option value="all">همه عملیات</option><option value="vaccination">واکسیناسیون</option><option value="disease">بیماری</option></select></label>
        <button onClick={() => { setDisease(""); setAnimal(""); setStart(""); setEnd(""); setOperation("all"); }}>پاک‌سازی فیلتر</button>
      </section>

      {loading && <div className="dc-state">در حال دریافت شاخص‌های مبارزه با بیماری‌های دامی...</div>}
      {error && <div className="dc-state error">خطا: {error}</div>}

      {!loading && !error && data && <>
        <section className="dc-kpis">
          <Stat label="جمعیت دامی مبنا" value={n(data.population?.total)} sub="بر اساس واحدهای اپیدمیولوژیک" />
          <Stat label="پوشش واکسیناسیون" value={pct(overallCoverage)} sub="مبنای محاسبه: دام واجد شرایط" tone={overallCoverage < 50 ? "critical" : overallCoverage < 70 ? "warning" : "good"} />
          <Stat label="کانون/گزارش بیماری" value={n(diseases.reduce((a: number, x: any) => a + Number(x.outbreaks || 0), 0))} sub="در بازه انتخابی" tone={diseases.length ? "warning" : "good"} />
          <Stat label="دام بررسی‌شده" value={n(data.surveillance?.animals_examined)} sub={`مثبت ${n(data.surveillance?.positive)} • مشکوک ${n(data.surveillance?.suspected)}`} />
          <Stat label="نمونه بدون نتیجه" value={n(data.samples?.without_result)} sub={`کل نمونه ${n(data.samples?.sample_count)}`} tone={data.samples?.without_result ? "warning" : "good"} />
          <Stat label="واکسن نزدیک انقضا" value={n(data.vaccine_supply?.expiring_30_days_packages)} sub="کمتر از ۳۰ روز" tone={data.vaccine_supply?.expiring_30_days_packages ? "warning" : "good"} />
        </section>

        <section className="dc-alerts">
          <div className="section-title"><h2>هشدارهای مدیریتی</h2><span>{n(data.management_alerts?.length)} مورد</span></div>
          <div className="alert-grid">
            {(data.management_alerts || []).length === 0 && <div className="empty">هشدار بحرانی یا مدیریتی ثبت نشده است.</div>}
            {(data.management_alerts || []).map((a: any, i: number) => <div className={`dc-alert ${a.level.toLowerCase()}`} key={i}><b>{a.level === "CRITICAL" ? "🔴 بحرانی" : "🟠 هشدار"}</b><span>{a.title}</span><strong>{a.value != null ? n(a.value) : ""}</strong></div>)}
          </div>
        </section>

        <section className="dc-grid">
          <div className="dc-card wide"><div className="section-title"><h2>عملیات واکسیناسیون</h2><span>Target آینده‌نگر • Actual فعلی • Coverage</span></div>
            {filteredVaccines.length ? <div className="vaccine-list">{filteredVaccines.map((x: any) => <div className="vaccine-row" key={x.vaccine}><div><b>{x.vaccine}</b><small>{n(x.eligible_animals)} دام واجد شرایط • {n(x.vaccinated_animals)} واکسینه</small></div><div className="progress"><span style={{ width: `${Math.min(Number(x.coverage_percent || 0), 100)}%` }} /></div><strong>{pct(x.coverage_percent)}</strong></div>)}</div> : <div className="empty">داده واکسیناسیون برای فیلتر فعلی وجود ندارد.</div>}
          </div>
          <div className="dc-card"><div className="section-title"><h2>جمعیت دامی</h2><span>مبنای فعلی</span></div><ResponsiveContainer width="100%" height={280}><BarChart data={Object.entries(data.population?.by_animal_type || {}).map(([animal_type, value]) => ({ animal_type, value }))}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="animal_type" /><YAxis /><Tooltip /><Bar dataKey="value" /></BarChart></ResponsiveContainer></div>
        </section>

        <section className="dc-grid">
          <div className="dc-card wide"><div className="section-title"><h2>وضعیت بیماری‌ها</h2><span>Attack Rate و Case Fatality</span></div><div className="disease-table"><div className="tr head"><span>بیماری</span><span>کانون</span><span>مبتلا</span><span>تلفات</span><span>Attack</span><span>CFR</span></div>{filteredDiseases.map((x: any) => <div className="tr" key={x.disease}><span>{x.disease}</span><span>{n(x.outbreaks)}</span><span>{n(x.infected)}</span><span>{n(x.deaths)}</span><span>{pct(x.attack_rate_percent)}</span><span>{pct(x.case_fatality_percent)}</span></div>)}</div></div>
          <div className="dc-card"><div className="section-title"><h2>مراقبت</h2><span>{n(data.surveillance?.operations)} عملیات</span></div><div className="mini-grid"><Stat label="بررسی‌شده" value={n(data.surveillance?.animals_examined)} /><Stat label="مثبت" value={n(data.surveillance?.positive)} tone="critical" /><Stat label="منفی" value={n(data.surveillance?.negative)} tone="good" /><Stat label="مشکوک" value={n(data.surveillance?.suspected)} tone="warning" /><Stat label="نرخ مثبت" value={pct(data.surveillance?.positive_rate_percent)} /></div></div>
        </section>

        <section className="dc-card map-card"><div className="section-title"><h2>پراکنش جغرافیایی عملیات</h2><span>{n(points.length)} نقطه • قابل فیلتر بر اساس عملیات و نوع دام</span></div><div className="map-wrap"><MapContainer center={[36.67, 48.49]} zoom={8} scrollWheelZoom><TileLayer attribution='&copy; OpenStreetMap contributors' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" /><FitPoints points={points} />{points.map((p: any, i: number) => <CircleMarker key={`${p.unit_code}-${p.operation}-${i}`} center={[p.lat, p.lng]} radius={7} pathOptions={{ fillOpacity: .75 }}><Popup><b>{p.unit_name || p.unit_code || "واحد اپیدمیولوژیک"}</b><br />شهرستان: {p.county_name || "-"}<br />عملیات: {p.operation === "vaccination" ? "واکسیناسیون" : "بروز بیماری"}<br />{p.vaccine && <>واکسن: {p.vaccine}<br /></>}{p.disease && <>بیماری: {p.disease}<br /></>}{p.animal_type && <>نوع دام: {p.animal_type}<br /></>}مقدار: {n(p.value)}{p.coverage_percent != null && <><br />پوشش: {pct(p.coverage_percent)}</>}</Popup></CircleMarker>)}</MapContainer></div></section>

        <section className="dc-grid">
          <div className="dc-card"><div className="section-title"><h2>نمونه و آزمایشگاه</h2><span>Sample Tracking</span></div><div className="mini-grid"><Stat label="ارسال/ثبت نمونه" value={n(data.samples?.sent_operations)} /><Stat label="بدون جواب" value={n(data.samples?.without_result)} tone={data.samples?.without_result ? "warning" : "good"} /><Stat label="نتایج آزمایشگاه" value={n(data.laboratory?.results)} /><Stat label="تعداد نمونه آزمایش‌شده" value={n(data.laboratory?.sample_count)} /></div></div>
          <div className="dc-card"><div className="section-title"><h2>اقدامات کنترلی و مبارزه با انگل</h2><span>عملیات فنی</span></div><div className="mini-grid"><Stat label="اقدام کنترلی" value={n(data.control_actions?.operations)} /><Stat label="کشتار" value={n(data.control_actions?.slaughtered)} /><Stat label="معدوم‌سازی" value={n(data.control_actions?.destroyed)} /><Stat label="مبارزه با انگل" value={n(data.parasitic_control?.animals)} sub="دام تحت عملیات" /></div></div>
        </section>

        <section className="economic-placeholder"><b>لایه اقتصادی آماده اتصال است</b><span>فعلاً هیچ عدد مالی تولید نمی‌شود. پس از اضافه شدن بودجه، هزینه عملیات، ارزش دام و خسارت پیشگیری‌شده، همین داشبورد به «هزینه به ازای دام حفاظت‌شده»، «خسارت اجتناب‌شده» و ROI تبدیل خواهد شد.</span></section>
      </>}
    </div>
  );
}
