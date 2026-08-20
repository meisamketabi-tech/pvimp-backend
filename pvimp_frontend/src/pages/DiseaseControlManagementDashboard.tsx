import React, { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from "react-leaflet";
import { Bar, BarChart, CartesianGrid, Cell, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import "leaflet/dist/leaflet.css";
import "./DiseaseControlManagementDashboard.css";
import { getToken } from "../utils/token";
import DiseaseControlAIBox from "../components/disease-control/DiseaseControlAIBox";

const API = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";
const COUNTIES = ["همه شهرستان‌ها", "زنجان", "ابهر", "خدابنده", "خرمدره", "طارم", "ماهنشان", "ایجرود", "سلطانیه"];

type Props = { title?: string; countyCode?: string; provinceCode?: string; compact?: boolean };
type DashboardData = any;

function FitPoints({ points }: { points: any[] }) {
  const map = useMap();
  useEffect(() => {
    if (!points.length) return;
    map.fitBounds(points.map((p) => [p.lat, p.lng] as [number, number]), { padding: [30, 30], maxZoom: 11 });
  }, [map, points]);
  return null;
}

const n = (v: number | null | undefined) => new Intl.NumberFormat("fa-IR").format(Number(v || 0));
const pct = (v: number | null | undefined) => v == null ? "—" : `${Number(v).toFixed(1)}٪`;
const tone = (v: number | null | undefined) => v == null ? "normal" : v < 50 ? "critical" : v < 70 ? "warning" : "good";

function Stat({ label, value, sub, variant = "normal", clickable = false, onClick }: any) {
  return <button type="button" className={`dc-stat ${variant} ${clickable ? "clickable" : ""}`} onClick={onClick} disabled={!clickable}>
    <span>{label}</span><strong>{value}</strong>{sub && <small>{sub}</small>}
  </button>;
}

export default function DiseaseControlManagementDashboard({ title = "داشبورد مدیریت مبارزه با بیماری‌های دامی", countyCode, provinceCode }: Props) {
  const navigate = useNavigate();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [county, setCounty] = useState("");
  const [disease, setDisease] = useState("");
  const [animal, setAnimal] = useState("");
  const [operation, setOperation] = useState("all");
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");

  const selectedCounty = countyCode || county || "";
  const url = useMemo(() => {
    const q = new URLSearchParams();
    if (provinceCode) q.set("province_code", provinceCode);
    if (selectedCounty) q.set("county_code", selectedCounty);
    if (disease) q.set("disease", disease);
    if (animal) q.set("animal_type", animal);
    if (start) q.set("start_date", start);
    if (end) q.set("end_date", end);
    return `${API}/gis/disease-control-dashboard/summary?${q.toString()}`;
  }, [provinceCode, selectedCounty, disease, animal, start, end]);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true); setError(null);
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
  const overview = data?.vaccination_overview || {};
  const alerts = data?.management_alerts || [];
  const targetCount = vaccines.filter((x: any) => x.target_available).length;
  const coverageChart = vaccines.map((x: any) => ({ name: x.vaccine, coverage: Number(x.coverage_percent || 0), public: Number(x.public?.vaccinated_animals || 0), private: Number(x.private?.vaccinated_animals || 0), target: x.target_available ? Number(x.target_progress_percent || 0) : null }));
  const operationChart = [{ name: "دولتی", value: Number(overview.public_vaccinated || 0) }, { name: "خصوصی", value: Number(overview.private_vaccinated || 0) }, { name: "سایر", value: Number(overview.other_vaccinated || 0) }];
  const diseaseChart = diseases.slice(0, 8).map((x: any) => ({ name: x.disease, infected: Number(x.infected || 0), outbreaks: Number(x.outbreaks || 0) }));
  const surveillanceChart = [{ name: "مثبت", value: Number(data?.surveillance?.positive || 0) }, { name: "منفی", value: Number(data?.surveillance?.negative || 0) }, { name: "مشکوک", value: Number(data?.surveillance?.suspected || 0) }];
  const monthly = (data?.vaccination_monthly || []).slice(-12).map((x: any) => ({ name: x.month, vaccinated: Number(x.vaccinated || 0), public: Number(x.public || 0), private: Number(x.private || 0) }));

  function openVaccine(row: any) {
    if (row?.vaccine) navigate(`/vaccination-vaccine-report/${encodeURIComponent(row.vaccine)}`);
  }

  return (
    <div className="dc-page" dir="rtl">
      <header className="dc-header">
        <div className="dc-title-block">
          <div className="dc-eyebrow">GIS • VET • DISEASE CONTROL</div>
          <h1>{title}</h1>
          <p>نمای مدیریتی استان از واکسیناسیون، عملکرد دولتی و خصوصی، بیماری، مراقبت، نمونه، موجودی و رخدادهای مکانی.</p>
        </div>
        <div className="dc-scope-card"><span>حوزه نمایش</span><b>{selectedCounty ? "شهرستان" : "استان زنجان"}</b><small>جمعیت مبنا: واحدهای اپیدمیولوژیک</small></div>
      </header>

      <section className="dc-toolbar">
        <label><span>شهرستان</span><select value={selectedCounty || ""} disabled={!!countyCode} onChange={(e) => setCounty(e.target.value)}><option value="">همه شهرستان‌ها</option>{COUNTIES.slice(1).map((x) => <option key={x} value={x}>{x}</option>)}</select></label>
        <label><span>از تاریخ</span><input type="date" value={start} onChange={(e) => setStart(e.target.value)} /></label>
        <label><span>تا تاریخ</span><input type="date" value={end} onChange={(e) => setEnd(e.target.value)} /></label>
        <label><span>بیماری / واکسن</span><input value={disease} onChange={(e) => setDisease(e.target.value)} placeholder="مثلاً بروسلوز" /></label>
        <label><span>نوع دام</span><input value={animal} onChange={(e) => setAnimal(e.target.value)} placeholder="گاو، گوسفند..." /></label>
        <label><span>نقشه</span><select value={operation} onChange={(e) => setOperation(e.target.value)}><option value="all">همه عملیات</option><option value="vaccination">واکسیناسیون</option><option value="disease">بیماری</option></select></label>
        <button className="dc-reset" onClick={() => { setCounty(""); setDisease(""); setAnimal(""); setStart(""); setEnd(""); setOperation("all"); }}>پاک‌سازی</button>
      </section>

      {loading && <div className="dc-state">در حال دریافت شاخص‌های مدیریتی از پایگاه داده...</div>}
      {error && <div className="dc-state error">خطا: {error}</div>}

      {!loading && !error && data && <>
        <section className="dc-kpis">
          <Stat label="کل واکسیناسیون ثبت‌شده" value={n(overview.vaccinated_animals)} sub={`دولتی ${n(overview.public_vaccinated)} • خصوصی ${n(overview.private_vaccinated)}`} variant="good" />
          <Stat label="جمعیت دامی مبنا" value={n(data.population?.total)} sub="واحدهای اپیدمیولوژیک" />
          <Stat label="واکسن‌های زیر ۵۰٪ پوشش" value={n(vaccines.filter((x: any) => x.coverage_percent != null && x.coverage_percent < 50).length)} sub="نیازمند مداخله فوری" variant="critical" />
          <Stat label="کانون / گزارش بیماری" value={n(diseases.reduce((a: number, x: any) => a + Number(x.outbreaks || 0), 0))} sub="در بازه انتخابی" variant={diseases.length ? "warning" : "good"} />
          <Stat label="نرخ مثبت مراقبت" value={pct(data.surveillance?.positive_rate_percent)} sub={`${n(data.surveillance?.positive)} مثبت از ${n(data.surveillance?.animals_examined)} بررسی`} variant={Number(data.surveillance?.positive_rate_percent || 0) > 5 ? "warning" : "good"} />
          <Stat label="نمونه بدون نتیجه" value={n(data.samples?.without_result)} sub={`${n(data.samples?.sample_count)} نمونه ثبت‌شده`} variant={data.samples?.without_result ? "warning" : "good"} />
          <Stat label="واکسن نزدیک انقضا" value={n(data.vaccine_supply?.expiring_30_days_packages)} sub="کمتر از ۳۰ روز" variant={data.vaccine_supply?.expiring_30_days_packages ? "warning" : "good"} />
          <Stat label="هدف قابل مقایسه" value={n(targetCount)} sub={targetCount ? "برنامه دارای Target" : "فعلاً Target در DB ثبت نشده"} />
        </section>

        <section className="dc-alert-strip">
          <div><span className="dc-alert-bell">🔔</span><div><b>{alerts.length ? `${alerts.length} آلارم مدیریتی فعال` : "آلارم فعال ثبت نشده"}</b><small>برای جزئیات، زنگوله بالای سامانه را باز کنید.</small></div></div>
          {alerts.slice(0, 3).map((a: any, i: number) => <div key={i} className={`dc-alert-chip ${a.level === "CRITICAL" ? "critical" : "warning"}`}><b>{a.level === "CRITICAL" ? "بحرانی" : "هشدار"}</b><span>{a.title}</span></div>)}
        </section>

        <section className="dc-grid dc-grid-main">
          <div className="dc-card wide-card">
            <div className="dc-section-head"><div><h2>پوشش واکسیناسیون به تفکیک واکسن</h2><p>برای ورود به گزارش کامل هر واکسن روی میله نمودار کلیک کنید.</p></div><span className="dc-live">LIVE FROM DB</span></div>
            <div className="dc-chart"><ResponsiveContainer width="100%" height={330}><BarChart data={coverageChart} onClick={(e: any) => e?.activePayload?.[0]?.payload && openVaccine(e.activePayload[0].payload)} margin={{ top: 12, right: 10, left: 5, bottom: 65 }}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" angle={-28} textAnchor="end" interval={0} height={80} tick={{ fontSize: 11 }} /><YAxis domain={[0, 100]} tickFormatter={(v) => `${v}%`} /><Tooltip formatter={(v: any) => [`${Number(v).toFixed(1)}%`, "پوشش"]} /><Bar dataKey="coverage" radius={[8, 8, 0, 0]} cursor="pointer">{coverageChart.map((x: any) => <Cell key={x.name} fill={x.coverage < 50 ? "#ff5d73" : x.coverage < 70 ? "#ffb84d" : "#2ec5ff"} />)}</Bar></BarChart></ResponsiveContainer></div>
          </div>
          <div className="dc-card">
            <div className="dc-section-head"><div><h2>عملکرد دولتی و خصوصی</h2><p>تعداد عملیات ثبت‌شده؛ نه Target.</p></div></div>
            <div className="dc-chart"><ResponsiveContainer width="100%" height={330}><BarChart data={operationChart} layout="vertical" margin={{ right: 10, left: 20 }}><CartesianGrid strokeDasharray="3 3" /><XAxis type="number" /><YAxis dataKey="name" type="category" /><Tooltip /><Bar dataKey="value" radius={[0, 8, 8, 0]} /></BarChart></ResponsiveContainer></div>
          </div>
        </section>

        <section className="dc-grid dc-grid-main">
          <div className="dc-card wide-card">
            <div className="dc-section-head"><div><h2>روند ماهانه واکسیناسیون</h2><p>عملکرد ثبت‌شده به تفکیک بخش دولتی و خصوصی.</p></div></div>
            <div className="dc-chart"><ResponsiveContainer width="100%" height={290}><LineChart data={monthly} margin={{ top: 10, right: 10, left: 0, bottom: 5 }}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" /><YAxis /><Tooltip /><Legend /><Line type="monotone" dataKey="public" name="دولتی" stroke="#2ec5ff" strokeWidth={3} dot={false} /><Line type="monotone" dataKey="private" name="خصوصی" stroke="#00e0a4" strokeWidth={3} dot={false} /></LineChart></ResponsiveContainer></div>
          </div>
          <div className="dc-card">
            <div className="dc-section-head"><div><h2>وضعیت مراقبت</h2><p>مثبت، منفی و مشکوک</p></div></div>
            <div className="dc-chart"><ResponsiveContainer width="100%" height={290}><BarChart data={surveillanceChart}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" /><YAxis /><Tooltip /><Bar dataKey="value" radius={[8, 8, 0, 0]} /></BarChart></ResponsiveContainer></div>
          </div>
        </section>

        <DiseaseControlAIBox />

        <section className="dc-grid dc-grid-main">
          <div className="dc-card wide-card"><div className="dc-section-head"><div><h2>بار بیماری</h2><p>کانون، مبتلا و رخداد برای تشخیص سریع فشار بیماری.</p></div></div><div className="dc-chart"><ResponsiveContainer width="100%" height={300}><BarChart data={diseaseChart} margin={{ bottom: 55 }}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" angle={-25} textAnchor="end" height={70} /><YAxis /><Tooltip /><Legend /><Bar dataKey="infected" name="مبتلا" /><Bar dataKey="outbreaks" name="کانون/رخداد" /></BarChart></ResponsiveContainer></div></div>
          <div className="dc-card"><div className="dc-section-head"><div><h2>وضعیت زنجیره واکسن</h2><p>توزیع، موجودی و انقضا</p></div></div><div className="dc-supply-grid"><Stat label="توزیع" value={n(data.vaccine_supply?.distributed_packages)} sub="بسته" /><Stat label="ردیف موجودی" value={n(data.vaccine_supply?.inventory_rows)} /><Stat label="انقضای ۳۰ روزه" value={n(data.vaccine_supply?.expiring_30_days_packages)} variant={data.vaccine_supply?.expiring_30_days_packages ? "warning" : "good"} /><Stat label="انقضای ۶۰ روزه" value={n(data.vaccine_supply?.expiring_60_days_packages)} /></div></div>
        </section>

        <section className="dc-card dc-map-card">
          <div className="dc-section-head"><div><h2>نقشه کانون‌ها و پوشش مداخله</h2><p>نقشه مشترک مدیرکل، معاون سلامت، رئیس اداره مبارزه و مدیر شهرستان؛ حوزه دسترسی از backend کنترل می‌شود.</p></div><span>{n(points.length)} نقطه</span></div>
          <div className="dc-map-wrap"><MapContainer center={[36.67, 48.49]} zoom={8} scrollWheelZoom><TileLayer attribution="&copy; OpenStreetMap contributors" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" /><FitPoints points={points} />{points.map((p: any, i: number) => <CircleMarker key={`${p.unit_code}-${p.operation}-${p.vaccine || p.disease}-${i}`} center={[p.lat, p.lng]} radius={p.operation === "disease" ? 9 : 7} pathOptions={{ color: p.operation === "disease" ? "#ff5d73" : "#2ec5ff", fillOpacity: .55 }}><Popup><div className="dc-popup"><b>{p.unit_name || p.unit_code || "واحد اپیدمیولوژیک"}</b><span>شهرستان: {p.county_name || "-"}</span><span>{p.operation === "vaccination" ? `واکسن: ${p.vaccine || "-"}` : `بیماری: ${p.disease || "-"}`}</span>{p.animal_type && <span>نوع دام: {p.animal_type}</span>}<span>مقدار: {n(p.value)}</span>{p.coverage_percent != null && <span>پوشش: {pct(p.coverage_percent)}</span>}</div></Popup></CircleMarker>)}</MapContainer></div>
        </section>

        <section className="dc-grid dc-grid-main">
          <div className="dc-card"><div className="dc-section-head"><div><h2>نمونه و آزمایشگاه</h2><p>گلوگاه‌های قابل پیگیری مدیریتی</p></div></div><div className="dc-mini-stats"><Stat label="نمونه ثبت‌شده" value={n(data.samples?.sample_count)} /><Stat label="بدون نتیجه" value={n(data.samples?.without_result)} variant={data.samples?.without_result ? "warning" : "good"} /><Stat label="نتایج آزمایشگاه" value={n(data.laboratory?.results)} /><Stat label="نمونه آزمایش‌شده" value={n(data.laboratory?.sample_count)} /></div></div>
          <div className="dc-card"><div className="dc-section-head"><div><h2>اقدامات کنترلی</h2><p>مبارزه، کشتار و معدوم‌سازی</p></div></div><div className="dc-mini-stats"><Stat label="اقدام کنترلی" value={n(data.control_actions?.operations)} /><Stat label="مثبت" value={n(data.control_actions?.positive)} variant={data.control_actions?.positive ? "critical" : "good"} /><Stat label="کشتار" value={n(data.control_actions?.slaughtered)} /><Stat label="معدوم‌سازی" value={n(data.control_actions?.destroyed)} /></div></div>
        </section>
      </>}
    </div>
  );
}
