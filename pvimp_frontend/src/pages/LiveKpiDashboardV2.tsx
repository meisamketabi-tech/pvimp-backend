import React, {
  useEffect,
  useState,
} from "react";

import "./LiveKpiDashboardV2.css";


// ======================================================
// API
// ======================================================

const API = "/api/v1/gis/dashboard/kpi-v2";


// ======================================================
// Types
// ======================================================

type AnyObj = Record<string, any>;

type Level =
  | "root"
  | "province"
  | "county"
  | "unit";


// ======================================================
// Number Formatter
// ======================================================

const nf = new Intl.NumberFormat("fa-IR", {
  maximumFractionDigits: 1,
});

function number(value: any) {
  const n = Number(value ?? 0);

  if (!Number.isFinite(n)) {
    return "۰";
  }

  return nf.format(n);
}

function percent(value: any) {
  const n = Number(value ?? 0);

  if (!Number.isFinite(n)) {
    return "۰٪";
  }

  return `${nf.format(n)}٪`;
}


// ======================================================
// API Helper
// ======================================================

async function getJson(path: string) {
  const response = await fetch(
    `${API}${path}`,
    {
      credentials: "include",
      headers: {
        Accept: "application/json",
      },
    }
  );

  if (!response.ok) {
    const text = await response.text();

    throw new Error(
      `${response.status}: ${text}`
    );
  }

  return response.json();
}


// ======================================================
// KPI Card
// ======================================================

function Card({
  label,
  value,
  sub,
  onClick,
}: {
  label: string;
  value: any;
  sub?: string;
  onClick?: () => void;
}) {
  return (
    <div
      className={`kpi-v2-card ${
        onClick ? "clickable" : ""
      }`}
      onClick={onClick}
    >
      <div className="kpi-v2-label">
        {label}
      </div>

      <div className="kpi-v2-value">
        {value}
      </div>

      {sub && (
        <div className="kpi-v2-sub">
          {sub}
        </div>
      )}
    </div>
  );
}


// ======================================================
// Empty State
// ======================================================

function EmptyState({
  children = "داده‌ای برای نمایش وجود ندارد.",
}: {
  children?: React.ReactNode;
}) {
  return (
    <div className="empty-state">
      {children}
    </div>
  );
}


// ======================================================
// Line Chart
// ======================================================

function LineChart({
  data,
}: {
  data: AnyObj[];
}) {
  if (!data?.length) {
    return (
      <EmptyState>
        داده‌ای برای نمودار وجود ندارد.
      </EmptyState>
    );
  }

  const width = 800;
  const height = 260;
  const padding = 40;

  const values = data.map(
    (item) =>
      Number(item.value ?? 0)
  );

  const max = Math.max(
    ...values,
    1
  );

  const points = data.map(
    (item, index) => {
      const x =
        padding +
        index *
          (
            (width - padding * 2) /
            Math.max(
              data.length - 1,
              1
            )
          );

      const y =
        height -
        padding -
        (
          Number(item.value ?? 0) /
          max
        ) *
          (
            height -
            padding * 2
          );

      return {
        x,
        y,
        value: item.value,
        period: item.period,
      };
    }
  );

  const polyline = points
    .map(
      (point) =>
        `${point.x},${point.y}`
    )
    .join(" ");

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      width="100%"
      height="100%"
      role="img"
      aria-label="نمودار روند"
    >
      <line
        x1={padding}
        y1={height - padding}
        x2={width - padding}
        y2={height - padding}
        stroke="#183c50"
      />

      <polyline
        points={polyline}
        fill="none"
        stroke="#1bdcff"
        strokeWidth="4"
      />

      {points.map(
        (point, index) => (
          <g key={index}>
            <circle
              cx={point.x}
              cy={point.y}
              r="5"
              fill="#1bdcff"
            />

            <text
              x={point.x}
              y={height - 10}
              fill="#789aaa"
              fontSize="10"
              textAnchor="middle"
            >
              {String(
                point.period ?? ""
              ).slice(5)}
            </text>
          </g>
        )
      )}
    </svg>
  );
}


