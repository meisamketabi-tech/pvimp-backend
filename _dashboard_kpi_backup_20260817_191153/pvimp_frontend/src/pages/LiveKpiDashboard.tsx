import React, { useEffect, useMemo, useState } from "react";
import "./LiveKpiDashboard.css";

type DashboardData = {
  cards?: Record<string, number>;
  series?: {
    vaccination?: Array<{ period: string; value: number }>;
    disease_reports?: Array<{ period: string; value: number }>;
    care_positive?: Array<{ period: string; value: number }>;
  };
  breakdowns?: {
    disease_by_name?: Array<{ name: string; value: number }>;
    vaccination_by_county?: Array<{
      name: string;
      coverage: number;
      value?: number;
    }>;
  };
};

type UnitDetail = {
  unit?: {
    unit_id?: number;
    unit_code?: string;
    unit_name?: string;
    county_name?: string;
  };
  vaccination?: {
    eligible?: number;
    vaccinated?: number;
    remaining?: number;
    coverage_percent?: number;
  };
  operation_counts?: Array<{
    name?: string;
    value?: number;
  }>;
  operation_history?: Array<{
    event_date?: string;
    operation_type?: string;
  }>;
  county_predictions?: Array<{
    value?: number;
  }>;
};

type UnitRow = {
  unit_id: number;
  unit_name?: string;
  value?: number;
  progress_percent?: number;
};

const API_BASE = "/api/v1/gis/dashboard/kpi";

const nf = new Intl.NumberFormat("fa-IR", {
  maximumFractionDigits: 1,
});

function num(value: unknown): string {
  return nf.format(Number(value || 0));
}

function pct(value: unknown): string {
  return `${nf.format(Number(value || 0))}%`;
}

async function api<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    credentials: "include",
    headers: {
      Accept: "application/json",
    },
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`${response.status} ${text}`);
  }

  return response.json();
}

function LineChart({
  data,
  height = 220,
}: {
  data?: Array<{ period: string; value: number }>;
  height?: number;
}) {
  if (!data?.length) {
    return (
      <div className="chart-empty">
        داده‌ای برای نمودار وجود ندارد
      </div>
    );
  }

  const width = 760;
  const padding = 34;

  const values = data.map((item) => Number(item.value || 0));
  const max = Math.max(...values, 1);

  const step =
    data.length > 1
      ? (width - padding * 2) / (data.length - 1)
      : 0;

  const points = data
    .map((item, index) => {
      const x = padding + index * step;
      const y =
        height -
        padding -
        (Number(item.value || 0) / max) *
        (height - padding * 2);

      return `${x},${y}`;
    })
    .join(" ");

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      width="100%"
      height={height}
      role="img"
      aria-label="نمودار روند"
    >
      <line
        x1={padding}
        x2={width - padding}
        y1={height - padding}
        y2={height - padding}
        stroke="#173b50"
      />

      <polyline
        points={points}
        fill="none"
        stroke="#19d9ff"
        strokeWidth="4"
      />

      {data.map((item, index) => {
        const [x, y] = points.split(" ")[index].split(",");

        return (
          <circle
            key={`${item.period}-${index}`}
            cx={x}
            cy={y}
            r="4"
            fill="#19d9ff"
          />
        );
      })}

      {data.map((item, index) => (
        <text
          key={`label-${item.period}-${index}`}
          x={padding + index * step}
          y={height - 10}
          fill="#7195a8"
          fontSize="11"
          textAnchor="middle"
        >
          {String(item.period).slice(5)}
        </text>
      ))}
    </svg>
  );
}

