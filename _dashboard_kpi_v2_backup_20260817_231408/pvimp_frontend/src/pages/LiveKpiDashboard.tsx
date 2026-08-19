import React, { useEffect, useMemo, useState } from "react";
import "./LiveKpiDashboard.css";

const API_BASE = "/api/v1/gis/dashboard/kpi";

type AnyObj = Record<string, any>;

const nf = new Intl.NumberFormat("fa-IR", {
  maximumFractionDigits: 1,
});

const pct = (v: number) => `${nf.format(Number(v || 0))}%`;
const num = (v: number) => nf.format(Number(v || 0));

function api(path: string) {
  return fetch(`${API_BASE}${path}`, {
    credentials: "include",
  }).then(async (r) => {
    if (!r.ok) {
      throw new Error(`${r.status} ${await r.text()}`);
    }

    return r.json();
  });
}

/* -------------------------------------------------------------------------- */
/*                                Line Chart                                  */
/* -------------------------------------------------------------------------- */

function LineChart({
  data,
  color = "#19d9ff",
  height = 220,
}: {
  data: any[];
  color?: string;
  height?: number;
}) {
  const w = 760;
  const h = height;
  const p = 34;

  if (!data?.length) {
    return (
      <div style={{ padding: 30, color: "#789" }}>
        داده‌ای برای نمودار وجود ندارد
      </div>
    );
  }

  const vals = data.map((x) => Number(x.value || 0));
  const max = Math.max(...vals, 1);

  const step = Math.max(
    1,
    (w - 2 * p) / Math.max(1, data.length - 1)
  );

  const points = data
    .map((x, i) => {
      const xx = p + i * step;
      const yy =
        h -
        p -
        (Number(x.value || 0) / max) * (h - 2 * p);

      return {
        x: xx,
        y: yy,
      };
    });

  const polylinePoints = points
    .map((point) => `${point.x},${point.y}`)
    .join(" ");

  return (
    <svg
      viewBox={`0 0 ${w} ${h}`}
      width="100%"
      height={height}
      preserveAspectRatio="none"
    >
      <line
        x1={p}
        x2={w - p}
        y1={h - p}
        y2={h - p}
        stroke="#173b50"
      />

      <polyline
        points={polylinePoints}
        fill="none"
        stroke={color}
        strokeWidth="4"
      />

      {points.map((point, i) => (
        <circle
          key={`point-${i}`}
          cx={point.x}
          cy={point.y}
          r="4"
          fill={color}
        />
      ))}

      {data.map((x, i) => (
        <text
          key={`label-${i}`}
          x={p + i * step}
          y={h - 10}
          fill="#7195a8"
          fontSize="11"
          textAnchor="middle"
        >
          {String(x.period || "").slice(5)}
        </text>
      ))}
    </svg>
  );
}

/* -------------------------------------------------------------------------- */
/*                                 Bar Chart                                  */
/* -------------------------------------------------------------------------- */