// ======================================================
// Bar Chart
// ======================================================

function BarChart({
  data,
  onClick,
}: {
  data: AnyObj[];
  onClick?: (
    item: AnyObj
  ) => void;
}) {
  if (!data?.length) {
    return (
      <EmptyState>
        داده‌ای برای نمودار وجود ندارد.
      </EmptyState>
    );
  }

  const max = Math.max(
    ...data.map(
      (item) =>
        Number(item.value ?? 0)
    ),
    1
  );

  return (
    <div
      style={{
        display: "flex",
        alignItems: "end",
        gap: 9,
        height: 250,
        padding: "10px 5px",
      }}
    >
      {data
        .slice(0, 15)
        .map(
          (item, index) => {
            const value =
              Number(
                item.value ?? 0
              );

            const height =
              Math.max(
                5,
                (value / max) * 185
              );

            return (
              <div
                key={index}
                style={{
                  flex: 1,
                  minWidth: 30,
                  cursor: onClick
                    ? "pointer"
                    : "default",
                  textAlign: "center",
                }}
                onClick={() =>
                  onClick?.(item)
                }
              >
                <div
                  title={number(value)}
                  style={{
                    height,
                    borderRadius:
                      "5px 5px 0 0",
                    background:
                      "linear-gradient(180deg,#1bdcff,#07506b)",
                  }}
                />

                <div
                  style={{
                    color: "#8caebe",
                    fontSize: 9,
                    marginTop: 5,
                    overflow: "hidden",
                  }}
                >
                  {String(
                    item.name ??
                      item.period ??
                      ""
                  ).slice(0, 13)}
                </div>
              </div>
            );
          }
        )}
    </div>
  );
}


// ======================================================
// Breadcrumb
// ======================================================

function Breadcrumb({
  level,
  province,
  county,
  unit,
  onRoot,
  onProvince,
  onCounty,
}: {
  level: Level;
  province: AnyObj | null;
  county: AnyObj | null;
  unit: AnyObj | null;
  onRoot: () => void;
  onProvince: () => void;
  onCounty: () => void;
}) {
  return (
    <div className="kpi-v2-drill">

      <button
        type="button"
        className={`kpi-v2-crumb ${
          level === "root"
            ? "current"
            : ""
        }`}
        onClick={onRoot}
      >
        کل کشور
      </button>

      {province && (
        <>
          <span className="kpi-v2-arrow">
            ←
          </span>

          <button
            type="button"
            className={`kpi-v2-crumb ${
              level === "province"
                ? "current"
                : ""
            }`}
            onClick={onProvince}
          >
            {province.name}
          </button>
        </>
      )}

      {county && (
        <>
          <span className="kpi-v2-arrow">
            ←
          </span>

          <button
            type="button"
            className={`kpi-v2-crumb ${
              level === "county"
                ? "current"
                : ""
            }`}
            onClick={onCounty}
          >
            {county.name}
          </button>
        </>
      )}

      {unit && (
        <>
          <span className="kpi-v2-arrow">
            ←
          </span>

          <button
            type="button"
            className="kpi-v2-crumb current"
          >
            {unit.name}
          </button>
        </>
      )}

    </div>
  );
}


// ======================================================
// Unit Timeline
// ======================================================

