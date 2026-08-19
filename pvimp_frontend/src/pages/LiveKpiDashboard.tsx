import React, { useEffect, useMemo, useState } from "react";
import "./LiveKpiDashboard.css";

const API = "/api/v1/gis/dashboard/kpi";

type AnyObj = Record<string, any>;

const nf = new Intl.NumberFormat(
  "fa-IR",
  { maximumFractionDigits: 1 }
);

const num = (v:any) =>
  nf.format(Number(v || 0));

const pct = (v:any) =>
  `${nf.format(Number(v || 0))}%`;


async function api(
  path:string
) {

  const response =
    await fetch(
      `${API}${path}`,
      {
        credentials:"include"
      }
    );

  if (!response.ok) {

    throw new Error(
      `${response.status} ${await response.text()}`
    );
  }

  return response.json();
}


/* =========================================================
   Charts
   ========================================================= */

function LineChart(
  {
    data,
    onClick,
    height=260,
    stroke="#19d9ff"
  }:
  {
    data:any[],
    onClick?:()=>void,
    height?:number,
    stroke?:string
  }
) {

  if (!data?.length) {

    return (
      <div className="detail-empty">
        Ø¯Ø§Ø¯Ù‡â€ŒØ§ÛŒ Ø¨Ø±Ø§ÛŒ Ø§ÛŒÙ† Ù†Ù…ÙˆØ¯Ø§Ø± ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯
      </div>
    );
  }


  const width = 760;
  const padding = 40;

  const values =
    data.map(
      x => Number(x.value || 0)
    );

  const max =
    Math.max(...values,1);


  const points =
    data.map(
      (x,i) => {

        const xx =
          padding +
          i *
          (
            (width - padding * 2) /
            Math.max(
              data.length - 1,
              1
            )
          );

        const yy =
          height -
          padding -
          (
            Number(x.value || 0) /
            max
          ) *
          (
            height -
            padding * 2
          );

        return `${xx},${yy}`;
      }
    ).join(" ");


  return (
    <div
      className="clickable-chart"
      onClick={onClick}
    >

      <svg
        viewBox={`0 0 ${width} ${height}`}
        width="100%"
        height={height}
      >

        <line
          x1={padding}
          x2={width-padding}
          y1={height-padding}
          y2={height-padding}
          stroke="#173b50"
        />

        <polyline
          points={points}
          fill="none"
          stroke={stroke}
          strokeWidth="4"
        />

        {data.map(
          (x,i) => {

            const [cx,cy] =
              points
                .split(" ")[i]
                .split(",");

            return (
              <circle
                key={i}
                cx={cx}
                cy={cy}
                r="4"
                fill={stroke}
              />
            );
          }
        )}

      </svg>

    </div>
  );
}


function BarChart(
  {
    data,
    onClick
  }:
  {
    data:any[],
    onClick?:()=>void
  }
) {

  if (!data?.length) {

    return (
      <div className="detail-empty">
        Ø¯Ø§Ø¯Ù‡â€ŒØ§ÛŒ Ø¨Ø±Ø§ÛŒ Ù†Ù…ÙˆØ¯Ø§Ø± ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯
      </div>
    );
  }


  const max =
    Math.max(
      ...data.map(
        x => Number(
          x.value ??
          x.coverage ??
          0
        )
      ),
      1
    );


  return (
    <div
      className="clickable-chart"
      onClick={onClick}
      style={{
        display:"flex",
        alignItems:"end",
        gap:10,
        minHeight:230,
        padding:"10px"
      }}
    >

      {data.slice(0,15).map(
        (x,i) => {

          const value =
            Number(
              x.value ??
              x.coverage ??
              0
            );

          const height =
            Math.max(
              6,
              value/max*170
            );

          return (
            <div
              key={i}
              style={{
                flex:1,
                textAlign:"center"
              }}
            >

              <div
                title={num(value)}
                style={{
                  height,
                  background:
                    "linear-gradient(180deg,#19d9ff,#07506b)",
                  borderRadius:
                    "5px 5px 0 0"
                }}
              />

              <div
                style={{
                  fontSize:10,
                  color:"#8caebe",
                  marginTop:5
                }}
              >
                {String(
                  x.name ??
                  x.period ??
                  ""
                ).slice(0,14)}
              </div>

            </div>
          );
        }
      )}

    </div>
  );
}


function Donut(
  {
    value,
    max,
    onClick
  }:
  {
    value:number,
    max:number,
    onClick?:()=>void
  }
) {

  const progress =
    Math.min(
      100,
      max
        ? value/max*100
        : 0
    );


  return (
    <div
      onClick={onClick}
      style={{
        height:230,
        display:"grid",
        placeItems:"center",
        cursor:onClick
          ? "pointer"
          : "default"
      }}
    >

      <div
        style={{
          width:145,
          height:145,
          borderRadius:"50%",
          background:
            `conic-gradient(
              #35e28b ${progress}%,
              #183748 0
            )`,
          display:"grid",
          placeItems:"center"
        }}
      >

        <div
          style={{
            width:98,
            height:98,
            borderRadius:"50%",
            background:"#071b2b",
            display:"grid",
            placeItems:"center",
            textAlign:"center"
          }}
        >

          <strong
            style={{
              fontSize:23
            }}
          >
            {pct(progress)}
          </strong>

          <small
            style={{
              color:"#789"
            }}
          >
            Ù¾ÙˆØ´Ø´
          </small>

        </div>

      </div>

    </div>
  );
}