function BarChart({
  data,
  valueKey = "value",
  color = "#19d9ff",
}: {
  data: any[];
  valueKey?: string;
  color?: string;
}) {
  if (!data?.length) {
    return (
      <div style={{ padding: 30, color: "#789" }}>
        داده‌ای برای نمودار وجود ندارد
      </div>
    );
  }

  const max = Math.max(
    ...data.map((x) => Number(x[valueKey] || 0)),
    1
  );

  return (
    <div
      style={{
        display: "flex",
        alignItems: "end",
        gap: 10,
        height: 220,
        padding: "10px 5px 20px",
      }}
    >
      {data.slice(0, 12).map((x, i) => {
        const value = Number(x[valueKey] || 0);
        const barHeight = Math.max(
          5,
          (value / max) * 165
        );

        return (
          <div
            key={i}
            style={{
              flex: 1,
              textAlign: "center",
              minWidth: 35,
            }}
          >
            <div
              title={num(value)}
              style={{
                height: barHeight,
                background: `linear-gradient(180deg, ${color}, #07506b)`,
                borderRadius: "5px 5px 0 0",
              }}
            />

            <div
              style={{
                fontSize: 10,
                color: "#8caebe",
                marginTop: 5,
                overflow: "hidden",
              }}
            >
              {String(x.name || x.period || "").slice(0, 12)}
            </div>
          </div>
        );
      })}
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/*                                  Donut                                      */
/* -------------------------------------------------------------------------- */

function Donut({
  value,
  max,
  color = "#19d9ff",
}: {
  value: number;
  max: number;
  color?: string;
}) {
  const progress = Math.min(
    100,
    max ? (value / max) * 100 : 0
  );

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: 220,
      }}
    >
      <div
        style={{
          width: 140,
          height: 140,
          borderRadius: "50%",
          background: `conic-gradient(${color} ${progress}%, #183748 0)`,
          display: "grid",
          placeItems: "center",
        }}
      >
        <div
          style={{
            width: 96,
            height: 96,
            borderRadius: "50%",
            background: "#071b2c",
            display: "grid",
            placeItems: "center",
            textAlign: "center",
          }}
        >
          <strong style={{ fontSize: 22 }}>
            {pct(progress)}
          </strong>

          <small style={{ color: "#779" }}>
            پیشرفت
          </small>
        </div>
      </div>
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/*                                    Card                                    */
/* -------------------------------------------------------------------------- */

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
      className="kpi-card"
      onClick={onClick}
      style={onClick ? { cursor: "pointer" } : undefined}
    >
      <div className="label">{label}</div>

      <div className="value">{value}</div>

      {sub && <div className="sub">{sub}</div>}
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/*                            Main Dashboard                                   */
/* -------------------------------------------------------------------------- */

export default function LiveKpiDashboard() {
  const [data, setData] = useState<AnyObj | null>(null);
  const [tab, setTab] = useState("overview");

  const [unitId, setUnitId] = useState<number | null>(null);
  const [unit, setUnit] = useState<AnyObj | null>(null);

  const [unitMetric, setUnitMetric] = useState("all");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [refresh, setRefresh] = useState(0);

  /* ------------------------------ Overview API ----------------------------- */

  useEffect(() => {
    setLoading(true);
    setError("");

    api("/overview")
      .then(setData)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, [refresh]);

  /* ------------------------------- Unit API -------------------------------- */

  useEffect(() => {
    if (unitId == null) {
      setUnit(null);
      return;
    }

    setLoading(true);
    setError("");

    api(`/units/${unitId}`)
      .then(setUnit)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, [unitId]);

  const cards = data?.cards || {};
  const series = data?.series || {};

  const diseases =
    data?.breakdowns?.disease_by_name || [];

  const counties =
    data?.breakdowns?.vaccination_by_county || [];

  /* ------------------------------ Drill-down ------------------------------- */

  const openMetric = (metric: string) => {
    setUnitMetric(metric);
    setTab("units");
  };

  /* -------------------------------- Tabs ----------------------------------- */

  const tabs = [
    ["overview", "نمای کلی"],
    ["disease", "بیماری و اپیدمیولوژی"],
    ["care", "مراقبت فعال"],
    ["lab", "آزمایشگاه و نمونه"],
    ["vaccination", "واکسیناسیون"],
    ["inventory", "زنجیره واکسن"],
    ["units", "واحدها و جزئیات"],
  ];

  /* ------------------------------- Loading --------------------------------- */

  if (loading && !data && !unit) {
    return (
      <div className="live-kpi-page">
        در حال دریافت شاخص‌های زنده از PostgreSQL...
      </div>
    );
  }

  /* -------------------------------- Error ---------------------------------- */

  if (error && !data) {
    return (
      <div className="live-kpi-page">
        <div className="kpi-panel">
          <b>خطا:</b> {error}
        </div>
      </div>
    );
  }

  /* -------------------------------------------------------------------------- */
  /*                              Unit Dashboard                               */
  /* -------------------------------------------------------------------------- */

  if (unitId != null && unit) {
    const vaccination = unit.vaccination || {};
    const operations = unit.operation_counts || [];

    return (
      <div className="live-kpi-page">
        <span
          className="back"
          onClick={() => setUnitId(null)}
        >
          ← بازگشت به داشبورد
        </span>

        <div className="live-kpi-head">
          <div>
            <h1>
              داشبورد واحد:{" "}
              {unit.unit?.unit_name ||
                `واحد ${unitId}`}
            </h1>

            <p>
              تمام عملیات ثبت‌شده برای این واحد +
              وضعیت پیشرفت واقعی
            </p>
          </div>

          <span className="live-kpi-live">
            ● LIVE
          </span>
        </div>

        <div className="kpi-grid">
          <Card
            label="دام واجد شرایط واکسیناسیون"
            value={num(vaccination.eligible)}
          />

          <Card
            label="دام واکسینه‌شده"
            value={num(vaccination.vaccinated)}
          />

          <Card
            label="باقی‌مانده"
            value={num(vaccination.remaining)}
          />

          <Card
            label="پیشرفت واکسیناسیون"
            value={pct(
              vaccination.coverage_percent
            )}
            sub="بر اساس داده واقعی واحد"
          />

          <Card
            label="تعداد عملیات ثبت‌شده"
            value={num(
              unit.operation_history?.length || 0
            )}
          />

          <Card
            label="پیش‌بینی شهرستان"
            value={num(
              (unit.county_predictions || [])[0]
                ?.value || 0
            )}
            sub="سطح پیش‌بینی: شهرستان"
          />
        </div>

        <div className="kpi-two">
          <div className="kpi-panel">
            <h2>پیشرفت واکسیناسیون واحد</h2>

            <Donut
              value={vaccination.vaccinated || 0}
              max={vaccination.eligible || 0}
            />
          </div>

          <div className="kpi-panel">
            <h2>تعداد عملیات به تفکیک نوع</h2>

            <BarChart
              data={operations}
              color="#35e28b"
            />
          </div>
        </div>

        <div className="kpi-panel">
          <h2>تاریخچه عملیات واحد</h2>

          <table className="kpi-table">
            <thead>
              <tr>
                <th>تاریخ</th>
                <th>عملیات</th>
              </tr>
            </thead>

            <tbody>
              {(unit.operation_history || []).map(
                (item: any, index: number) => (
                  <tr key={index}>
                    <td>
                      {String(
                        item.event_date || ""
                      ).slice(0, 19)}
                    </td>

                    <td>
                      {item.operation_type}
                    </td>
                  </tr>
                )
              )}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

  /* -------------------------------------------------------------------------- */
  /*                            Main Dashboard UI                               */
  /* -------------------------------------------------------------------------- */

  return (
    <div className="live-kpi-page">
      <div className="live-kpi-head">
        <div>
          <h1>
            داشبورد زنده کنترل بیماری و عملیات دامپزشکی
          </h1>

          <p>
            تمام اعداد در هر درخواست مستقیماً از
            PostgreSQL خوانده می‌شوند.
          </p>
        </div>

        <button
          className="kpi-tab"
          onClick={() =>
            setRefresh((value) => value + 1)
          }
        >
          ↻ بروزرسانی
        </button>
      </div>

      {/* -------------------------------- Tabs -------------------------------- */}

      <div className="kpi-tabs">
        {tabs.map(([key, label]) => (
          <button
            key={key}
            className={`kpi-tab ${tab === key ? "active" : ""
              }`}
            onClick={() => setTab(key)}
          >
            {label}
          </button>
        ))}
      </div>

      {/* ---------------------------------------------------------------------- */}
      {/*                                Overview                                */}
      {/* ---------------------------------------------------------------------- */}

      {tab === "overview" && (
        <>
          <div className="kpi-grid">
            <Card
              label="واحدهای اپیدمیولوژیک"
              value={num(cards.total_units)}
              onClick={() => openMetric("all")}
            />

            <Card
              label="واحدهای فعال"
              value={num(cards.active_units)}
            />

            <Card
              label="جمعیت دام تحت پوشش"
              value={num(cards.total_livestock)}
            />

            <Card
              label="گزارش بیماری"
              value={num(cards.disease_reports)}
              onClick={() =>
                openMetric("disease_reports")
              }
            />

            <Card
              label="مراقبت فعال"
              value={num(cards.care_records)}
              onClick={() => openMetric("care")}
            />

            <Card
              label="واکسیناسیون انجام‌شده"
              value={num(cards.vaccinated_animals)}
              onClick={() =>
                openMetric("vaccination")
              }
            />

            <Card
              label="پوشش واکسیناسیون"
              value={pct(
                cards.vaccination_coverage
              )}
            />

            <Card
              label="باقی‌مانده واکسیناسیون"
              value={num(
                cards.vaccination_remaining
              )}
              onClick={() =>
                openMetric("vaccination")
              }
            />

            <Card
              label="نتایج آزمایشگاهی"
              value={num(cards.lab_results)}
              onClick={() => openMetric("lab")}
            />

            <Card
              label="نرخ مثبت آزمایشگاه"
              value={pct(cards.lab_positive_rate)}
            />

            <Card
              label="موجودی واکسن"
              value={num(cards.inventory_packages)}
            />

            <Card
              label="واکسن نزدیک انقضا"
              value={num(cards.expiring_30_days)}
            />
          </div>

          <div className="kpi-layout">
            <div>
              <div className="kpi-panel">
                <h2>روند واکسیناسیون</h2>

                <div className="chart-box">
                  <LineChart
                    data={series.vaccination}
                  />
                </div>
              </div>

              <div className="kpi-two">
                <div className="kpi-panel">
                  <h2>روند گزارش بیماری</h2>

                  <LineChart
                    data={series.disease_reports}
                    color="#ff476b"
                  />
                </div>

                <div className="kpi-panel">
                  <h2>موارد مثبت مراقبت</h2>

                  <LineChart
                    data={series.care_positive}
                    color="#35e28b"
                  />
                </div>
              </div>
            </div>

            <div>
              <div className="kpi-panel">
                <h2>پوشش واکسیناسیون</h2>

                <Donut
                  value={
                    cards.vaccinated_animals || 0
                  }
                  max={
                    cards.eligible_animals || 0
                  }
                />
              </div>

              <div className="kpi-panel">
                <h2>بیماری‌های پرتکرار</h2>

                <BarChart
                  data={diseases}
                  color="#ff476b"
                />
              </div>
            </div>
          </div>

          <div className="kpi-panel">
            <h2>
              مقایسه عملکرد واکسیناسیون شهرستان‌ها
            </h2>

            <BarChart
              data={counties.map((item: any) => ({
                ...item,
                value: item.coverage,
              }))}
              color="#f4c542"
            />
          </div>
        </>
      )}

      {/* ---------------------------------------------------------------------- */}
      {/*                                Disease                                 */}
      {/* ---------------------------------------------------------------------- */}

      {tab === "disease" && (
        <div className="kpi-layout">
          <div>
            <div className="kpi-grid">
              <Card
                label="گزارش بیماری"
                value={num(cards.disease_reports)}
                onClick={() =>
                  openMetric("disease_reports")
                }
              />

              <Card
                label="وقوع بیماری"
                value={num(
                  cards.disease_occurrences
                )}
              />

              <Card
                label="بیماری‌های ثبت‌شده"
                value={num(cards.diseases)}
              />

              <Card
                label="کانون فعال"
                value={num(
                  cards.active_outbreaks
                )}
              />
            </div>

            <div className="kpi-panel">
              <h2>روند گزارش‌های بیماری</h2>

              <LineChart
                data={series.disease_reports}
                color="#ff476b"
                height={300}
              />
            </div>
          </div>

          <div className="kpi-panel">
            <h2>توزیع بیماری‌ها</h2>

            <BarChart
              data={diseases}
              color="#ff476b"
            />
          </div>
        </div>
      )}

      {/* ---------------------------------------------------------------------- */}
      {/*                                  Care                                  */}
      {/* ---------------------------------------------------------------------- */}

      {tab === "care" && (
        <>
          <div className="kpi-grid">
            <Card
              label="رکورد مراقبت"
              value={num(cards.care_records)}
            />

            <Card
              label="دام بررسی‌شده"
              value={num(cards.care_animals)}
            />

            <Card
              label="مثبت"
              value={num(cards.care_positive)}
            />

            <Card
              label="منفی"
              value={num(cards.care_negative)}
            />

            <Card
              label="مشکوک"
              value={num(cards.care_suspicious)}
            />

            <Card
              label="نرخ مثبت"
              value={pct(
                cards.care_positive_rate
              )}
            />
          </div>

          <div className="kpi-panel">
            <h2>روند موارد مثبت مراقبت</h2>

            <LineChart
              data={series.care_positive}
              color="#35e28b"
              height={300}
            />
          </div>
        </>
      )}

      {/* ---------------------------------------------------------------------- */}
      {/*                                  Lab                                   */}
      {/* ---------------------------------------------------------------------- */}

      {tab === "lab" && (
        <>
          <div className="kpi-grid">
            <Card
              label="نتایج آزمایشگاهی"
              value={num(cards.lab_results)}
              onClick={() => openMetric("lab")}
            />

            <Card
              label="نمونه آزمایشگاه"
              value={num(cards.lab_samples)}
            />

            <Card
              label="نمونه ارسال‌شده"
              value={num(cards.sent_samples)}
            />

            <Card
              label="مثبت"
              value={num(cards.lab_positive)}
            />

            <Card
              label="نرخ مثبت"
              value={pct(
                cards.lab_positive_rate
              )}
            />
          </div>

          <div className="kpi-two">
            <div className="kpi-panel">
              <h2>وضعیت نمونه و نتیجه</h2>

              <BarChart
                data={[
                  {
                    name: "نتیجه",
                    value: cards.lab_results,
                  },
                  {
                    name: "ارسال",
                    value: cards.sent_samples,
                  },
                  {
                    name: "مثبت",
                    value: cards.lab_positive,
                  },
                ]}
                color="#19d9ff"
              />
            </div>

            <div className="kpi-panel">
              <h2>توضیح جزئیات واحدها</h2>

              <p
                style={{
                  lineHeight: 2,
                  color: "#9eb9c5",
                }}
              >
                از صفحه واحدها می‌توان تا واحد
                اپیدمیولوژیک رفت و تاریخچه عملیات
                همان واحد را مشاهده کرد.
              </p>
            </div>
          </div>
        </>
      )}

      {/* ---------------------------------------------------------------------- */}
      {/*                             Vaccination                                */}
      {/* ---------------------------------------------------------------------- */}

      {tab === "vaccination" && (
        <>
          <div className="kpi-grid">
            <Card
              label="دام واجد شرایط"
              value={num(
                cards.eligible_animals
              )}
            />

            <Card
              label="واکسینه‌شده"
              value={num(
                cards.vaccinated_animals
              )}
            />

            <Card
              label="باقی‌مانده"
              value={num(
                cards.vaccination_remaining
              )}
            />

            <Card
              label="پوشش"
              value={pct(
                cards.vaccination_coverage
              )}
            />

            <Card
              label="توزیع بسته"
              value={num(
                cards.distributed_packages
              )}
            />

            <Card
              label="دفع بسته"
              value={num(
                cards.disposed_packages
              )}
            />
          </div>

          <div className="kpi-two">
            <div className="kpi-panel">
              <h2>روند واکسیناسیون</h2>

              <LineChart
                data={series.vaccination}
                height={300}
              />
            </div>

            <div className="kpi-panel">
              <h2>پیشرفت</h2>

              <Donut
                value={
                  cards.vaccinated_animals || 0
                }
                max={
                  cards.eligible_animals || 0
                }
                color="#35e28b"
              />
            </div>
          </div>

          <div className="kpi-panel">
            <h2>مقایسه شهرستان‌ها</h2>

            <BarChart
              data={counties.map((item: any) => ({
                ...item,
                value: item.coverage,
              }))}
              color="#f4c542"
            />
          </div>
        </>
      )}

      {/* ---------------------------------------------------------------------- */}
      {/*                               Inventory                                */}
      {/* ---------------------------------------------------------------------- */}

      {tab === "inventory" && (
        <>
          <div className="kpi-grid">
            <Card
              label="موجودی بسته"
              value={num(
                cards.inventory_packages
              )}
            />

            <Card
              label="توزیع‌شده"
              value={num(
                cards.distributed_packages
              )}
            />

            <Card
              label="دفع‌شده"
              value={num(
                cards.disposed_packages
              )}
            />

            <Card
              label="نزدیک انقضا (۳۰ روز)"
              value={num(
                cards.expiring_30_days
              )}
            />
          </div>

          <div className="kpi-panel">
            <h2>جریان زنجیره واکسن</h2>

            <BarChart
              data={[
                {
                  name: "موجودی",
                  value: cards.inventory_packages,
                },
                {
                  name: "توزیع",
                  value: cards.distributed_packages,
                },
                {
                  name: "دفع",
                  value: cards.disposed_packages,
                },
                {
                  name: "انقضای نزدیک",
                  value: cards.expiring_30_days,
                },
              ]}
              color="#19d9ff"
            />
          </div>
        </>
      )}

      {/* ---------------------------------------------------------------------- */}
      {/*                                  Units                                 */}
      {/* ---------------------------------------------------------------------- */}

      {tab === "units" && (
        <UnitExplorer
          onOpen={setUnitId}
          metric={unitMetric}
        />
      )}
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/*                              Unit Explorer                                  */
/* -------------------------------------------------------------------------- */

function UnitExplorer({
  onOpen,
  metric,
}: {
  onOpen: (id: number) => void;
  metric: string;
}) {
  const [q, setQ] = useState("");
  const [rows, setRows] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    setError("");

    api(`/drilldown/${metric}`)
      .then((result) => {
        setRows(result.units || []);
      })
      .catch((e) => {
        setError(String(e));
        setRows([]);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [metric]);

  const list = useMemo(() => {
    const query = q.trim();

    return rows
      .filter(
        (item) =>
          !query ||
          String(item.unit_name || "")
            .toLowerCase()
            .includes(query.toLowerCase())
      )
      .slice(0, 1000);
  }, [rows, q]);

  const title =
    {
      all: "همه عملیات",
      vaccination: "واکسیناسیون",
      disease_reports: "گزارش بیماری",
      care: "مراقبت",
      lab: "آزمایشگاه",
      samples: "ارسال نمونه",
      spraying: "سمپاشی",
      operations: "تاریخچه عملیات",
    }[metric] || "واحدها";

  return (
    <div>
      <div className="kpi-panel">
        <h2>
          جزئیات واحدها — {title}
        </h2>

        <p
          style={{
            color: "#789",
            fontSize: 12,
            lineHeight: 1.8,
          }}
        >
          با انتخاب هر شاخص، واحدهای تشکیل‌دهنده
          همان شاخص نمایش داده می‌شوند. با انتخاب
          هر واحد نیز تاریخچه عملیات و وضعیت
          پیشرفت واقعی آن واحد نمایش داده خواهد شد.
        </p>

        <div className="unit-search">
          <input
            value={q}
            onChange={(e) =>
              setQ(e.target.value)
            }
            placeholder="جستجوی نام واحد..."
          />
        </div>

        {loading && (
          <div>
            در حال دریافت داده زنده...
          </div>
        )}

        {!loading && error && (
          <div
            style={{
              color: "#ff6b6b",
              padding: 15,
            }}
          >
            خطا در دریافت اطلاعات: {error}
          </div>
        )}

        {!loading && !error && (
          <div className="unit-list">
            {list.length === 0 ? (
              <div
                style={{
                  padding: 25,
                  color: "#789",
                  textAlign: "center",
                }}
              >
                واحدی برای نمایش پیدا نشد.
              </div>
            ) : (
              list.map((item) => (
                <div
                  className="unit-row"
                  key={item.unit_id}
                  onClick={() =>
                    onOpen(
                      Number(item.unit_id)
                    )
                  }
                >
                  <span>
                    {item.unit_name ||
                      `واحد ${item.unit_id}`}
                  </span>

                  <span>
                    {num(item.value)}

                    {metric ===
                      "vaccination" && (
                        <span
                          className={`badge ${Number(
                            item.progress_percent ||
                            0
                          ) >= 80
                              ? "good"
                              : Number(
                                item.progress_percent ||
                                0
                              ) >= 50
                                ? "warn"
                                : "bad"
                            }`}
                        >
                          {pct(
                            item.progress_percent ||
                            0
                          )}
                        </span>
                      )}
                  </span>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
}