function UnitTimeline({
  operations,
  unitId,
}: {
  operations: AnyObj[];
  unitId: number;
}) {
  const [
    selected,
    setSelected,
  ] = useState<AnyObj | null>(
    null
  );

  const [
    chain,
    setChain,
  ] = useState<AnyObj[]>([]);

  const [
    loadingChain,
    setLoadingChain,
  ] = useState(false);

  async function openOperation(
    operation: AnyObj
  ) {
    setSelected(operation);
    setChain([]);
    setLoadingChain(true);

    try {
      const result =
        await getJson(
          `/units/${unitId}/chain?operation_id=${encodeURIComponent(
            operation.source_id
          )}`
        );

      setChain(
        result?.items || []
      );
    } catch {
      setChain([]);
    } finally {
      setLoadingChain(false);
    }
  }

  return (
    <div className="kpi-v2-panel">

      <h2>
        تاریخچه و زنجیره تمام عملیات مرتبط واحد
      </h2>

      <p
        style={{
          color: "#789",
          fontSize: 11,
          lineHeight: 1.9,
        }}
      >
        هر ردیف قابل کلیک است و در صورت وجود
        کلید خارجی مشترک، زنجیره عملیات مرتبط
        نمایش داده می‌شود.
      </p>

      <div className="kpi-v2-timeline">

        {operations.length === 0 && (
          <EmptyState>
            برای این واحد هنوز عملیاتی قابل نمایش
            در جداول منبع پیدا نشد.
          </EmptyState>
        )}

        {operations.map(
          (
            operation,
            index
          ) => (
            <React.Fragment
              key={`${operation.source_id}-${index}`}
            >

              <div
                className="timeline-row"
                onClick={() =>
                  openOperation(
                    operation
                  )
                }
              >

                <div className="timeline-date">
                  {String(
                    operation.event_date ??
                      ""
                  ).slice(0, 19)}
                </div>

                <div className="timeline-type">
                  {operation.operation_type ??
                    "عملیات"}
                </div>

                <div className="timeline-detail">

                  {operation.disease_id && (
                    <span>
                      بیماری:{" "}
                      {operation.disease_id}
                      {" | "}
                    </span>
                  )}

                  {operation.sample_id && (
                    <span>
                      نمونه:{" "}
                      {operation.sample_id}
                      {" | "}
                    </span>
                  )}

                  {operation.laboratory_result_id && (
                    <span>
                      آزمایشگاه:{" "}
                      {
                        operation.laboratory_result_id
                      }
                      {" | "}
                    </span>
                  )}

                  {operation.result_status && (
                    <span>
                      نتیجه:{" "}
                      {
                        operation.result_status
                      }
                    </span>
                  )}

                </div>

              </div>

              {selected?.source_id ===
                operation.source_id && (
                <div className="timeline-chain">

                  <strong>
                    زنجیره مرتبط عملیات
                  </strong>

                  {loadingChain && (
                    <div
                      style={{
                        color: "#789",
                        marginTop: 8,
                      }}
                    >
                      در حال دریافت زنجیره مرتبط...
                    </div>
                  )}

                  {!loadingChain &&
                    chain.length === 0 && (
                      <div
                        style={{
                          color: "#789",
                          marginTop: 8,
                        }}
                      >
                        رابطه FK مشترک برای این عملیات
                        پیدا نشد یا رکورد مرتبط وجود ندارد.
                      </div>
                    )}

                  {!loadingChain &&
                    chain.map(
                      (
                        item,
                        chainIndex
                      ) => (
                        <div
                          className="chain-item"
                          key={chainIndex}
                        >

                          <div>
                            {String(
                              item.event_date ??
                                ""
                            ).slice(0, 19)}
                          </div>

                          <div>
                            {item.operation_type ??
                              "عملیات"}
                          </div>

                          <div>

                            {item.disease_id
                              ? `بیماری: ${item.disease_id}`
                              : ""}

                            {" "}

                            {item.sample_id
                              ? `نمونه: ${item.sample_id}`
                              : ""}

                            {" "}

                            {item.laboratory_result_id
                              ? `آزمایشگاه: ${item.laboratory_result_id}`
                              : ""}

                            {" "}

                            {item.result_status
                              ? `نتیجه: ${item.result_status}`
                              : ""}

                          </div>

                        </div>
                      )
                    )}

                </div>
              )}

            </React.Fragment>
          )
        )}

      </div>

    </div>
  );
}


// ======================================================
// Main Dashboard
// ======================================================

