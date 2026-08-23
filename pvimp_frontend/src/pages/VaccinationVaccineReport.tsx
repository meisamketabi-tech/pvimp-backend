import React, { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams, useSearchParams } from "react-router-dom";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import api from "../services/api";
import "./VaccinationDashboard.css";

type County = { county_code: string | number; county_name: string; units: number; target_population: number; vaccinated_animals: number; remaining_animals: number; coverage_percent: number; status: string };
type Unit = { unit_code: string; unit_name: string; county_name: string | null; animal_group: string; animal_group_name: string; target_population: number; vaccinated_animals: number; remaining_animals: number; coverage_percent: number; status: string; vaccine_brand: string | null; records: number; last_vaccination_date: string | null };
type Vaccine = { vaccine_type: string; disease_name: string | null; animal_group: string; animal_group_name: string; vaccine_brand: string | null; target_population: number; vaccinated_animals: number; remaining_animals: number; coverage_percent: number };
type Report = { dashboard: { target_population: number; vaccinated_animals: number; remaining_animals: number; coverage_percent: number; coverage_is_valid: boolean }; counties: County[]; vaccines: Vaccine[]; units: Unit[] };

function fmt(value: number) { return new Intl.NumberFormat("fa-IR").format(Number(value || 0)); }
function pct(value: number) { return `${Number(value || 0).toFixed(1)}%`; }
function color(status: string) { if (status === "NO_TARGET" || status === "NO_COVERAGE" || status === "CRITICAL") return "#dc2626"; if (status === "WARNING") return "#f59e0b"; if (status === "ON_TRACK") return "#2563eb"; return "#16a34a"; }

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
    async function load() {
      try {
        setLoading(true); setError("");
        const response = await api.get("/api/v1/gis/kpi/vaccination/management-report", {
          params: { vaccine_type: vaccineType, animal_group: animalGroup || undefined, county_code: countyCode || undefined }, signal: controller.signal,
        });
        setReport(response.data);
      } catch (err: any) {
        if (err?.code !== "ERR_CANCELED" && err?.name !== "CanceledError") setError("خطا در دریافت گزارش واکسن");
      } finally { if (!controller.signal.aborted) setLoading(false); }
    }
    load(); return () => controller.abort();
  }, [vaccineType, animalGroup, countyCode]);

  const selectedCounty = useMemo(() => report?.counties.find((c) => String(c.county_code) === countyCode) || null, [report, countyCode]);
  const visibleUnits = useMemo(() => report?.units || [], [report]);
  const chart = useMemo(() => (report?.counties || []).map((c) => ({ ...c, label: c.county_name, coverage: c.coverage_percent })), [report]);
  function selectCounty(code: string | number) { const next = new URLSearchParams(searchParams); next.set("county_code", String(code)); setSearchParams(next); }

  if (loading) return <div className="dashboard-page" dir="rtl"><div className="panel"><h2>در حال دریافت گزارش...</h2></div></div>;
  if (error || !report) return <div className="dashboard-page" dir="rtl"><div className="panel"><h2>{error || "گزارش پیدا نشد"}</h2><button onClick={() => navigate("/gis/kpi/vaccination")}>بازگشت</button></div></div>;

  const v = report.vaccines.find((x) => x.vaccine_type === vaccineType && (!animalGroup || x.animal_group === animalGroup)) || report.vaccines[0];
  const coverage = Number(v?.coverage_percent ?? report.dashboard.coverage_percent ?? 0);
  const status = coverage >= 90 ? "EXCELLENT" : coverage >= 75 ? "ON_TRACK" : coverage >= 50 ? "WARNING" : "CRITICAL";

  return (
    <div className="dashboard-page" dir="rtl">
      <div className="dashboard-header">
        <button onClick={() => navigate("/gis/kpi/vaccination")}>بازگشت به KPI واکسیناسیون</button>
        <h1>{v?.disease_name || vaccineType} — {v?.animal_group_name || animalGroup}</h1>
        <p>واکسن استاندارد: {vaccineType} | برند ثبت‌شده: {v?.vaccine_brand || "-"}</p>
      </div>

      <div className="kpi-grid">
        <div className="kpi-card"><div className="kpi-title">جمعیت هدف</div><div className="kpi-value">{fmt(v?.target_population || report.dashboard.target_population)}</div></div>
        <div className="kpi-card"><div className="kpi-title">واکسینه شده</div><div className="kpi-value">{fmt(v?.vaccinated_animals || report.dashboard.vaccinated_animals)}</div></div>
        <div className="kpi-card"><div className="kpi-title">باقی‌مانده</div><div className="kpi-value">{fmt(v?.remaining_animals || report.dashboard.remaining_animals)}</div></div>
        <div className="kpi-card"><div className="kpi-title">پوشش</div><div className="kpi-value" style={{ color: color(status) }}>{pct(coverage)}</div></div>
      </div>

      <div className="dashboard-panel" style={{ marginTop: 24 }}>
        <h2>پوشش واکسیناسیون به تفکیک شهرستان</h2>
        <div style={{ width: "100%", height: 360 }}>
          <ResponsiveContainer>
            <BarChart data={chart} margin={{ top: 20, right: 20, left: 20, bottom: 80 }}>
              <CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="label" angle={-35} textAnchor="end" interval={0} height={90} />
              <YAxis domain={[0, 100]} tickFormatter={(x) => `${x}%`} /><Tooltip formatter={(x) => pct(Number(x || 0))} />
              <Bar dataKey="coverage" name="پوشش" fill="#2563eb" onClick={(data: any) => { const row = data?.payload; if (row) selectCounty(row.county_code); }} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="dashboard-panel" style={{ marginTop: 24, overflowX: "auto" }}>
        <h2>{selectedCounty ? `واحدهای شهرستان ${selectedCounty.county_name}` : "وضعیت شهرستان‌ها"}</h2>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead><tr><th>شهرستان</th><th>واحد</th><th>جمعیت هدف</th><th>واکسینه</th><th>باقی‌مانده</th><th>پوشش</th><th>وضعیت</th></tr></thead>
          <tbody>{(report.counties || []).map((c) => <tr key={String(c.county_code)} onClick={() => selectCounty(c.county_code)} style={{ cursor: "pointer" }}><td>{c.county_name}</td><td>{fmt(c.units)}</td><td>{fmt(c.target_population)}</td><td>{fmt(c.vaccinated_animals)}</td><td>{fmt(c.remaining_animals)}</td><td>{pct(c.coverage_percent)}</td><td style={{ color: color(c.status), fontWeight: 800 }}>{c.status}</td></tr>)}</tbody>
        </table>
      </div>

      {selectedCounty && <div className="dashboard-panel" style={{ marginTop: 24, overflowX: "auto" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}><h2>واحدهای تحت پوشش/بدون پوشش — {selectedCounty.county_name}</h2><button onClick={() => { const next = new URLSearchParams(searchParams); next.delete("county_code"); setSearchParams(next); }}>بازگشت به همه شهرستان‌ها</button></div>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead><tr><th>واحد</th><th>گروه دام</th><th>هدف</th><th>واکسینه</th><th>باقی‌مانده</th><th>پوشش</th><th>آخرین عملیات</th><th>برند</th></tr></thead>
          <tbody>{visibleUnits.map((u) => <tr key={`${u.unit_code}-${u.animal_group}`} onClick={() => navigate(`/gis/kpi/vaccination/unit/${encodeURIComponent(u.unit_code)}`)} style={{ cursor: "pointer" }}><td>{u.unit_name || u.unit_code}</td><td>{u.animal_group_name}</td><td>{fmt(u.target_population)}</td><td>{fmt(u.vaccinated_animals)}</td><td>{fmt(u.remaining_animals)}</td><td style={{ color: color(u.status), fontWeight: 800 }}>{pct(u.coverage_percent)}</td><td>{u.last_vaccination_date || "-"}</td><td>{u.vaccine_brand || "-"}</td></tr>)}</tbody>
        </table>
        {!visibleUnits.length && <p>برای این شهرستان و این واکسن رکورد عملیاتی ثبت نشده است.</p>}
      </div>}
    </div>
  );
}
