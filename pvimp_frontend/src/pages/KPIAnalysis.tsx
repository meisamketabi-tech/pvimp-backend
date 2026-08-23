import React, { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { getToken } from "../utils/token";
import "./Dashboard.css";

type VaccineKpi = {
  vaccine_type: string;
  disease_name: string | null;
  animal_group: string;
  animal_group_name: string;
  vaccine_brand: string | null;
  units: number;
  counties: number;
  records: number;
  target_population: number;
  vaccinated_animals: number;
  remaining_animals: number;
  coverage_percent: number;
  status: string;
  adverse_events: number;
  adverse_event_rate_percent: number;
};

type Dashboard = {
  units: number;
  counties: number;
  vaccine_types: number;
  target_population: number;
  vaccinated_animals: number;
  remaining_animals: number;
  coverage_is_valid: boolean;
  coverage_note: string | null;
};

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";

function fmt(value: number) {
  return new Intl.NumberFormat("fa-IR").format(Number(value || 0));
}

function statusLabel(status: string) {
  if (status === "NO_TARGET") return "بدون جمعیت هدف";
  if (status === "NO_COVERAGE") return "بدون پوشش";
  if (status === "CRITICAL") return "بحرانی";
  if (status === "WARNING") return "نیازمند توجه";
  if (status === "ON_TRACK") return "در مسیر";
  return "عالی";
}

function statusColor(status: string) {
  if (status === "NO_TARGET" || status === "NO_COVERAGE" || status === "CRITICAL") return "#dc2626";
  if (status === "WARNING") return "#f59e0b";
  if (status === "ON_TRACK") return "#2563eb";
  return "#16a34a";
}

export default function KPIAnalysis() {
  const { type } = useParams();
  const navigate = useNavigate();
  const [vaccines, setVaccines] = useState<VaccineKpi[]>([]);
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (type && type !== "vaccination") return;
    const controller = new AbortController();
    async function load() {
      try {
        setLoading(true);
        setError("");
        const token = getToken();
        const headers = { Accept: "application/json", Authorization: `Bearer ${token}` };
        const [vaccineResponse, dashboardResponse] = await Promise.all([
          fetch(`${API_BASE}/gis/kpi/vaccination/vaccines`, { headers, signal: controller.signal }),
          fetch(`${API_BASE}/gis/kpi/vaccination/dashboard`, { headers, signal: controller.signal }),
        ]);
        if (!vaccineResponse.ok || !dashboardResponse.ok) throw new Error("HTTP_ERROR");
        setVaccines(await vaccineResponse.json());
        setDashboard(await dashboardResponse.json());
      } catch (err: any) {
        if (err?.name !== "AbortError") setError("خطا در دریافت KPI واکسیناسیون");
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }
    load();
    return () => controller.abort();
  }, [type]);

  const chartData = useMemo(() => vaccines.map((v) => ({
    key: `${v.vaccine_type}-${v.animal_group}`,
    label: `${v.vaccine_type} — ${v.animal_group_name}`,
    vaccineType: v.vaccine_type,
    animalGroup: v.animal_group,
    coverage: v.coverage_percent,
  })), [vaccines]);

  if (loading) return <div className="dashboard-page" dir="rtl"><div className="panel"><h2>در حال دریافت KPI واکسیناسیون...</h2></div></div>;
  if (error) return <div className="dashboard-page" dir="rtl"><div className="panel"><h2>{error}</h2></div></div>;

  return (
    <div className="dashboard-page" dir="rtl">
      <div className="dashboard-header">
        <h1>تحلیل KPI واکسیناسیون مبارزه با بیماری‌های دامی</h1>
        <p>منبع محاسبه: Mapping استاندارد + جمعیت واقعی واحد اپیدمیولوژیک. فیلد eligible در KPI استفاده نمی‌شود.</p>
      </div>

      <div className="kpi-grid">
        <div className="kpi-card"><div className="kpi-title">تعداد واکسن/گروه دام</div><div className="kpi-value">{fmt(vaccines.length)}</div></div>
        <div className="kpi-card"><div className="kpi-title">تعداد واحدهای درگیر</div><div className="kpi-value">{fmt(dashboard?.units || 0)}</div></div>
        <div className="kpi-card"><div className="kpi-title">شهرستان‌های درگیر</div><div className="kpi-value">{fmt(dashboard?.counties || 0)}</div></div>
        <div className="kpi-card"><div className="kpi-title">دام واکسینه شده</div><div className="kpi-value">{fmt(dashboard?.vaccinated_animals || 0)}</div></div>
      </div>

      <div className="dashboard-panel" style={{ marginTop: 24 }}>
        <h2>درصد پوشش هر واکسن به تفکیک گروه دام</h2>
        <p>برای KPI پوشش، هر ردیف مستقل است؛ پوشش چند واکسن با هم جمع نمی‌شود.</p>
        <div style={{ width: "100%", height: Math.max(360, chartData.length * 38) }}>
          <ResponsiveContainer>
            <BarChart data={chartData} layout="vertical" margin={{ top: 10, right: 20, left: 30, bottom: 10 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[0, 100]} tickFormatter={(v) => `${v}%`} />
              <YAxis type="category" dataKey="label" width={260} />
              <Tooltip formatter={(v) => `${Number(v || 0).toFixed(2)}%`} />
              <Bar dataKey="coverage" name="پوشش" fill="#2563eb" radius={[0, 6, 6, 0]} onClick={(data: any) => {
                const row = data?.payload;
                if (!row?.vaccineType) return;
                navigate(`/gis/kpi/vaccination/vaccine/${encodeURIComponent(row.vaccineType)}?animal_group=${encodeURIComponent(row.animalGroup)}`);
              }} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="dashboard-panel" style={{ marginTop: 24, overflowX: "auto" }}>
        <h2>جدول KPI رسمی واکسیناسیون</h2>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead><tr><th>بیماری</th><th>واکسن</th><th>گروه دام</th><th>جمعیت هدف</th><th>واکسینه</th><th>باقی‌مانده</th><th>پوشش</th><th>واحد</th><th>شهرستان</th></tr></thead>
          <tbody>
            {vaccines.map((v) => (
              <tr key={`${v.vaccine_type}-${v.animal_group}`} onClick={() => navigate(`/gis/kpi/vaccination/vaccine/${encodeURIComponent(v.vaccine_type)}?animal_group=${encodeURIComponent(v.animal_group)}`)} style={{ cursor: "pointer" }}>
                <td>{v.disease_name || "-"}</td>
                <td>{v.vaccine_type}</td>
                <td>{v.animal_group_name}</td>
                <td>{fmt(v.target_population)}</td>
                <td>{fmt(v.vaccinated_animals)}</td>
                <td>{fmt(v.remaining_animals)}</td>
                <td style={{ color: statusColor(v.status), fontWeight: 800 }}>{Number(v.coverage_percent || 0).toFixed(1)}% — {statusLabel(v.status)}</td>
                <td>{fmt(v.units)}</td>
                <td>{fmt(v.counties)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