export default function LiveKpiDashboardV2() {

  const [
    data,
    setData,
  ] = useState<AnyObj | null>(
    null
  );

  const [
    metric,
    setMetric,
  ] = useState("all");

  const [
    level,
    setLevel,
  ] = useState<Level>("root");

  const [
    province,
    setProvince,
  ] = useState<AnyObj | null>(
    null
  );

  const [
    county,
    setCounty,
  ] = useState<AnyObj | null>(
    null
  );

  const [
    unit,
    setUnit,
  ] = useState<AnyObj | null>(
    null
  );

  const [
    locations,
    setLocations,
  ] = useState<AnyObj[]>([]);

  const [
    unitDetail,
    setUnitDetail,
  ] = useState<AnyObj | null>(
    null
  );

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState("");

  const [
    refresh,
    setRefresh,
  ] = useState(0);


  // ====================================================
  // Overview
  // ====================================================

  useEffect(() => {

    let cancelled = false;

    setLoading(true);
    setError("");

    getJson("/overview")
      .then((result) => {

        if (!cancelled) {
          setData(result);
        }

      })
      .catch((e) => {

        if (!cancelled) {
          setError(
            String(e?.message || e)
          );
        }

      })
      .finally(() => {

        if (!cancelled) {
          setLoading(false);
        }

      });

    return () => {
      cancelled = true;
    };

  }, [refresh]);


  // ====================================================
  // Province / County / Unit List
  // ====================================================

  useEffect(() => {

    let cancelled = false;

    if (level === "root") {
      setLocations([]);
      return;
    }

    let request = "";

    if (level === "province") {
      request =
        `/provinces?metric=${encodeURIComponent(
          metric
        )}`;
    }

    if (
      level === "county" &&
      province
    ) {
      request =
        `/provinces/${province.id}/counties?metric=${encodeURIComponent(
          metric
        )}`;
    }

    if (
      level === "unit" &&
      county
    ) {
      request =
        `/counties/${county.id}/units?metric=${encodeURIComponent(
          metric
        )}`;
    }

    if (!request) {
      setLocations([]);
      return;
    }

    setLoading(true);
    setError("");

    getJson(request)
      .then((result) => {

        if (!cancelled) {
          setLocations(
            result?.items || []
          );
        }

      })
      .catch((e) => {

        if (!cancelled) {
          setLocations([]);
          setError(
            String(e?.message || e)
          );
        }

      })
      .finally(() => {

        if (!cancelled) {
          setLoading(false);
        }

      });

    return () => {
      cancelled = true;
    };

  }, [
    level,
    province,
    county,
    metric,
  ]);


  // ====================================================
  // Unit Detail
  // ====================================================

  useEffect(() => {

    let cancelled = false;

    if (!unit) {
      setUnitDetail(null);
      return;
    }

    setLoading(true);
    setError("");

    getJson(
      `/units/${unit.id}`
    )
      .then((result) => {

        if (!cancelled) {
          setUnitDetail(result);
        }

      })
      .catch((e) => {

        if (!cancelled) {
          setUnitDetail(null);
          setError(
            String(e?.message || e)
          );
        }

      })
      .finally(() => {

        if (!cancelled) {
          setLoading(false);
        }

      });

    return () => {
      cancelled = true;
    };

  }, [unit]);


  // ====================================================
  // Data
  // ====================================================

  const cards =
    data?.cards || {};

  const charts =
    data?.charts || {};


  // ====================================================
  // Drill Metric
  // ====================================================

  function drillMetric(
    selectedMetric: string
  ) {
    setMetric(selectedMetric);

    setProvince(null);
    setCounty(null);
    setUnit(null);
    setUnitDetail(null);

    setLocations([]);

    setLevel("province");
  }


  // ====================================================
  // Root
  // ====================================================

  function root() {
    setMetric("all");

    setProvince(null);
    setCounty(null);
    setUnit(null);
    setUnitDetail(null);

    setLocations([]);

    setLevel("root");
  }


  // ====================================================
  // Open Province
  // ====================================================

  function openProvince(
    item: AnyObj
  ) {
    setProvince(item);

    setCounty(null);
    setUnit(null);
    setUnitDetail(null);

    setLocations([]);

    setLevel("county");
  }


  // ====================================================
  // Open County
  // ====================================================

  function openCounty(
    item: AnyObj
  ) {
    setCounty(item);

    setUnit(null);
    setUnitDetail(null);

    setLocations([]);

    setLevel("unit");
  }


  // ====================================================
  // Open Unit
  // ====================================================

  function openUnit(
    item: AnyObj
  ) {
    setUnit(item);
    setUnitDetail(null);

    setLevel("unit");
  }


  // ====================================================
  // Initial Loading
  // ====================================================

  if (
    loading &&
    !data
  ) {
    return (
      <div className="live-kpi-v2">
        <div className="kpi-v2-panel">
          در حال دریافت KPIهای زنده از PostgreSQL...
        </div>
      </div>
    );
  }


  // ====================================================
  // Initial Error
  // ====================================================

  if (
    error &&
    !data
  ) {
    return (
      <div className="live-kpi-v2">

        <div className="kpi-v2-panel">

          <b>خطا:</b>

          <div
            style={{
              marginTop: 10,
              direction: "ltr",
              textAlign: "left",
              whiteSpace: "pre-wrap",
            }}
          >
            {error}
          </div>

          <button
            type="button"
            className="refresh-button"
            style={{
              marginTop: 15,
            }}
            onClick={() =>
              setRefresh(
                (value) =>
                  value + 1
              )
            }
          >
            تلاش مجدد
          </button>

        </div>

      </div>
    );
  }


  // ====================================================
  // Render
  // ====================================================

  return (
    <div className="live-kpi-v2">

      {/* ============================================== */}
      {/* Header */}
      {/* ============================================== */}

      <div className="kpi-v2-header">

        <div>

          <h1>
            داشبورد زنده کنترل بیماری و عملیات دامپزشکی
          </h1>

          <p>
            تمام KPIها و نمودارها در یک صفحه؛
            کلیک روی هر KPI شما را به استان،
            شهرستان و واحد هدایت می‌کند.
          </p>

        </div>

        <div
          style={{
            display: "flex",
            gap: 8,
            alignItems: "center",
          }}
        >

          <span className="live-badge">
            ● LIVE PostgreSQL
          </span>

          <button
            type="button"
            className="refresh-button"
            onClick={() =>
              setRefresh(
                (value) =>
                  value + 1
              )
            }
          >
            ↻ بروزرسانی
          </button>

        </div>

      </div>


      {/* ============================================== */}
      {/* Error While Data Exists */}
      {/* ============================================== */}

      {error && data && (
        <div
          className="kpi-v2-panel"
          style={{
            borderColor:
              "rgba(255,85,119,.6)",
          }}
        >
          <b>خطا در دریافت اطلاعات:</b>
          <div
            style={{
              marginTop: 6,
              direction: "ltr",
              textAlign: "left",
              whiteSpace: "pre-wrap",
            }}
          >
            {error}
          </div>
        </div>
      )}


      {/* ============================================== */}
      {/* Breadcrumb */}
      {/* ============================================== */}

      {level !== "root" && (
        <Breadcrumb
          level={level}
          province={province}
          county={county}
          unit={unit}
          onRoot={root}
          onProvince={() => {

            setCounty(null);
            setUnit(null);
            setUnitDetail(null);

            setLevel(
              "county"
            );

          }}
          onCounty={() => {

            setUnit(null);
            setUnitDetail(null);

            setLevel(
              "unit"
            );

          }}
        />
      )}


      {/* ============================================== */}
      {/* ROOT DASHBOARD */}
      {/* ============================================== */}

      {level === "root" && (
        <>

          {/* KPI Cards */}

          <div className="kpi-v2-grid">

            <Card
              label="واحدهای اپیدمیولوژیک"
              value={number(
                cards.total_units
              )}
              onClick={() =>
                drillMetric("units")
              }
            />

            <Card
              label="واحدهای فعال"
              value={number(
                cards.active_units
              )}
              onClick={() =>
                drillMetric("units")
              }
            />

            <Card
              label="گزارش بیماری"
              value={number(
                cards.disease_reports
              )}
              onClick={() =>
                drillMetric("disease")
              }
            />

            <Card
              label="وقوع بیماری"
              value={number(
                cards.disease_occurrences
              )}
              onClick={() =>
                drillMetric("disease")
              }
            />

            <Card
              label="مراقبت فعال"
              value={number(
                cards.care_records
              )}
              onClick={() =>
                drillMetric("care")
              }
            />

            <Card
              label="واکسیناسیون انجام‌شده"
              value={number(
                cards.vaccinated
              )}
              sub="برای Drill-down کلیک کنید"
              onClick={() =>
                drillMetric(
                  "vaccination"
                )
              }
            />

            <Card
              label="دام واجد شرایط"
              value={number(
                cards.eligible
              )}
              onClick={() =>
                drillMetric(
                  "vaccination"
                )
              }
            />

            <Card
              label="پوشش واکسیناسیون"
              value={percent(
                cards.vaccination_coverage
              )}
              onClick={() =>
                drillMetric(
                  "vaccination"
                )
              }
            />

            <Card
              label="باقی‌مانده واکسیناسیون"
              value={number(
                cards.vaccination_remaining
              )}
              onClick={() =>
                drillMetric(
                  "vaccination"
                )
              }
            />

            <Card
              label="نتایج آزمایشگاهی"
              value={number(
                cards.lab_results
              )}
              onClick={() =>
                drillMetric("lab")
              }
            />

            <Card
              label="مثبت آزمایشگاهی"
              value={number(
                cards.lab_positive
              )}
              onClick={() =>
                drillMetric("lab")
              }
            />

            <Card
              label="نرخ مثبت آزمایشگاه"
              value={percent(
                cards.lab_positive_rate
              )}
              onClick={() =>
                drillMetric("lab")
              }
            />

            <Card
              label="نمونه‌ها"
              value={number(
                cards.sample_records
              )}
              onClick={() =>
                drillMetric("samples")
              }
            />

            <Card
              label="موجودی واکسن"
              value={number(
                cards.inventory
              )}
            />

            <Card
              label="توزیع واکسن"
              value={number(
                cards.distributed
              )}
            />

            <Card
              label="دفع واکسن"
              value={number(
                cards.disposed
              )}
            />

          </div>


          {/* Charts */}

          <div className="kpi-v2-layout">

            <div>

              <div className="kpi-v2-panel">

                <h2>
                  روند واکسیناسیون
                </h2>

                <div className="kpi-v2-chart">

                  <LineChart
                    data={
                      charts.vaccination ||
                      []
                    }
                  />

                </div>

              </div>


              <div className="kpi-v2-panel">

                <h2>
                  روند گزارش بیماری
                </h2>

                <div className="kpi-v2-chart">

                  <LineChart
                    data={
                      charts.disease ||
                      []
                    }
                  />

                </div>

              </div>

            </div>


            <div>

              <div className="kpi-v2-panel">

                <h2>
                  روند مراقبت
                </h2>

                <div className="kpi-v2-chart">

                  <LineChart
                    data={
                      charts.care ||
                      []
                    }
                  />

                </div>

              </div>


              <div className="kpi-v2-panel">

                <h2>
                  روند آزمایشگاه
                </h2>

                <div className="kpi-v2-chart">

                  <LineChart
                    data={
                      charts.laboratory ||
                      []
                    }
                  />

                </div>

              </div>

            </div>

          </div>

        </>
      )}


      {/* ============================================== */}
      {/* PROVINCE / COUNTY */}
      {/* ============================================== */}

      {level !== "root" &&
        level !== "unit" && (

          <div className="kpi-v2-panel">

            <h2>

              {level === "province"
                ? `استان‌ها — شاخص: ${metric}`
                : `شهرستان‌ها — شاخص: ${metric}`}

            </h2>

            {loading ? (
              <EmptyState>
                در حال دریافت اطلاعات...
              </EmptyState>
            ) : locations.length === 0 ? (
              <EmptyState>
                رکوردی برای نمایش پیدا نشد.
              </EmptyState>
            ) : (
              <div className="kpi-v2-list">

                {locations.map(
                  (item) => (

                    <div
                      className="kpi-v2-location"
                      key={item.id}
                      onClick={() => {

                        if (
                          level ===
                          "province"
                        ) {
                          openProvince(
                            item
                          );
                        } else {
                          openCounty(
                            item
                          );
                        }

                      }}
                    >

                      <div className="kpi-v2-location-title">
                        {item.name}
                      </div>

                      <div className="kpi-v2-location-value">
                        {number(
                          item.value
                        )}
                      </div>

                    </div>

                  )
                )}

              </div>
            )}

          </div>

        )}


      {/* ============================================== */}
      {/* UNITS */}
      {/* ============================================== */}

      {level === "unit" &&
        !unit && (

          <div className="kpi-v2-panel">

            <h2>
              واحدهای اپیدمیولوژیک
            </h2>

            {loading ? (

              <EmptyState>
                در حال دریافت واحدها...
              </EmptyState>

            ) : locations.length === 0 ? (

              <EmptyState>
                هیچ واحدی برای این شهرستان پیدا نشد.
              </EmptyState>

            ) : (

              <div className="kpi-v2-list">

                {locations.map(
                  (item) => (

                    <div
                      className="kpi-v2-location"
                      key={item.id}
                      onClick={() =>
                        openUnit(item)
                      }
                    >

                      <div className="kpi-v2-location-title">
                        {item.name}
                      </div>

                      <div className="kpi-v2-location-value">
                        {number(
                          item.value
                        )}
                      </div>

                      <div
                        style={{
                          color: "#789",
                          fontSize: 10,
                          marginTop: 5,
                        }}
                      >
                        مشاهده جزئیات کامل واحد →
                      </div>

                    </div>

                  )
                )}

              </div>

            )}

          </div>

        )}


      {/* ============================================== */}
      {/* UNIT DETAIL */}
      {/* ============================================== */}

      {unit &&
        unitDetail && (

          <>

            <div className="kpi-v2-panel">

              <div className="kpi-v2-unit-header">

                <div>

                  <h2>
                    واحد: {unit.name}
                  </h2>

                  <div
                    style={{
                      color: "#789",
                      fontSize: 11,
                      marginTop: 6,
                    }}
                  >
                    جزئیات کامل عملیات واقعی ثبت‌شده
                    برای این واحد
                  </div>

                </div>

              </div>

            </div>


            <div className="kpi-v2-grid">

              <Card
                label="تمام عملیات"
                value={number(
                  unitDetail.cards?.all
                )}
              />

              <Card
                label="بیماری"
                value={number(
                  unitDetail.cards?.disease
                )}
              />

              <Card
                label="مراقبت"
                value={number(
                  unitDetail.cards?.care
                )}
              />

              <Card
                label="واکسیناسیون"
                value={number(
                  unitDetail.cards?.vaccination
                )}
              />

              <Card
                label="آزمایشگاه"
                value={number(
                  unitDetail.cards?.lab
                )}
              />

              <Card
                label="نمونه"
                value={number(
                  unitDetail.cards?.samples
                )}
              />

              <Card
                label="سمپاشی"
                value={number(
                  unitDetail.cards?.spraying
                )}
              />

              <Card
                label="امحاء"
                value={number(
                  unitDetail.cards?.slaughter
                )}
              />

            </div>


            <UnitTimeline
              operations={
                unitDetail.operations ||
                []
              }
              unitId={
                Number(unit.id)
              }
            />

          </>
        )}


      {/* ============================================== */}
      {/* UNIT DETAIL LOADING */}
      {/* ============================================== */}

      {unit &&
        !unitDetail &&
        loading && (

          <div className="kpi-v2-panel">

            <EmptyState>
              در حال دریافت جزئیات واحد...
            </EmptyState>

          </div>

        )}

    </div>
  );
}