/* =========================================================
   KPI Card
   ========================================================= */

function Card(
  {
    label,
    value,
    sub,
    onClick
  }:
  {
    label:string,
    value:any,
    sub?:string,
    onClick?:()=>void
  }
) {

  return (
    <div
      className="kpi-card"
      onClick={onClick}
    >

      <div className="kpi-label">
        {label}
      </div>

      <div className="kpi-value">
        {value}
      </div>

      {sub && (
        <div className="kpi-sub">
          {sub}
        </div>
      )}

    </div>
  );
}


/* =========================================================
   MAIN
   ========================================================= */

export default function LiveKpiDashboard() {

  const [
    dashboard,
    setDashboard
  ] =
    useState<AnyObj|null>(null);


  const [
    scope,
    setScope
  ] =
    useState<
      "dashboard" |
      "provinces" |
      "counties" |
      "units" |
      "unit"
    >("dashboard");


  const [
    selectedMetric,
    setSelectedMetric
  ] =
    useState("all");


  const [
    selectedProvince,
    setSelectedProvince
  ] =
    useState<AnyObj|null>(null);


  const [
    selectedCounty,
    setSelectedCounty
  ] =
    useState<AnyObj|null>(null);


  const [
    selectedUnit,
    setSelectedUnit
  ] =
    useState<AnyObj|null>(null);


  const [
    loading,
    setLoading
  ] =
    useState(true);


  const [
    error,
    setError
  ] =
    useState("");


  const loadDashboard =
    () => {

      setLoading(true);
      setError("");

      api("/overview")
        .then(setDashboard)
        .catch(
          e => setError(String(e))
        )
        .finally(
          () => setLoading(false)
        );
    };


  useEffect(
    () => {
      loadDashboard();
    },
    []
  );


  const openDrill =
    (metric:string) => {

      setSelectedMetric(metric);

      setSelectedProvince(null);
      setSelectedCounty(null);
      setSelectedUnit(null);

      setScope("provinces");
    };


  const openProvince =
    (province:AnyObj) => {

      setSelectedProvince(province);
      setSelectedCounty(null);
      setSelectedUnit(null);

      setScope("counties");
    };


  const openCounty =
    (county:AnyObj) => {

      setSelectedCounty(county);
      setSelectedUnit(null);

      setScope("units");
    };


  const openUnit =
    (unit:AnyObj) => {

      setSelectedUnit(unit);

      setScope("unit");
    };


  const goDashboard =
    () => {

      setScope("dashboard");
      setSelectedProvince(null);
      setSelectedCounty(null);
      setSelectedUnit(null);
    };


  if (
    loading &&
    !dashboard
  ) {

    return (
      <div className="live-kpi-page">
        Ø¯Ø± Ø­Ø§Ù„ Ø¯Ø±ÛŒØ§ÙØª KPIÙ‡Ø§ÛŒ Ø²Ù†Ø¯Ù‡ Ø§Ø² PostgreSQL...
      </div>
    );
  }


  if (
    error &&
    !dashboard
  ) {

    return (
      <div className="live-kpi-page">

        <div className="kpi-panel">

          <b>Ø®Ø·Ø§:</b>

          {" "}

          {error}

        </div>

      </div>
    );
  }


  if (scope !== "dashboard") {

    return (
      <DrillDown
        metric={selectedMetric}
        province={selectedProvince}
        county={selectedCounty}
        unit={selectedUnit}
        scope={scope}
        onProvince={openProvince}
        onCounty={openCounty}
        onUnit={openUnit}
        onDashboard={goDashboard}
        onBack={() => {

          if (scope === "unit") {
            setScope("units");
            setSelectedUnit(null);
            return;
          }

          if (scope === "units") {
            setScope("counties");
            return;
          }

          if (scope === "counties") {
            setScope("provinces");
            setSelectedProvince(null);
            return;
          }

          goDashboard();
        }}
      />
    );
  }


  const cards =
    dashboard?.cards || {};

  const series =
    dashboard?.series || {};

  const breakdown =
    dashboard?.breakdowns || {};


  return (
    <div className="live-kpi-page">

      {/* ==================================================
          HEADER
          ================================================== */}

      <div className="live-kpi-header">

        <div>

          <h1>
            Ø¯Ø§Ø´Ø¨ÙˆØ±Ø¯ Ø²Ù†Ø¯Ù‡ Ú©Ù†ØªØ±Ù„ Ø¨ÛŒÙ…Ø§Ø±ÛŒ Ùˆ Ø¹Ù…Ù„ÛŒØ§Øª Ø¯Ø§Ù…Ù¾Ø²Ø´Ú©ÛŒ
          </h1>

          <p>
            Ù‡Ù…Ù‡ KPIÙ‡Ø§ Ø¯Ø± ÛŒÚ© ØµÙØ­Ù‡ â€” Ú©Ù„ÛŒÚ© Ø±ÙˆÛŒ Ù‡Ø± Ú©Ø§Ø±Øª ÛŒØ§ Ù†Ù…ÙˆØ¯Ø§Ø±
            Ø¨Ø±Ø§ÛŒ Drill-down
          </p>

        </div>

        <div
          style={{
            display:"flex",
            gap:8,
            alignItems:"center"
          }}
        >

          <button
            className="refresh-button"
            onClick={loadDashboard}
          >
            â†» Ø¨Ø±ÙˆØ²Ø±Ø³Ø§Ù†ÛŒ
          </button>

          <span className="live-badge">
            â— LIVE
          </span>

        </div>

      </div>


      {/* ==================================================
          ALL KPI CARDS
          ================================================== */}

      <div className="kpi-grid">

        <Card
          label="ÙˆØ§Ø­Ø¯Ù‡Ø§ÛŒ Ø§Ù¾ÛŒØ¯Ù…ÛŒÙˆÙ„ÙˆÚ˜ÛŒÚ©"
          value={num(cards.total_units)}
          sub="Drill-down ØªØ§ ÙˆØ§Ø­Ø¯"
          onClick={() => openDrill("all")}
        />

        <Card
          label="ÙˆØ§Ø­Ø¯Ù‡Ø§ÛŒ ÙØ¹Ø§Ù„"
          value={num(cards.active_units)}
          onClick={() => openDrill("all")}
        />

        <Card
          label="Ø¬Ù…Ø¹ÛŒØª Ø¯Ø§Ù… ØªØ­Øª Ù¾ÙˆØ´Ø´"
          value={num(cards.total_livestock)}
          onClick={() => openDrill("all")}
        />

        <Card
          label="Ú¯Ø²Ø§Ø±Ø´ Ø¨ÛŒÙ…Ø§Ø±ÛŒ"
          value={num(cards.disease_reports)}
          sub="Ú¯Ø²Ø§Ø±Ø´ â†’ ÙˆØ§Ø­Ø¯"
          onClick={() => openDrill("disease_reports")}
        />

        <Card
          label="ÙˆÙ‚ÙˆØ¹ Ø¨ÛŒÙ…Ø§Ø±ÛŒ"
          value={num(cards.disease_occurrences)}
          onClick={() => openDrill("disease_reports")}
        />

        <Card
          label="Ø¨ÛŒÙ…Ø§Ø±ÛŒâ€ŒÙ‡Ø§ÛŒ Ø«Ø¨Øªâ€ŒØ´Ø¯Ù‡"
          value={num(cards.diseases)}
          onClick={() => openDrill("disease_reports")}
        />

        <Card
          label="Ø±Ú©ÙˆØ±Ø¯ Ù…Ø±Ø§Ù‚Ø¨Øª ÙØ¹Ø§Ù„"
          value={num(cards.care_records)}
          onClick={() => openDrill("care")}
        />

        <Card
          label="Ø¯Ø§Ù… Ø¨Ø±Ø±Ø³ÛŒâ€ŒØ´Ø¯Ù‡"
          value={num(cards.care_animals)}
          onClick={() => openDrill("care")}
        />

        <Card
          label="Ù…ÙˆØ§Ø±Ø¯ Ù…Ø«Ø¨Øª Ù…Ø±Ø§Ù‚Ø¨Øª"
          value={num(cards.care_positive)}
          onClick={() => openDrill("care")}
        />

        <Card
          label="Ù…ÙˆØ§Ø±Ø¯ Ù…Ù†ÙÛŒ Ù…Ø±Ø§Ù‚Ø¨Øª"
          value={num(cards.care_negative)}
          onClick={() => openDrill("care")}
        />

        <Card
          label="Ù…ÙˆØ§Ø±Ø¯ Ù…Ø´Ú©ÙˆÚ©"
          value={num(cards.care_suspicious)}
          onClick={() => openDrill("care")}
        />

        <Card
          label="Ù†Ø±Ø® Ù…Ø«Ø¨Øª Ù…Ø±Ø§Ù‚Ø¨Øª"
          value={pct(cards.care_positive_rate)}
          onClick={() => openDrill("care")}
        />

        <Card
          label="Ø¯Ø§Ù… ÙˆØ§Ø¬Ø¯ Ø´Ø±Ø§ÛŒØ· ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†"
          value={num(cards.eligible_animals)}
          onClick={() => openDrill("vaccination")}
        />

        <Card
          label="Ø¯Ø§Ù… ÙˆØ§Ú©Ø³ÛŒÙ†Ù‡â€ŒØ´Ø¯Ù‡"
          value={num(cards.vaccinated_animals)}
          onClick={() => openDrill("vaccination")}
        />

        <Card
          label="Ø¨Ø§Ù‚ÛŒâ€ŒÙ…Ø§Ù†Ø¯Ù‡ ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†"
          value={num(cards.vaccination_remaining)}
          onClick={() => openDrill("vaccination")}
        />

        <Card
          label="Ù¾ÙˆØ´Ø´ ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†"
          value={pct(cards.vaccination_coverage)}
          onClick={() => openDrill("vaccination")}
        />

        <Card
          label="Ù†ØªØ§ÛŒØ¬ Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡ÛŒ"
          value={num(cards.lab_results)}
          onClick={() => openDrill("lab")}
        />

        <Card
          label="Ù†Ù…ÙˆÙ†Ù‡ Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡"
          value={num(cards.lab_samples)}
          onClick={() => openDrill("lab")}
        />

        <Card
          label="Ù†Ù…ÙˆÙ†Ù‡ Ø§Ø±Ø³Ø§Ù„â€ŒØ´Ø¯Ù‡"
          value={num(cards.sent_samples)}
          onClick={() => openDrill("samples")}
        />

        <Card
          label="Ù†ØªØ§ÛŒØ¬ Ù…Ø«Ø¨Øª Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡"
          value={num(cards.lab_positive)}
          onClick={() => openDrill("lab")}
        />

        <Card
          label="Ù†Ø±Ø® Ù…Ø«Ø¨Øª Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡"
          value={pct(cards.lab_positive_rate)}
          onClick={() => openDrill("lab")}
        />

        <Card
          label="Ù…ÙˆØ¬ÙˆØ¯ÛŒ ÙˆØ§Ú©Ø³Ù†"
          value={num(cards.inventory_packages)}
          onClick={() => openDrill("all")}
        />

        <Card
          label="ØªÙˆØ²ÛŒØ¹ ÙˆØ§Ú©Ø³Ù†"
          value={num(cards.distributed_packages)}
          onClick={() => openDrill("all")}
        />

        <Card
          label="Ø¯ÙØ¹ ÙˆØ§Ú©Ø³Ù†"
          value={num(cards.disposed_packages)}
          onClick={() => openDrill("all")}
        />

        <Card
          label="Ù†Ø²Ø¯ÛŒÚ© Ø§Ù†Ù‚Ø¶Ø§"
          value={num(cards.expiring_30_days)}
          onClick={() => openDrill("all")}
        />

      </div>


      {/* ==================================================
          CHARTS
          ================================================== */}

      <div className="dashboard-grid">

        <div>

          <div className="kpi-panel">

            <h2>
              Ø±ÙˆÙ†Ø¯ ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†
            </h2>

            <LineChart
              data={
                series.vaccination
              }
              onClick={() =>
                openDrill("vaccination")
              }
            />

          </div>


          <div className="dashboard-grid-wide">

            <div className="kpi-panel">

              <h2>
                Ø±ÙˆÙ†Ø¯ Ú¯Ø²Ø§Ø±Ø´ Ø¨ÛŒÙ…Ø§Ø±ÛŒ
              </h2>

              <LineChart
                data={
                  series.disease_reports
                }
                stroke="#ff476b"
                onClick={() =>
                  openDrill("disease_reports")
                }
              />

            </div>


            <div className="kpi-panel">

              <h2>
                Ø±ÙˆÙ†Ø¯ Ù…ÙˆØ§Ø±Ø¯ Ù…Ø«Ø¨Øª Ù…Ø±Ø§Ù‚Ø¨Øª
              </h2>

              <LineChart
                data={
                  series.care_positive
                }
                stroke="#35e28b"
                onClick={() =>
                  openDrill("care")
                }
              />

            </div>

          </div>

        </div>


        <div>

          <div className="kpi-panel">

            <h2>
              Ù¾ÙˆØ´Ø´ ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†
            </h2>

            <Donut
              value={
                Number(
                  cards.vaccinated_animals || 0
                )
              }
              max={
                Number(
                  cards.eligible_animals || 0
                )
              }
              onClick={() =>
                openDrill("vaccination")
              }
            />

          </div>


          <div className="kpi-panel">

            <h2>
              Ø¨ÛŒÙ…Ø§Ø±ÛŒâ€ŒÙ‡Ø§ÛŒ Ù¾Ø±ØªÚ©Ø±Ø§Ø±
            </h2>

            <BarChart
              data={
                breakdown.disease
              }
              onClick={() =>
                openDrill("disease_reports")
              }
            />

          </div>

        </div>

      </div>


      <div className="dashboard-grid-wide">

        <div className="kpi-panel">

          <h2>
            Ù…Ù‚Ø§ÛŒØ³Ù‡ Ø¹Ù…Ù„Ú©Ø±Ø¯ ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†
            Ø´Ù‡Ø±Ø³ØªØ§Ù†â€ŒÙ‡Ø§
          </h2>

          <BarChart
            data={
              (breakdown.vaccination || [])
                .map((x:any) => ({
                  ...x,
                  value:
                    x.eligible
                      ? Number(x.vaccinated || 0) /
                        Number(x.eligible || 0) *
                        100
                      : 0
                }))
            }
            onClick={() =>
              openDrill("vaccination")
            }
          />

        </div>


        <div className="kpi-panel">

          <h2>
            Ø²Ù†Ø¬ÛŒØ±Ù‡ ÙˆØ§Ú©Ø³Ù†
          </h2>

          <BarChart
            data={[
              {
                name:"Ù…ÙˆØ¬ÙˆØ¯ÛŒ",
                value:
                  cards.inventory_packages
              },
              {
                name:"ØªÙˆØ²ÛŒØ¹",
                value:
                  cards.distributed_packages
              },
              {
                name:"Ø¯ÙØ¹",
                value:
                  cards.disposed_packages
              },
              {
                name:"Ø§Ù†Ù‚Ø¶Ø§ÛŒ Ù†Ø²Ø¯ÛŒÚ©",
                value:
                  cards.expiring_30_days
              }
            ]}
            onClick={() =>
              openDrill("all")
            }
          />

        </div>

      </div>

    </div>
  );
}


