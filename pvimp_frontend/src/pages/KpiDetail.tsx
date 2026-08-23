import React, { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../services/api";
import "../styles/index.css";

type HistoryResponse = { unit: Record<string, any>; unit_code: string; unit_name: string | null; history: any[]; sections: Record<string, any[]>; summary: Record<string, number> };
type KpiResponse = { vaccinated_animals: number; target_population: number; coverage_percent: number; disease_records: number; affected_units: number; infected_count: number; dead_count: number; adverse_events: number };
const fmt = (v: any) => new Intl.NumberFormat("fa-IR").format(Number(v || 0));
const display = (v: any) => v === null || v === undefined || v === "" ? "-" : String(v).replaceAll("-", "/");
function Table({ rows, columns }: { rows: any[]; columns: [string, string][] }) { return <div style={{ overflowX: "auto" }}><table style={{ width: "100%", borderCollapse: "collapse" }}><thead><tr>{columns.map(([key, label]) => <th key={key}>{label}</th>)}</tr></thead><tbody>{rows.map((row, i) => <tr key={i}>{columns.map(([key]) => <td key={key}>{display(row[key])}</td>)}</tr>)}</tbody></table></div>; }

export default function KpiDetail() {
  const { unitCode = "" } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState<HistoryResponse | null>(null);
  const [kpi, setKpi] = useState<KpiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  useEffect(() => {
    if (!unitCode) return;
    const controller = new AbortController();
    async function load() {
      try {
        setLoading(true); setError("");
        const [historyResponse, kpiResponse] = await Promise.all([
          api.get(`/api/v1/gis/kpi/vaccination/unit/${encodeURIComponent(unitCode)}/history`, { signal: controller.signal }),
          api.get(`/api/v1/gis/kpi/vaccination/effectiveness`, { params: { unit_code: unitCode }, signal: controller.signal }),
        ]);
        setData(historyResponse.data); setKpi(kpiResponse.data);
      } catch (err: any) {
        if (err?.code !== "ERR_CANCELED" && err?.name !== "CanceledError") setError("خطا در دریافت پرونده واحد اپیدمیولوژیک");
      } finally { if (!controller.signal.aborted) setLoading(false); }
    }
    load(); return () => controller.abort();
  }, [unitCode]);
  const summary = useMemo(() => data?.summary || {}, [data]);
  if (loading) return <div className="dashboard-page" dir="rtl"><div className="panel"><h2>در حال دریافت پرونده واحد...</h2></div></div>;
  if (error || !data) return <div className="dashboard-page" dir="rtl"><div className="panel"><h2>{error || "واحد پیدا نشد"}</h2></div></div>;
  const u = data.unit || {};
  return <div className="dashboard-page" dir="rtl">
    <div className="dashboard-header"><button onClick={() => navigate(-1)}>بازگشت</button><h1>{data.unit_name || unitCode}</h1><p>پرونده 360 درجه واحد اپیدمیولوژیک — {unitCode}</p></div>
    <div className="kpi-grid">
      <div className="kpi-card"><div className="kpi-title">پوشش واکسیناسیون</div><div className="kpi-value">{Number(kpi?.coverage_percent || 0).toFixed(1)}%</div></div>
      <div className="kpi-card"><div className="kpi-title">دام هدف</div><div className="kpi-value">{fmt(kpi?.target_population)}</div></div>
      <div className="kpi-card"><div className="kpi-title">واکسینه شده</div><div className="kpi-value">{fmt(kpi?.vaccinated_animals)}</div></div>
      <div className="kpi-card"><div className="kpi-title">رخداد بیماری</div><div className="kpi-value">{fmt(kpi?.disease_records)}</div></div>
      <div className="kpi-card"><div className="kpi-title">مبتلا</div><div className="kpi-value">{fmt(kpi?.infected_count)}</div></div>
      <div className="kpi-card"><div className="kpi-title">تلفات</div><div className="kpi-value">{fmt(kpi?.dead_count)}</div></div>
      <div className="kpi-card"><div className="kpi-title">مراقبت</div><div className="kpi-value">{fmt(summary.surveillance_operations)}</div></div>
      <div className="kpi-card"><div className="kpi-title">نمونه آزمایشگاهی</div><div className="kpi-value">{fmt(summary.samples)}</div></div>
    </div>
    <div className="dashboard-panel" style={{ marginTop: 24 }}><h2>مشخصات واحد</h2><Table rows={[u]} columns={[["unit_code", "کد واحد"],["province_name", "استان"],["county_name", "شهرستان"],["license_type", "نوع مجوز"],["address", "آدرس"]]} /></div>
    <div className="dashboard-panel" style={{ marginTop: 24 }}><h2>تمام عملیات واکسیناسیون</h2><Table rows={data.sections.vaccination || []} columns={[["vaccination_date", "تاریخ"],["disease_name", "بیماری"],["vaccine_type", "واکسن"],["vaccine_brand", "برند"],["manufacturer", "تولیدکننده"],["batch_number", "بچ"],["animal_type", "نوع دام"],["vaccinated_animals", "واکسینه"],["operation_type", "بخش/عملیات"]]} /></div>
    <div className="dashboard-panel" style={{ marginTop: 24 }}><h2>پایش و مراقبت</h2><Table rows={data.sections.surveillance || []} columns={[["care_date", "تاریخ"],["care_type", "نوع مراقبت"],["animal_type", "نوع دام"],["total_animals", "کل دام"],["positive_count", "مثبت"],["negative_count", "منفی"],["suspicious_count", "مشکوک"]]} /></div>
    <div className="dashboard-panel" style={{ marginTop: 24 }}><h2>ارسال نمونه</h2><Table rows={data.sections.samples || []} columns={[["sampling_date", "تاریخ"],["disease_name", "بیماری"],["sample_type", "نوع نمونه"],["sample_count", "تعداد"],["result_status", "وضعیت نتیجه"]]} /></div>
    <div className="dashboard-panel" style={{ marginTop: 24 }}><h2>نتایج آزمایشگاه</h2><Table rows={data.sections.laboratory_results || []} columns={[["answer_date", "تاریخ جواب"],["sampling_date", "تاریخ نمونه"],["disease_name", "بیماری"],["laboratory_name", "آزمایشگاه"],["result_status", "نتیجه"],["isolate_name_1", "عامل ۱"],["isolate_name_2", "عامل ۲"],["serotype_a", "A"],["serotype_o", "O"],["serotype_asia1", "Asia1"]]} /></div>
    <div className="dashboard-panel" style={{ marginTop: 24 }}><h2>بروز بیماری</h2><Table rows={data.sections.disease_occurrences || []} columns={[["start_date", "تاریخ شروع"],["disease_name", "بیماری"],["animal_type", "نوع دام"],["total_animals", "کل"],["infected_count", "مبتلا"],["dead_count", "تلفات"],["slaughtered_count", "کشتار"],["status", "وضعیت"]]} /></div>
    <div className="dashboard-panel" style={{ marginTop: 24 }}><h2>گزارش بیماری</h2><Table rows={data.sections.disease_reports || []} columns={[["disease_start_date", "تاریخ"],["disease_name", "بیماری"],["animal_type", "نوع دام"],["total_animals", "کل"],["infected_count", "مبتلا"],["death_count", "تلفات"],["slaughtered_count", "کشتار"],["destroyed_count", "معدوم"]]} /></div>
    <div className="dashboard-panel" style={{ marginTop: 24 }}><h2>مبارزه با انگل / سمپاشی</h2><Table rows={data.sections.spraying || []} columns={[["spraying_date", "تاریخ"],["plan_type", "طرح"],["operation_type", "عملیات"],["poison_type", "سم"],["animal_type", "نوع دام"],["sprayed_animal_count", "دام تحت عملیات"],["sprayed_area", "مساحت"]]} /></div>
  </div>;
}