function BarChart({
  data,
}: {
  data?: Array<{
    name?: string;
    value?: number;
  }>;
}) {
  if (!data?.length) {
    return (
      <div className="chart-empty">
        داده‌ای برای نمودار وجود ندارد
      </div>
    );
  }

  const max = Math.max(
    ...data.map((item) => Number(item.value || 0)),
    1,
  );

  return (
    <div className="bar-chart">
      {data.slice(0, 12).map((item, index) => {
        const value = Number(item.value || 0);
        const height = Math.max(5, (value / max) * 165);

        return (
          <div className="bar-item" key={`${item.name}-${index}`}>
            <div
              className="bar-value"
              title={num(value)}
              style={{ height }}
            />

            <div className="bar-label">
              {String(item.name || "").slice(0, 12)}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function Donut({
  value,
  max,
}: {
  value: number;
  max: number;
}) {
  const progress = Math.min(
    100,
    max > 0 ? (value / max) * 100 : 0,
  );

  return (
    <div className="donut-wrapper">
      <div
        className="donut"
        style={{
          background: `conic-gradient(#19d9ff ${progress}%, #183748 0)`,
        }}
      >
        <div className="donut-inner">
          <strong>{pct(progress)}</strong>
          <small>پیشرفت</small>
        </div>
      </div>
    </div>
  );
}

function Card({
  label,
  value,
  sub,
  onClick,
}: {
  label: string;
  value: React.ReactNode;
  sub?: string;
  onClick?: () => void;
}) {
  return (
    <div
      className={`kpi-card ${onClick ? "clickable" : ""}`}
      onClick={onClick}
      role={onClick ? "button" : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={
        onClick
          ? (event) => {
            if (event.key === "Enter") {
              onClick();
            }
          }
          : undefined
      }
    >
      <div className="label">{label}</div>
      <div className="value">{value}</div>

      {sub && <div className="sub">{sub}</div>}
    </div>
  );
}

function UnitExplorer({
  onOpen,
  metric,
}: {
  onOpen: (unitId: number) => void;
  metric: string;
}) {
  const [query, setQuery] = useState("");
  const [rows, setRows] = useState<UnitRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        setLoading(true);
        setError("");

        const result = await api<{ units?: UnitRow[] }>(
          `/drilldown/${encodeURIComponent(metric)}`,
        );

        if (!cancelled) {
          setRows(Array.isArray(result.units) ? result.units : []);
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "خطا در دریافت اطلاعات",
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    load();

    return () => {
      cancelled = true;
    };
  }, [metric]);

  const filteredRows = useMemo(() => {
    const q = query.trim();

    if (!q) {
      return rows.slice(0, 1000);
    }

    return rows
      .filter((row) =>
        String(row.unit_name || "").includes(q),
      )
      .slice(0, 1000);
  }, [rows, query]);

  const titles: Record<string, string> = {
    all: "همه عملیات",
    vaccination: "واکسیناسیون",
    disease_reports: "گزارش بیماری",
    care: "مراقبت",
    lab: "آزمایشگاه",
    samples: "ارسال نمونه",
    spraying: "سمپاشی",
    operations: "تاریخچه عملیات",
  };

  const title = titles[metric] || "واحدها";

  return (
    <div className="kpi-panel">
      <h2>
        Drill-down واحدها — {title}
      </h2>

      <p className="drilldown-description">
        با کلیک روی هر KPI، واحدهای تشکیل‌دهنده آن شاخص نمایش داده
        می‌شوند. با کلیک روی هر واحد، جزئیات و تاریخچه عملیات همان
        واحد قابل مشاهده است.
      </p>

      <div className="unit-search">
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="جستجوی نام واحد..."
        />
      </div>

      {loading && (
        <div className="loading-text">
          در حال دریافت داده زنده...
        </div>
      )}

      {error && (
        <div className="error-text">
          {error}
        </div>
      )}

      {!loading && !error && (
        <div className="unit-list">
          {filteredRows.length === 0 ? (
            <div className="chart-empty">
              واحدی پیدا نشد.
            </div>
          ) : (
            filteredRows.map((row) => {
              const progress = Number(
                row.progress_percent || 0,
              );

              return (
                <div
                  className="unit-row"
                  key={row.unit_id}
                  onClick={() => onOpen(Number(row.unit_id))}
                >
                  <span>
                    {row.unit_name ||
                      `واحد ${row.unit_id}`}
                  </span>

                  <span>
                    {num(row.value)}

                    {metric === "vaccination" && (
                      <span
                        className={`badge ${progress >= 80
                            ? "good"
                            : progress >= 50
                              ? "warn"
                              : "bad"
                          }`}
                      >
                        {pct(progress)}
                      </span>
                    )}
                  </span>
                </div>
              );
            })
          )}
        </div>
      )}
    </div>
  );
}

export default function LiveKpiDashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [tab, setTab] = useState("overview");

  const [unitId, setUnitId] = useState<number | null>(null);
  const [unit, setUnit] = useState<UnitDetail | null>(null);

  const [unitMetric, setUnitMetric] = useState("all");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [refresh, setRefresh] = useState(0);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        setLoading(true);
        setError("");

        const result = await api<DashboardData>(
          "/overview",
        );

        if (!cancelled) {
          setData(result);
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "خطا در دریافت داشبورد",
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    load();

    return () => {
      cancelled = true;
    };
  }, [refresh]);

  useEffect(() => {
    if (unitId === null) {
      setUnit(null);
      return;
    }

    let cancelled = false;

    async function loadUnit() {
      try {
        setLoading(true);
        setError("");

        const result = await api<UnitDetail>(
          `/units/${unitId}`,
        );

        if (!cancelled) {
          setUnit(result);
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "خطا در دریافت اطلاعات واحد",
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadUnit();

    return () => {
      cancelled = true;
    };
  }, [unitId]);

  const cards = data?.cards || {};
  const series = data?.series || {};

  const diseases =
    data?.breakdowns?.disease_by_name || [];

  const counties =
    data?.breakdowns?.vaccination_by_county || [];

  function openMetric(metric: string) {
    setUnitMetric(metric);
    setTab("units");
  }

  const tabs = [
    ["overview", "نمای کلی"],
    ["disease", "بیماری و اپیدمیولوژی"],
    ["care", "مراقبت فعال"],
    ["lab", "آزمایشگاه و نمونه"],
    ["vaccination", "واکسیناسیون"],
    ["inventory", "زنجیره واکسن"],
    ["units", "واحدها و Drill-down"],
  ];

  if (loading && !data && !unit) {
    return (
      <div className="live-kpi-page" dir="rtl">
        <div className="kpi-panel loading-panel">
          در حال دریافت KPIهای زنده از PostgreSQL...
        </div>
      </div>
    );
  }

  if (error && !data) {
    return (
      <div className="live-kpi-page" dir="rtl">
        <div className="kpi-panel error-panel">
          <strong>خطا:</strong> {error}
        </div>
      </div>
    );
  }

  if (unitId !== null && unit) {
    const vaccination = unit.vaccination || {};
    const operations =
      unit.operation_counts || [];

    return (
      <div
        className="live-kpi-page"
        dir="rtl"
      >
        <button
          className="back-button"
          onClick={() => setUnitId(null)}
        >
          ← بازگشت به داشبورد
        </button>

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
              vaccination.coverage_percent,
            )}
            sub="بر اساس داده واقعی واحد"
          />

          <Card
            label="تعداد عملیات ثبت‌شده"
            value={num(
              unit.operation_history?.length || 0,
            )}
          />

          <Card
            label="پیش‌بینی شهرستان"
            value={num(
              unit.county_predictions?.[0]
                ?.value || 0,
            )}
            sub="سطح شهرستان"
          />
        </div>

        <div className="kpi-two">
          <div className="kpi-panel">
            <h2>
              پیشرفت واکسیناسیون واحد
            </h2>

            <Donut
              value={
                Number(
                  vaccination.vaccinated || 0,
                )
              }
              max={
                Number(
                  vaccination.eligible || 0,
                )
              }
            />
          </div>

          <div className="kpi-panel">
            <h2>
              تعداد عملیات به تفکیک نوع
            </h2>

            <BarChart data={operations} />
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
                (item, index) => (
                  <tr key={index}>
                    <td>
                      {String(
                        item.event_date || "",
                      ).slice(0, 19)}
                    </td>

                    <td>
                      {item.operation_type || "-"}
                    </td>
                  </tr>
                ),
              )}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

  return (
    <div
      className="live-kpi-page"
      dir="rtl"
    >
      <div className="live-kpi-head">
        <div>
          <h1>
            داشبورد زنده کنترل بیماری و عملیات
            دامپزشکی
          </h1>

          <p>
            تمام اعداد در هر درخواست مستقیماً از
            PostgreSQL خوانده می‌شوند.
          </p>
        </div>

        <button
          className="kpi-tab refresh-button"
          onClick={() =>
            setRefresh((value) => value + 1)
          }
        >
          ↻ بروزرسانی
        </button>
      </div>

      <div className="kpi-tabs">
        {tabs.map(([key, title]) => (
          <button
            key={key}
            className={`kpi-tab ${tab === key ? "active" : ""
              }`}
            onClick={() => setTab(key)}
          >
            {title}
          </button>
        ))}
      </div>

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
              value={num(
                cards.total_livestock,
              )}
            />

            <Card
              label="گزارش بیماری"
              value={num(
                cards.disease_reports,
              )}
              onClick={() =>
                openMetric("disease_reports")
              }
            />

            <Card
              label="مراقبت فعال"
              value={num(
                cards.care_records,
              )}
              onClick={() =>
                openMetric("care")
              }
            />

            <Card
              label="واکسیناسیون انجام‌شده"
              value={num(
                cards.vaccinated_animals,
              )}
              onClick={() =>
                openMetric("vaccination")
              }
            />

            <Card
              label="پوشش واکسیناسیون"
              value={pct(
                cards.vaccination_coverage,
              )}
            />

            <Card
              label="باقی‌مانده واکسیناسیون"
              value={num(
                cards.vaccination_remaining,
              )}
              onClick={() =>
                openMetric("vaccination")
              }
            />

            <Card
              label="نتایج آزمایشگاهی"
              value={num(
                cards.lab_results,
              )}
              onClick={() =>
                openMetric("lab")
              }
            />

            <Card
              label="نرخ مثبت آزمایشگاه"
              value={pct(
                cards.lab_positive_rate,
              )}
            />

            <Card
              label="موجودی واکسن"
              value={num(
                cards.inventory_packages,
              )}
            />

            <Card
              label="واکسن نزدیک انقضا"
              value={num(
                cards.expiring_30_days,
              )}
            />
          </div>

          <div className="kpi-layout">
            <div>
              <div className="kpi-panel">
                <h2>
                  روند واکسیناسیون
                </h2>

                <LineChart
                  data={series.vaccination}
                />
              </div>

              <div className="kpi-two">
                <div className="kpi-panel">
                  <h2>
                    روند گزارش بیماری
                  </h2>

                  <LineChart
                    data={
                      series.disease_reports
                    }
                  />
                </div>

                <div className="kpi-panel">
                  <h2>
                    موارد مثبت مراقبت
                  </h2>

                  <LineChart
                    data={
                      series.care_positive
                    }
                  />
                </div>
              </div>
            </div>

            <div>
              <div className="kpi-panel">
                <h2>
                  پوشش واکسیناسیون
                </h2>

                <Donut
                  value={Number(
                    cards.vaccinated_animals ||
                    0,
                  )}
                  max={Number(
                    cards.eligible_animals ||
                    0,
                  )}
                />
              </div>

              <div className="kpi-panel">
                <h2>
                  بیماری‌های پرتکرار
                </h2>

                <BarChart
                  data={diseases}
                />
              </div>
            </div>
          </div>

          <div className="kpi-panel">
            <h2>
              مقایسه عملکرد واکسیناسیون شهرستان‌ها
            </h2>

            <BarChart
              data={counties.map((item) => ({
                name: item.name,
                value: Number(
                  item.coverage || 0,
                ),
              }))}
            />
          </div>
        </>
      )}

      {tab === "disease" && (
        <div className="kpi-layout">
          <div>
            <div className="kpi-grid">
              <Card
                label="گزارش بیماری"
                value={num(
                  cards.disease_reports,
                )}
                onClick={() =>
                  openMetric(
                    "disease_reports",
                  )
                }
              />

              <Card
                label="وقوع بیماری"
                value={num(
                  cards.disease_occurrences,
                )}
              />

              <Card
                label="بیماری‌های ثبت‌شده"
                value={num(
                  cards.diseases,
                )}
              />

              <Card
                label="کانون فعال"
                value={num(
                  cards.active_outbreaks,
                )}
              />
            </div>

            <div className="kpi-panel">
              <h2>
                روند گزارش‌های بیماری
              </h2>

              <LineChart
                data={
                  series.disease_reports
                }
                height={300}
              />
            </div>
          </div>

          <div className="kpi-panel">
            <h2>
              توزیع بیماری‌ها
            </h2>

            <BarChart data={diseases} />
          </div>
        </div>
      )}

      {tab === "care" && (
        <>
          <div className="kpi-grid">
            <Card
              label="رکورد مراقبت"
              value={num(
                cards.care_records,
              )}
            />

            <Card
              label="دام بررسی‌شده"
              value={num(
                cards.care_animals,
              )}
            />

            <Card
              label="مثبت"
              value={num(
                cards.care_positive,
              )}
            />

            <Card
              label="منفی"
              value={num(
                cards.care_negative,
              )}
            />

            <Card
              label="مشکوک"
              value={num(
                cards.care_suspicious,
              )}
            />

            <Card
              label="نرخ مثبت"
              value={pct(
                cards.care_positive_rate,
              )}
            />
          </div>

          <div className="kpi-panel">
            <h2>
              روند موارد مثبت مراقبت
            </h2>

            <LineChart
              data={
                series.care_positive
              }
              height={300}
            />
          </div>
        </>
      )}

      {tab === "lab" && (
        <>
          <div className="kpi-grid">
            <Card
              label="نتایج آزمایشگاهی"
              value={num(
                cards.lab_results,
              )}
              onClick={() =>
                openMetric("lab")
              }
            />

            <Card
              label="نمونه آزمایشگاه"
              value={num(
                cards.lab_samples,
              )}
            />

            <Card
              label="نمونه ارسال‌شده"
              value={num(
                cards.sent_samples,
              )}
            />

            <Card
              label="مثبت"
              value={num(
                cards.lab_positive,
              )}
            />

            <Card
              label="نرخ مثبت"
              value={pct(
                cards.lab_positive_rate,
              )}
            />
          </div>

          <div className="kpi-two">
            <div className="kpi-panel">
              <h2>
                وضعیت نمونه و نتیجه
              </h2>

              <BarChart
                data={[
                  {
                    name: "نتیجه",
                    value: Number(
                      cards.lab_results ||
                      0,
                    ),
                  },
                  {
                    name: "ارسال",
                    value: Number(
                      cards.sent_samples ||
                      0,
                    ),
                  },
                  {
                    name: "مثبت",
                    value: Number(
                      cards.lab_positive ||
                      0,
                    ),
                  },
                ]}
              />
            </div>

            <div className="kpi-panel">
              <h2>
                توضیح Drill-down
              </h2>

              <p className="drilldown-description">
                از صفحه واحدها می‌توان به واحد
                اپیدمیولوژیک رفت و تاریخچه عملیات
                همان واحد را مشاهده کرد.
              </p>
            </div>
          </div>
        </>
      )}

      {tab === "vaccination" && (
        <>
          <div className="kpi-grid">
            <Card
              label="دام واجد شرایط"
              value={num(
                cards.eligible_animals,
              )}
            />

            <Card
              label="واکسن زده‌شده"
              value={num(
                cards.vaccinated_animals,
              )}
            />

            <Card
              label="باقی‌مانده"
              value={num(
                cards.vaccination_remaining,
              )}
            />

            <Card
              label="پوشش"
              value={pct(
                cards.vaccination_coverage,
              )}
            />

            <Card
              label="توزیع بسته"
              value={num(
                cards.distributed_packages,
              )}
            />

            <Card
              label="دفع بسته"
              value={num(
                cards.disposed_packages,
              )}
            />
          </div>

          <div className="kpi-two">
            <div className="kpi-panel">
              <h2>
                روند واکسیناسیون
              </h2>

              <LineChart
                data={series.vaccination}
                height={300}
              />
            </div>

            <div className="kpi-panel">
              <h2>پیشرفت</h2>

              <Donut
                value={Number(
                  cards.vaccinated_animals ||
                  0,
                )}
                max={Number(
                  cards.eligible_animals ||
                  0,
                )}
              />
            </div>
          </div>

          <div className="kpi-panel">
            <h2>
              مقایسه شهرستان‌ها
            </h2>

            <BarChart
              data={counties.map((item) => ({
                name: item.name,
                value: Number(
                  item.coverage || 0,
                ),
              }))}
            />
          </div>
        </>
      )}

      {tab === "inventory" && (
        <>
          <div className="kpi-grid">
            <Card
              label="موجودی بسته"
              value={num(
                cards.inventory_packages,
              )}
            />

            <Card
              label="توزیع‌شده"
              value={num(
                cards.distributed_packages,
              )}
            />

            <Card
              label="دفع‌شده"
              value={num(
                cards.disposed_packages,
              )}
            />

            <Card
              label="نزدیک انقضا (۳۰ روز)"
              value={num(
                cards.expiring_30_days,
              )}
            />
          </div>

          <div className="kpi-panel">
            <h2>
              جریان زنجیره واکسن
            </h2>

            <BarChart
              data={[
                {
                  name: "موجودی",
                  value: Number(
                    cards.inventory_packages ||
                    0,
                  ),
                },
                {
                  name: "توزیع",
                  value: Number(
                    cards.distributed_packages ||
                    0,
                  ),
                },
                {
                  name: "دفع",
                  value: Number(
                    cards.disposed_packages ||
                    0,
                  ),
                },
                {
                  name: "انقضای نزدیک",
                  value: Number(
                    cards.expiring_30_days ||
                    0,
                  ),
                },
              ]}
            />
          </div>
        </>
      )}

      {tab === "units" && (
        <UnitExplorer
          onOpen={setUnitId}
          metric={unitMetric}
        />
      )}
    </div>
  );
}