/* =========================================================
   DRILL DOWN
   ========================================================= */

function DrillDown(
  {
    metric,
    province,
    county,
    unit,
    scope,
    onProvince,
    onCounty,
    onUnit,
    onDashboard,
    onBack
  }:
  {
    metric:string,
    province:AnyObj|null,
    county:AnyObj|null,
    unit:AnyObj|null,
    scope:string,
    onProvince:(x:AnyObj)=>void,
    onCounty:(x:AnyObj)=>void,
    onUnit:(x:AnyObj)=>void,
    onDashboard:()=>void,
    onBack:()=>void
  }
) {

  const [
    items,
    setItems
  ] =
    useState<any[]>([]);


  const [
    loading,
    setLoading
  ] =
    useState(true);


  const [
    detail,
    setDetail
  ] =
    useState<AnyObj|null>(null);


  useEffect(
    () => {

      setLoading(true);


      if (
        scope === "unit" &&
        unit
      ) {

        api(
          `/unit/${unit.id}`
        )
          .then(setDetail)
          .finally(
            () => setLoading(false)
          );

        return;
      }


      if (
        scope === "provinces"
      ) {

        api("/provinces")
          .then(
            x => setItems(
              x.items || []
            )
          )
          .finally(
            () => setLoading(false)
          );

        return;
      }


      if (
        scope === "counties" &&
        province
      ) {

        api(
          `/counties/${province.id}`
        )
          .then(
            x => setItems(
              x.items || []
            )
          )
          .finally(
            () => setLoading(false)
          );

        return;
      }


      if (
        scope === "units" &&
        county
      ) {

        api(
          `/units/${county.id}`
        )
          .then(
            x => setItems(
              x.items || []
            )
          )
          .finally(
            () => setLoading(false)
          );

      }

    },
    [
      scope,
      province,
      county,
      unit
    ]
  );


  const metricTitle = {

    all:
      "Ø¹Ù…Ù„ÛŒØ§Øª",

    vaccination:
      "ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†",

    disease_reports:
      "Ú¯Ø²Ø§Ø±Ø´ Ø¨ÛŒÙ…Ø§Ø±ÛŒ",

    care:
      "Ù…Ø±Ø§Ù‚Ø¨Øª ÙØ¹Ø§Ù„",

    lab:
      "Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡",

    samples:
      "Ù†Ù…ÙˆÙ†Ù‡â€ŒÚ¯ÛŒØ±ÛŒ Ùˆ Ø§Ø±Ø³Ø§Ù„ Ù†Ù…ÙˆÙ†Ù‡"

  }[metric] || "KPI";


  if (
    scope === "unit" &&
    detail
  ) {

    return (
      <UnitDetail
        detail={detail}
        metric={metric}
        province={province}
        county={county}
        onBack={onBack}
        onDashboard={onDashboard}
      />
    );
  }


  return (
    <div className="live-kpi-page">

      <div className="drill-header">

        <div>

          <div className="drill-title">
            Drill-down: {metricTitle}
          </div>

          <div
            style={{
              color:"#789",
              fontSize:11,
              marginTop:5
            }}
          >
            Ø§Ø³ØªØ§Ù† â† Ø´Ù‡Ø±Ø³ØªØ§Ù† â† ÙˆØ§Ø­Ø¯
          </div>

        </div>


        <div
          style={{
            display:"flex",
            gap:7
          }}
        >

          <button
            className="back-button"
            onClick={onBack}
          >
            â† Ø¨Ø§Ø²Ú¯Ø´Øª
          </button>

          <button
            className="back-button"
            onClick={onDashboard}
          >
            Ø¯Ø§Ø´Ø¨ÙˆØ±Ø¯ Ø§ØµÙ„ÛŒ
          </button>

        </div>

      </div>


      <div className="drill-path">

        <button
          className="drill-crumb"
          onClick={onDashboard}
        >
          Ú©Ù„ Ú©Ø´ÙˆØ±
        </button>


        {province && (
          <button
            className="drill-crumb"
            onClick={() => {
              onProvince(province);
            }}
          >
            Ø§Ø³ØªØ§Ù†: {province.name}
          </button>
        )}


        {county && (
          <button
            className="drill-crumb"
          >
            Ø´Ù‡Ø±Ø³ØªØ§Ù†: {county.name}
          </button>
        )}

      </div>


      <div className="kpi-panel">

        <h2>
          {scope === "provinces"
            ? "Ø§Ø³ØªØ§Ù†â€ŒÙ‡Ø§"
            : scope === "counties"
            ? "Ø´Ù‡Ø±Ø³ØªØ§Ù†â€ŒÙ‡Ø§ÛŒ Ø§Ø³ØªØ§Ù†"
            : "ÙˆØ§Ø­Ø¯Ù‡Ø§ÛŒ Ø´Ù‡Ø±Ø³ØªØ§Ù†"}
        </h2>


        {loading ? (

          <div className="detail-empty">
            Ø¯Ø± Ø­Ø§Ù„ Ø¯Ø±ÛŒØ§ÙØª Ø§Ø·Ù„Ø§Ø¹Ø§Øª...
          </div>

        ) : !items.length ? (

          <div className="detail-empty">
            Ø±Ú©ÙˆØ±Ø¯ÛŒ Ø¨Ø±Ø§ÛŒ Ø§ÛŒÙ† Ø³Ø·Ø­ ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯
          </div>

        ) : (

          <div className="drill-list">

            {items.map(
              item => (

                <div
                  className="drill-item"
                  key={item.id}
                  onClick={() => {

                    if (
                      scope === "provinces"
                    ) {
                      onProvince(item);
                    }
                    else if (
                      scope === "counties"
                    ) {
                      onCounty(item);
                    }
                    else {
                      onUnit(item);
                    }

                  }}
                >

                  <div className="drill-item-name">
                    {item.name ||
                      `Ù…ÙˆØ±Ø¯ ${item.id}`}
                  </div>

                  <div className="drill-item-meta">
                    ID: {item.id}
                  </div>

                </div>

              )
            )}

          </div>

        )}

      </div>

    </div>
  );
}


/* =========================================================
   UNIT DETAIL
   ========================================================= */

function UnitDetail(
  {
    detail,
    metric,
    province,
    county,
    onBack,
    onDashboard
  }:
  {
    detail:AnyObj,
    metric:string,
    province:AnyObj|null,
    county:AnyObj|null,
    onBack:()=>void,
    onDashboard:()=>void
  }
) {

  const unit =
    detail.unit || {};

  const kpi =
    detail.kpi || {};

  const vaccination =
    kpi.vaccination || {};

  const care =
    kpi.care || {};

  const timeline =
    detail.timeline || [];


  return (
    <div className="live-kpi-page">

      <div className="drill-header">

        <div>

          <div className="drill-title">
            ÙˆØ§Ø­Ø¯:{" "}
            {unit.unit_name ||
              `ÙˆØ§Ø­Ø¯ ${unit.id}`}
          </div>

          <div
            style={{
              color:"#789",
              fontSize:11,
              marginTop:5
            }}
          >
            Ø¬Ø²Ø¦ÛŒØ§Øª Ú©Ø§Ù…Ù„ Ø¹Ù…Ù„ÛŒØ§Øª Ùˆ Ø³ÙˆØ§Ø¨Ù‚ Ù…Ø±ØªØ¨Ø·
          </div>

        </div>


        <div
          style={{
            display:"flex",
            gap:7
          }}
        >

          <button
            className="back-button"
            onClick={onBack}
          >
            â† Ø¨Ø§Ø²Ú¯Ø´Øª
          </button>

          <button
            className="back-button"
            onClick={onDashboard}
          >
            Ø¯Ø§Ø´Ø¨ÙˆØ±Ø¯ Ø§ØµÙ„ÛŒ
          </button>

        </div>

      </div>


      {/* ==================================================
          UNIT KPI CARDS
          ================================================== */}

      <div className="kpi-grid">

        <Card
          label="Ø¯Ø§Ù… ÙˆØ§Ø¬Ø¯ Ø´Ø±Ø§ÛŒØ·"
          value={
            num(
              vaccination.eligible
            )
          }
        />

        <Card
          label="Ø¯Ø§Ù… ÙˆØ§Ú©Ø³ÛŒÙ†Ù‡â€ŒØ´Ø¯Ù‡"
          value={
            num(
              vaccination.vaccinated
            )
          }
        />

        <Card
          label="Ø¨Ø§Ù‚ÛŒâ€ŒÙ…Ø§Ù†Ø¯Ù‡"
          value={
            num(
              vaccination.remaining
            )
          }
        />

        <Card
          label="Ù¾ÙˆØ´Ø´ ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†"
          value={
            pct(
              vaccination.coverage
            )
          }
        />

        <Card
          label="Ø±Ú©ÙˆØ±Ø¯ Ù…Ø±Ø§Ù‚Ø¨Øª"
          value={
            num(
              care.records
            )
          }
        />

        <Card
          label="Ø¯Ø§Ù… Ø¨Ø±Ø±Ø³ÛŒâ€ŒØ´Ø¯Ù‡"
          value={
            num(
              care.animals
            )
          }
        />

        <Card
          label="Ù…Ø«Ø¨Øª Ù…Ø±Ø§Ù‚Ø¨Øª"
          value={
            num(
              care.positive
            )
          }
        />

        <Card
          label="Ù…Ù†ÙÛŒ Ù…Ø±Ø§Ù‚Ø¨Øª"
          value={
            num(
              care.negative
            )
          }
        />

        <Card
          label="Ù…Ø´Ú©ÙˆÚ©"
          value={
            num(
              care.suspicious
            )
          }
        />

        <Card
          label="Ú¯Ø²Ø§Ø±Ø´ Ø¨ÛŒÙ…Ø§Ø±ÛŒ"
          value={
            num(
              kpi.disease_reports
            )
          }
        />

        <Card
          label="Ù†ØªØ§ÛŒØ¬ Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡"
          value={
            num(
              kpi.laboratory_results
            )
          }
        />

        <Card
          label="Ù†Ù…ÙˆÙ†Ù‡â€ŒÙ‡Ø§"
          value={
            num(
              kpi.samples
            )
          }
        />

        <Card
          label="Ú©Ù„ Ø¹Ù…Ù„ÛŒØ§Øª"
          value={
            num(
              kpi.operations
            )
          }
        />

      </div>


      {/* ==================================================
          UNIT PROGRESS
          ================================================== */}

      <div className="dashboard-grid">

        <div className="kpi-panel">

          <h2>
            ÙˆØ¶Ø¹ÛŒØª ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ† ÙˆØ§Ø­Ø¯
          </h2>

          <Donut
            value={
              Number(
                vaccination.vaccinated || 0
              )
            }
            max={
              Number(
                vaccination.eligible || 0
              )
            }
          />

        </div>


        <div className="kpi-panel">

          <h2>
            Ø®Ù„Ø§ØµÙ‡ Ù…Ø³ÛŒØ± Ø¹Ù…Ù„ÛŒØ§ØªÛŒ
          </h2>

          <div
            style={{
              lineHeight:2.2,
              color:"#9eb9c5",
              fontSize:12
            }}
          >

            <div>
              ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†:
              {" "}
              {num(
                vaccination.vaccinated
              )}
            </div>

            <div>
              Ù…Ø±Ø§Ù‚Ø¨Øª:
              {" "}
              {num(
                care.records
              )}
            </div>

            <div>
              Ù†Ù…ÙˆÙ†Ù‡:
              {" "}
              {num(
                kpi.samples
              )}
            </div>

            <div>
              Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡:
              {" "}
              {num(
                kpi.laboratory_results
              )}
            </div>

            <div>
              Ú¯Ø²Ø§Ø±Ø´ Ø¨ÛŒÙ…Ø§Ø±ÛŒ:
              {" "}
              {num(
                kpi.disease_reports
              )}
            </div>

          </div>

        </div>

      </div>


      {/* ==================================================
          RELATED OPERATION HISTORY
          ================================================== */}

      <div className="kpi-panel">

        <h2>
          ØªØ§Ø±ÛŒØ®Ú†Ù‡ Ú©Ø§Ù…Ù„ Ùˆ Ù…Ø±ØªØ¨Ø· Ø¹Ù…Ù„ÛŒØ§Øª ÙˆØ§Ø­Ø¯
        </h2>

        <p
          style={{
            color:"#789",
            fontSize:11,
            lineHeight:1.9
          }}
        >
          Ø±ÙˆÛŒØ¯Ø§Ø¯Ù‡Ø§ÛŒ ÙˆØ§Ù‚Ø¹ÛŒ Ø«Ø¨Øªâ€ŒØ´Ø¯Ù‡ Ø¯Ø± Ø¬Ø¯Ø§ÙˆÙ„ Ø¹Ù…Ù„ÛŒØ§ØªÛŒ
          Ø¨Ù‡ ØªØ±ØªÛŒØ¨ ØªØ§Ø±ÛŒØ® Ù†Ù…Ø§ÛŒØ´ Ø¯Ø§Ø¯Ù‡ Ù…ÛŒâ€ŒØ´ÙˆÙ†Ø¯.
          Ù‡Ø± Ø±ÙˆÛŒØ¯Ø§Ø¯ Ù…Ù†Ø¨Ø¹ØŒ ÙˆØ¶Ø¹ÛŒØªØŒ Ø¨ÛŒÙ…Ø§Ø±ÛŒ Ùˆ Ø´Ù†Ø§Ø³Ù‡ Ù†Ù…ÙˆÙ†Ù‡
          Ø±Ø§ Ø¯Ø± ØµÙˆØ±Øª ÙˆØ¬ÙˆØ¯ Ù†Ø´Ø§Ù† Ù…ÛŒâ€ŒØ¯Ù‡Ø¯.
        </p>


        {!timeline.length ? (

          <div className="detail-empty">
            Ù‡ÛŒÚ† Ø¹Ù…Ù„ÛŒØ§Øª Ø«Ø¨Øªâ€ŒØ´Ø¯Ù‡â€ŒØ§ÛŒ Ø¨Ø±Ø§ÛŒ Ø§ÛŒÙ† ÙˆØ§Ø­Ø¯ ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯.
          </div>

        ) : (

          <div className="timeline">

            {timeline.map(
              (event:any,index:number) => (

                <div
                  className="timeline-item"
                  key={
                    `${event.source_table}-${event.record_id}-${index}`
                  }
                >

                  <div className="timeline-date">
                    {String(
                      event.event_date || ""
                    ).replace("T"," ").slice(0,19)}
                  </div>


                  <div className="timeline-operation">
                    {event.operation_type}
                  </div>


                  <div
                    className="timeline-detail"
                  >

                    {event.disease_name && (
                      <span className="timeline-tag">
                        Ø¨ÛŒÙ…Ø§Ø±ÛŒ: {event.disease_name}
                      </span>
                    )}


                    {event.status && (
                      <span className="timeline-tag">
                        Ù†ØªÛŒØ¬Ù‡/ÙˆØ¶Ø¹ÛŒØª: {event.status}
                      </span>
                    )}


                    {event.reference && (
                      <span className="timeline-tag">
                        Ù†Ù…ÙˆÙ†Ù‡/Ù…Ø±Ø¬Ø¹: {event.reference}
                      </span>
                    )}


                    {event.record_id != null && (
                      <span className="timeline-tag">
                        Ø±Ú©ÙˆØ±Ø¯: {event.record_id}
                      </span>
                    )}


                    {event.details && (
                      <div
                        style={{
                          marginTop:7
                        }}
                      >
                        {event.details}
                      </div>
                    )}

                  </div>

                </div>
              )
            )}

          </div>

        )}

      </div>


      {/* ==================================================
          RAW DETAIL TABLE
          ================================================== */}

      <div className="kpi-panel">

        <h2>
          Ø¬Ø¯ÙˆÙ„ Ø¬Ø²Ø¦ÛŒØ§Øª Ø¹Ù…Ù„ÛŒØ§Øª
        </h2>

        {!timeline.length ? (

          <div className="detail-empty">
            Ø¯Ø§Ø¯Ù‡â€ŒØ§ÛŒ ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯
          </div>

        ) : (

          <div
            style={{
              overflowX:"auto"
            }}
          >

            <table className="kpi-table">

              <thead>

                <tr>

                  <th>
                    ØªØ§Ø±ÛŒØ®
                  </th>

                  <th>
                    Ø¹Ù…Ù„ÛŒØ§Øª
                  </th>

                  <th>
                    Ø¨ÛŒÙ…Ø§Ø±ÛŒ
                  </th>

                  <th>
                    Ù†ØªÛŒØ¬Ù‡ / ÙˆØ¶Ø¹ÛŒØª
                  </th>

                  <th>
                    Ù†Ù…ÙˆÙ†Ù‡ / Ù…Ø±Ø¬Ø¹
                  </th>

                  <th>
                    Ù…Ù†Ø¨Ø¹
                  </th>

                  <th>
                    Ø±Ú©ÙˆØ±Ø¯
                  </th>

                </tr>

              </thead>


              <tbody>

                {timeline.map(
                  (event:any,index:number) => (

                    <tr
                      key={index}
                    >

                      <td>
                        {String(
                          event.event_date || ""
                        )
                          .replace("T"," ")
                          .slice(0,19)}
                      </td>

                      <td>
                        {event.operation_type}
                      </td>

                      <td>
                        {event.disease_name ||
                          "â€”"}
                      </td>

                      <td>
                        {event.status ||
                          "â€”"}
                      </td>

                      <td>
                        {event.reference ||
                          "â€”"}
                      </td>

                      <td>
                        {event.source_table}
                      </td>

                      <td>
                        {event.record_id ??
                          "â€”"}
                      </td>

                    </tr>
                  )
                )}

              </tbody>

            </table>

          </div>

        )}

      </div>

    </div>
  );
}