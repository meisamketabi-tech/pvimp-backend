import React, { useEffect, useMemo, useState } from "react";
import {
  Bar,
  BarChart,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import {
  useNavigate,
  useParams,
} from "react-router-dom";

import api from "../services/api";
import {
  vaccinationKpiCategories,
  vaccinationKpiIndicators,
  type VaccinationKpiIndicator,
  type VaccinationKpiRow,
} from "../data/vaccinationKpiCatalog";

import "./VaccinationKpiCategories.css";

type Period = 3 | 4 | 5 | 12;

type PeriodOverride = {
  annualTarget?: number;
  target3?: number;
  actual3?: number;
  target5?: number;
  actual5?: number;
  target12?: number;
  actual12?: number;
};

type UnitRow = {
  unit_code: string;
  unit_name: string;
  county_name: string | null;
  unit_type: string | null;
  total_animals: number;
  vaccinated_animals: number;
  remaining_animals: number;
  coverage_percent: number;
  status: string;
  priority: string;
};

const COLORS = {
  critical: "#dc2626",
  warning: "#f59e0b",
  track: "#2563eb",
  excellent: "#16a34a",
  neutral: "#64748b",
};

const PERIOD_LABELS: Record<Period, string> = {
  3: "۳ ماهه",
  4: "۴ ماهه - منبع Excel",
  5: "۵ ماهه",
  12: "سالانه",
};

function fmt(value: number | null | undefined) {
  return new Intl.NumberFormat("fa-IR").format(Number(value ?? 0));
}

function pct(value: number | null | undefined) {
  return `${Number(value ?? 0).toFixed(1)}%`;
}

function normalize(text: string) {
  return text
    .replace(/\u200c/g, "")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();
}

function statusForAchievement(value: number | null) {
  const x = Number(value ?? 0);
  if (x >= 90) return "EXCELLENT";
  if (x >= 75) return "ON_TRACK";
  if (x >= 50) return "WARNING";
  return "CRITICAL";
}

function statusLabel(status: string) {
  switch (status) {
    case "EXCELLENT":
      return "عالی";
    case "ON_TRACK":
      return "مطلوب";
    case "WARNING":
      return "نیازمند توجه";
    case "CRITICAL":
      return "بحرانی";
    case "NO_COVERAGE":
      return "بدون پوشش";
    default:
      return status || "-";
  }
}

function statusColor(status: string) {
  switch (status) {
    case "EXCELLENT":
      return COLORS.excellent;
    case "ON_TRACK":
      return COLORS.track;
    case "WARNING":
      return COLORS.warning;
    case "CRITICAL":
    case "NO_COVERAGE":
      return COLORS.critical;
    default:
      return COLORS.neutral;
  }
}

function indicatorPeriodValue(
  indicator: VaccinationKpiIndicator,
  row: VaccinationKpiRow,
  period: Period,
  overrides: Record<string, PeriodOverride>,
) {
  const key = `${indicator.id}::${row.county}`;

  if (period === 4) {
    return row.actual;
  }

  const override = overrides[key];

  if (!override) return null;

  if (period === 3) return override.actual3 ?? null;
  if (period === 5) return override.actual5 ?? null;
  if (period === 12) return override.actual12 ?? null;

  return null;
}

function indicatorTarget(
  indicator: VaccinationKpiIndicator,
  row: VaccinationKpiRow,
  period: Period,
  overrides: Record<string, PeriodOverride>,
) {
  const key = `${indicator.id}::${row.county}`;
  const override = overrides[key];

  if (period === 4) return row.periodTarget;
  if (period === 12) return override?.annualTarget ?? row.annualTarget;
  if (period === 3) return override?.target3 ?? null;
  if (period === 5) return override?.target5 ?? null;

  return null;
}

function achievement(
  actual: number | null,
  target: number | null,
) {
  if (actual == null || target == null || target === 0) {
    return null;
  }

  return (actual * 100) / target;
}

function loadOverrides(): Record<string, PeriodOverride> {
  try {
    return JSON.parse(
      localStorage.getItem("pvimp_vaccination_kpi_period_overrides_v1") ||
        "{}",
    );
  } catch {
    return {};
  }
}

function saveOverrides(
  value: Record<string, PeriodOverride>,
) {
  localStorage.setItem(
    "pvimp_vaccination_kpi_period_overrides_v1",
    JSON.stringify(value),
  );
}

function getApiTerms(indicator: VaccinationKpiIndicator) {
  const text = normalize(
    `${indicator.sheet} ${indicator.title} ${indicator.indicator}`,
  );

  const terms: string[] = [];

  if (text.includes("شاربن")) terms.push("شاربن");
  if (text.includes("ppr")) terms.push("ppr");
  if (text.includes("آبله")) terms.push("آبله");
  if (text.includes("لمپی")) terms.push("لمپی");
  if (text.includes("تب برفکی")) terms.push("تب برفکی");
  if (text.includes("هاری")) terms.push("هاری");
  if (text.includes("rev1")) terms.push("rev1", "بروسلوز");
  if (text.includes("fd iriba")) terms.push("fd iriba", "بروسلوز");
  if (text.includes("rd iriba")) terms.push("rd iriba", "بروسلوز");

  return terms.length ? terms : [indicator.indicator];
}

export default function VaccinationKpiCategories() {
  const {
    categoryId = "infectious",
    indicatorId,
    countyCode,
  } = useParams<{
    categoryId: string;
    indicatorId?: string;
    countyCode?: string;
  }>();

  const navigate = useNavigate();

  const [period, setPeriod] = useState<Period>(4);
  const [overrides, setOverrides] =
    useState<Record<string, PeriodOverride>>(loadOverrides);

  const [units, setUnits] = useState<UnitRow[]>([]);
  const [unitsLoading, setUnitsLoading] = useState(false);
  const [unitStatusFilter, setUnitStatusFilter] =
    useState<string | null>(null);

  const category = vaccinationKpiCategories.find(
    (x) => x.id === categoryId,
  ) ?? vaccinationKpiCategories[0];

  const categoryIndicators =
    vaccinationKpiIndicators.filter(
      (x) => x.categoryId === category.id,
    );

  const selectedIndicator =
    vaccinationKpiIndicators.find(
      (x) => x.id === indicatorId,
    ) ?? categoryIndicators[0] ?? null;

  const selectedRows = selectedIndicator?.rows ?? [];

  const saveOverride = (
    key: string,
    field: keyof PeriodOverride,
    value: string,
  ) => {
    const next = {
      ...overrides,
      [key]: {
        ...(overrides[key] ?? {}),
        [field]:
          value === ""
            ? undefined
            : Number(value),
      },
    };

    setOverrides(next);
    saveOverrides(next);
  };

  const indicatorChart = useMemo(() => {
    return categoryIndicators.map((indicator) => {
      const actuals = indicator.rows
        .map((row) =>
          indicatorPeriodValue(
            indicator,
            row,
            period,
            overrides,
          ),
        )
        .filter((x): x is number => x != null);

      const targets = indicator.rows
        .map((row) =>
          indicatorTarget(
            indicator,
            row,
            period,
            overrides,
          ),
        )
        .filter((x): x is number => x != null);

      const actual = actuals.reduce(
        (sum, value) => sum + value,
        0,
      );

      const target = targets.reduce(
        (sum, value) => sum + value,
        0,
      );

      const achievementValue =
        target > 0
          ? (actual * 100) / target
          : null;

      return {
        id: indicator.id,
        name: indicator.indicator,
        livestock: indicator.livestockGroup,
        achievement: achievementValue,
        actual,
        target,
        status: statusForAchievement(
          achievementValue,
        ),
      };
    });
  }, [
    categoryIndicators,
    period,
    overrides,
  ]);

  const livestockCharts = useMemo(() => {
    if (!selectedIndicator) return [];

    return [selectedIndicator].map((indicator) => {
      const rows = indicator.rows.map((row) => {
        const actual = indicatorPeriodValue(
          indicator,
          row,
          period,
          overrides,
        );

        const target = indicatorTarget(
          indicator,
          row,
          period,
          overrides,
        );

        return {
          county: row.county,
          actual,
          target,
          achievement: achievement(
            actual,
            target,
          ),
          status: statusForAchievement(
            achievement(actual, target),
          ),
        };
      });

      return {
        indicator,
        rows,
      };
    });
  }, [
    selectedIndicator,
    period,
    overrides,
  ]);

  const selectedCounty = selectedRows.find(
    (x) =>
      normalize(x.county) ===
      normalize(countyCode ?? ""),
  );

  const countyChart = useMemo(() => {
    if (!selectedIndicator) return [];

    return selectedIndicator.rows.map((row) => {
      const actual = indicatorPeriodValue(
        selectedIndicator,
        row,
        period,
        overrides,
      );

      const target = indicatorTarget(
        selectedIndicator,
        row,
        period,
        overrides,
      );

      return {
        county: row.county,
        achievement:
          achievement(actual, target),
        actual,
        target,
      };
    });
  }, [
    selectedIndicator,
    period,
    overrides,
  ]);

  const unitStatusData = useMemo(() => {
    const groups: Record<string, number> = {
      EXCELLENT: 0,
      ON_TRACK: 0,
      WARNING: 0,
      CRITICAL: 0,
      NO_COVERAGE: 0,
    };

    units.forEach((unit) => {
      const key =
        unit.status in groups
          ? unit.status
          : unit.coverage_percent >= 90
            ? "EXCELLENT"
            : unit.coverage_percent >= 75
              ? "ON_TRACK"
              : unit.coverage_percent >= 50
                ? "WARNING"
                : "CRITICAL";

      groups[key] += 1;
    });

    return Object.entries(groups)
      .filter(([, value]) => value > 0)
      .map(([status, value]) => ({
        status,
        name: statusLabel(status),
        value,
        fill: statusColor(status),
      }));
  }, [units]);

  const filteredUnits = useMemo(() => {
    if (!unitStatusFilter) return units;

    return units.filter((unit) => {
      const status =
        unit.status ||
        statusForAchievement(
          unit.coverage_percent,
        );

      return status === unitStatusFilter;
    });
  }, [units, unitStatusFilter]);

  useEffect(() => {
    if (!selectedIndicator) return;

    let cancelled = false;

    async function loadUnits() {
      setUnits([]);
      setUnitStatusFilter(null);
      setUnitsLoading(true);

      try {
        const vaccineResponse =
          await api.get(
            "/api/v1/gis/kpi/vaccination/vaccines",
          );

        const vaccines =
          Array.isArray(vaccineResponse.data)
            ? vaccineResponse.data
            : [];

        const terms =
          getApiTerms(selectedIndicator);

        const matched =
          vaccines.find((item: any) => {
            const value = normalize(
              String(item?.vaccine_type ?? ""),
            );

            return terms.some((term) =>
              value.includes(normalize(term)),
            );
          }) ?? null;

        if (!matched?.vaccine_type) {
          return;
        }

        const response =
          await api.get(
            `/api/v1/gis/kpi/vaccination/vaccine/${encodeURIComponent(
              matched.vaccine_type,
            )}/units-paginated`,
            {
              params: {
                page: 1,
                page_size: 500,
              },
            },
          );

        const items =
          Array.isArray(response.data?.items)
            ? response.data.items
            : [];

        if (!cancelled) {
          setUnits(
            items.map((item: any) => ({
              unit_code: String(
                item?.unit_code ?? "",
              ),
              unit_name: String(
                item?.unit_name ?? "",
              ),
              county_name:
                item?.county_name ?? null,
              unit_type:
                item?.unit_type ?? null,
              total_animals: Number(
                item?.total_animals ?? 0,
              ),
              vaccinated_animals: Number(
                item?.vaccinated_animals ?? 0,
              ),
              remaining_animals: Number(
                item?.remaining_animals ?? 0,
              ),
              coverage_percent: Number(
                item?.coverage_percent ?? 0,
              ),
              status: String(
                item?.status ?? "CRITICAL",
              ),
              priority: String(
                item?.priority ?? "HIGH",
              ),
            })),
          );
        }
      } catch (error) {
        console.warn(
          "[VACCINATION KPI] unit drilldown unavailable",
          error,
        );
      } finally {
        if (!cancelled) {
          setUnitsLoading(false);
        }
      }
    }

    loadUnits();

    return () => {
      cancelled = true;
    };
  }, [selectedIndicator]);

  if (!category) {
    return null;
  }

  return (
    <div
      className="vaccination-kpi-categories"
      dir="rtl"
    >
      <header className="vkc-header">
        <div>
          <div className="vkc-eyebrow">
            سامانه مدیریت یکپارچه دامپزشکی
          </div>

          <h1>
            گزارش نموداری عملکرد واکسیناسیون،
            پایش و مراقبت
          </h1>

          <p>
            ساختار دسته‌بندی بر اساس فایل عملکرد
            واکسیناسیون، پایش و مراقبت استان و شهرستان
          </p>
        </div>

        <button
          type="button"
          onClick={() =>
            navigate("/gis/kpi/vaccination")
          }
        >
          بازگشت به KPI اصلی
        </button>
      </header>

      <section className="vkc-toolbar">
        <div>
          <strong>دوره گزارش:</strong>
          <select
            value={period}
            onChange={(event) =>
              setPeriod(
                Number(event.target.value) as Period,
              )
            }
          >
            <option value={3}>۳ ماهه</option>
            <option value={4}>
              ۴ ماهه - داده منبع
            </option>
            <option value={5}>۵ ماهه</option>
            <option value={12}>سالانه</option>
          </select>
        </div>

        <div className="vkc-source-note">
          داده منبع این فایل تا تاریخ
          <strong> ۱۴۰۵/۰۵/۰۱ </strong>
          برای دوره ۴ ماهه است؛ دوره‌های ۳، ۵ و
          سالانه قابل ورود/اصلاح هستند.
        </div>
      </section>

      <nav className="vkc-category-tabs">
        {vaccinationKpiCategories.map((item) => (
          <button
            key={item.id}
            className={
              item.id === category.id
                ? "active"
                : ""
            }
            type="button"
            onClick={() =>
              navigate(
                `/gis/kpi/vaccination/categories/${item.id}`,
              )
            }
          >
            {item.title}
          </button>
        ))}
      </nav>

      <section className="vkc-panel">
        <div className="vkc-panel-title">
          <div>
            <h2>{category.title}</h2>
            <p>{category.description}</p>
          </div>
        </div>

        <div className="vkc-chart-grid">
          <div className="vkc-chart-card">
            <h3>
              عملکرد شاخص‌های این گروه -{" "}
              {PERIOD_LABELS[period]}
            </h3>

            <div className="vkc-chart">
              <ResponsiveContainer>
                <BarChart
                  data={indicatorChart}
                  onClick={(state: any) => {
                    const active =
                      state?.activePayload?.[0]
                        ?.payload;

                    if (active?.id) {
                      navigate(
                        `/gis/kpi/vaccination/categories/${category.id}/${encodeURIComponent(
                          active.id,
                        )}`,
                      );
                    }
                  }}
                >
                  <XAxis
                    dataKey="name"
                    interval={0}
                    angle={-25}
                    textAnchor="end"
                    height={90}
                  />
                  <YAxis
                    domain={[0, 100]}
                    tickFormatter={(value) =>
                      `${value}%`
                    }
                  />
                  <Tooltip
                    formatter={(value: any) =>
                      pct(Number(value ?? 0))
                    }
                  />
                  <Legend />
                  <Bar
                    dataKey="achievement"
                    name="درصد تحقق"
                    cursor="pointer"
                  >
                    {indicatorChart.map(
                      (entry) => (
                        <Cell
                          key={entry.id}
                          fill={statusColor(
                            entry.status,
                          )}
                        />
                      ),
                    )}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="vkc-chart-card">
            <h3>وضعیت شاخص‌ها</h3>

            <div className="vkc-chart">
              <ResponsiveContainer>
                <PieChart>
                  <Pie
                    data={[
                      "EXCELLENT",
                      "ON_TRACK",
                      "WARNING",
                      "CRITICAL",
                    ].map((status) => ({
                      status,
                      name: statusLabel(status),
                      value:
                        indicatorChart.filter(
                          (x) =>
                            x.status === status,
                        ).length,
                      fill: statusColor(status),
                    })).filter(
                      (x) => x.value > 0,
                    )}
                    dataKey="value"
                    nameKey="name"
                    outerRadius={105}
                    label={({ name, value }) =>
                      `${name}: ${value}`
                    }
                    onClick={(entry: any) => {
                      const item =
                        indicatorChart.find(
                          (x) =>
                            x.status ===
                            entry?.status,
                        );

                      if (item) {
                        navigate(
                          `/gis/kpi/vaccination/categories/${category.id}/${encodeURIComponent(
                            item.id,
                          )}`,
                        );
                      }
                    }}
                  />
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </section>

      {selectedIndicator && (
        <>
          <section className="vkc-panel">
            <div className="vkc-panel-title">
              <div>
                <h2>
                  {selectedIndicator.indicator}
                </h2>
                <p>
                  شیت منبع:{" "}
                  {selectedIndicator.sheet}
                </p>
              </div>
            </div>

            <div className="vkc-livestock-grid">
              {livestockCharts.map(
                ({ indicator, rows }) => (
                  <div
                    className="vkc-chart-card"
                    key={indicator.id}
                  >
                    <h3>
                      گروه دام:{" "}
                      {indicator.livestockGroup}
                    </h3>

                    <div className="vkc-chart">
                      <ResponsiveContainer>
                        <BarChart
                          data={rows}
                          onClick={(
                            state: any,
                          ) => {
                            const active =
                              state?.activePayload?.[0]
                                ?.payload;

                            if (
                              active?.county
                            ) {
                              navigate(
                                `/gis/kpi/vaccination/categories/${category.id}/${encodeURIComponent(
                                  indicator.id,
                                )}/county/${encodeURIComponent(
                                  active.county,
                                )}`,
                              );
                            }
                          }}
                        >
                          <XAxis
                            dataKey="county"
                            interval={0}
                            angle={-35}
                            textAnchor="end"
                            height={95}
                          />
                          <YAxis
                            domain={[0, 100]}
                            tickFormatter={(v) =>
                              `${v}%`
                            }
                          />
                          <Tooltip
                            formatter={(
                              value: any,
                            ) =>
                              pct(
                                Number(
                                  value ?? 0,
                                ),
                              )
                            }
                          />
                          <Bar
                            dataKey="achievement"
                            name="درصد تحقق"
                            cursor="pointer"
                          >
                            {rows.map(
                              (row) => (
                                <Cell
                                  key={
                                    row.county
                                  }
                                  fill={statusColor(
                                    row.status,
                                  )}
                                />
                              ),
                            )}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                ),
              )}
            </div>
          </section>

          {countyCode && selectedCounty && (
            <section className="vkc-panel">
              <div className="vkc-panel-title">
                <div>
                  <h2>
                    جزئیات شهرستان{" "}
                    {selectedCounty.county}
                  </h2>
                  <p>
                    {selectedIndicator.indicator}
                    {" - "}
                    {PERIOD_LABELS[period]}
                  </p>
                </div>

                <button
                  type="button"
                  onClick={() =>
                    navigate(
                      `/gis/kpi/vaccination/categories/${category.id}/${encodeURIComponent(
                        selectedIndicator.id,
                      )}`,
                    )
                  }
                >
                  بازگشت به نمودار شهرستان‌ها
                </button>
              </div>

              <div className="vkc-chart-grid">
                <div className="vkc-chart-card">
                  <h3>
                    تحقق دوره انتخاب‌شده
                  </h3>

                  <div className="vkc-single-kpi">
                    {pct(
                      achievement(
                        indicatorPeriodValue(
                          selectedIndicator,
                          selectedCounty,
                          period,
                          overrides,
                        ),
                        indicatorTarget(
                          selectedIndicator,
                          selectedCounty,
                          period,
                          overrides,
                        ),
                      ),
                    )}
                  </div>
                </div>

                <div className="vkc-chart-card">
                  <h3>
                    عملکرد در برابر هدف
                  </h3>

                  <div className="vkc-chart">
                    <ResponsiveContainer>
                      <BarChart
                        data={[
                          {
                            name: "هدف",
                            value:
                              indicatorTarget(
                                selectedIndicator,
                                selectedCounty,
                                period,
                                overrides,
                              ) ?? 0,
                          },
                          {
                            name: "عملکرد",
                            value:
                              indicatorPeriodValue(
                                selectedIndicator,
                                selectedCounty,
                                period,
                                overrides,
                              ) ?? 0,
                          },
                        ]}
                      >
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Bar
                          dataKey="value"
                          name="تعداد"
                          fill={COLORS.track}
                        />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>
            </section>
          )}

          {!countyCode && (
            <section className="vkc-panel">
              <div className="vkc-panel-title">
                <div>
                  <h2>
                    عملکرد شهرستان‌ها
                  </h2>
                  <p>
                    کلیک روی هر شهرستان، وارد
                    جزئیات همان شهرستان می‌شود.
                  </p>
                </div>
              </div>

              <div className="vkc-chart">
                <ResponsiveContainer>
                  <BarChart
                    data={countyChart}
                    onClick={(state: any) => {
                      const active =
                        state?.activePayload?.[0]
                          ?.payload;

                      if (active?.county) {
                        navigate(
                          `/gis/kpi/vaccination/categories/${category.id}/${encodeURIComponent(
                            selectedIndicator.id,
                          )}/county/${encodeURIComponent(
                            active.county,
                          )}`,
                        );
                      }
                    }}
                  >
                    <XAxis
                      dataKey="county"
                      interval={0}
                      angle={-35}
                      textAnchor="end"
                      height={100}
                    />
                    <YAxis
                      domain={[0, 100]}
                      tickFormatter={(v) =>
                        `${v}%`
                      }
                    />
                    <Tooltip
                      formatter={(v: any) =>
                        pct(Number(v ?? 0))
                      }
                    />
                    <Bar
                      dataKey="achievement"
                      name="درصد تحقق"
                      cursor="pointer"
                    >
                      {countyChart.map(
                        (entry) => (
                          <Cell
                            key={entry.county}
                            fill={statusColor(
                              statusForAchievement(
                                entry.achievement,
                              ),
                            )}
                          />
                        ),
                      )}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </section>
          )}

          <section className="vkc-panel">
            <div className="vkc-panel-title">
              <div>
                <h2>
                  ورود و اصلاح پیش‌بینی‌های دوره‌ای
                </h2>
                <p>
                  دوره ۴ ماهه از فایل منبع خوانده شده
                  است. مقادیر ۳، ۵ و سالانه قابل ورود
                  هستند و در مرورگر ذخیره می‌شوند.
                </p>
              </div>
            </div>

            <div className="vkc-table-wrap">
              <table className="vkc-table">
                <thead>
                  <tr>
                    <th>شهرستان</th>
                    <th>هدف سالانه منبع</th>
                    <th>هدف ۴ ماهه منبع</th>
                    <th>عملکرد ۴ ماهه منبع</th>
                    <th>هدف ۳ ماهه</th>
                    <th>عملکرد ۳ ماهه</th>
                    <th>هدف ۵ ماهه</th>
                    <th>عملکرد ۵ ماهه</th>
                    <th>هدف سالانه</th>
                    <th>عملکرد سالانه</th>
                  </tr>
                </thead>

                <tbody>
                  {selectedIndicator.rows.map(
                    (row) => {
                      const key =
                        `${selectedIndicator.id}::${row.county}`;

                      const override =
                        overrides[key] ?? {};

                      return (
                        <tr key={key}>
                          <td>
                            <button
                              type="button"
                              className="vkc-link-button"
                              onClick={() =>
                                navigate(
                                  `/gis/kpi/vaccination/categories/${category.id}/${encodeURIComponent(
                                    selectedIndicator.id,
                                  )}/county/${encodeURIComponent(
                                    row.county,
                                  )}`,
                                )
                              }
                            >
                              {row.county}
                            </button>
                          </td>

                          <td>
                            {fmt(
                              row.annualTarget,
                            )}
                          </td>

                          <td>
                            {fmt(
                              row.periodTarget,
                            )}
                          </td>

                          <td>
                            {fmt(row.actual)}
                          </td>

                          <td>
                            <input
                              type="number"
                              value={
                                override.target3 ??
                                ""
                              }
                              onChange={(e) =>
                                saveOverride(
                                  key,
                                  "target3",
                                  e.target.value,
                                )
                              }
                            />
                          </td>

                          <td>
                            <input
                              type="number"
                              value={
                                override.actual3 ??
                                ""
                              }
                              onChange={(e) =>
                                saveOverride(
                                  key,
                                  "actual3",
                                  e.target.value,
                                )
                              }
                            />
                          </td>

                          <td>
                            <input
                              type="number"
                              value={
                                override.target5 ??
                                ""
                              }
                              onChange={(e) =>
                                saveOverride(
                                  key,
                                  "target5",
                                  e.target.value,
                                )
                              }
                            />
                          </td>

                          <td>
                            <input
                              type="number"
                              value={
                                override.actual5 ??
                                ""
                              }
                              onChange={(e) =>
                                saveOverride(
                                  key,
                                  "actual5",
                                  e.target.value,
                                )
                              }
                            />
                          </td>

                          <td>
                            <input
                              type="number"
                              value={
                                override.annualTarget ??
                                row.annualTarget ??
                                ""
                              }
                              onChange={(e) =>
                                saveOverride(
                                  key,
                                  "annualTarget",
                                  e.target.value,
                                )
                              }
                            />
                          </td>

                          <td>
                            <input
                              type="number"
                              value={
                                override.actual12 ??
                                ""
                              }
                              onChange={(e) =>
                                saveOverride(
                                  key,
                                  "actual12",
                                  e.target.value,
                                )
                              }
                            />
                          </td>
                        </tr>
                      );
                    },
                  )}
                </tbody>
              </table>
            </div>
          </section>

          <section className="vkc-panel">
            <div className="vkc-panel-title">
              <div>
                <h2>
                  وضعیت واحدهای شهرستان
                </h2>
                <p>
                  اگر نوع واکسن شاخص در API فعلی پیدا
                  شود، واحدها از همان KPI موجود خوانده
                  می‌شوند.
                </p>
              </div>

              {unitsLoading && (
                <span>در حال دریافت واحدها...</span>
              )}
            </div>

            <div className="vkc-chart-grid">
              <div className="vkc-chart-card">
                <h3>
                  توزیع وضعیت واحدها
                </h3>

                <div className="vkc-chart">
                  {units.length > 0 ? (
                    <ResponsiveContainer>
                      <PieChart>
                        <Pie
                          data={unitStatusData}
                          dataKey="value"
                          nameKey="name"
                          outerRadius={105}
                          label={({ name, value }) =>
                            `${name}: ${value}`
                          }
                          onClick={(entry: any) =>
                            setUnitStatusFilter(
                              entry?.status ?? null,
                            )
                          }
                        >
                          {unitStatusData.map(
                            (entry) => (
                              <Cell
                                key={entry.status}
                                fill={entry.fill}
                                cursor="pointer"
                              />
                            ),
                          )}
                        </Pie>

                        <Tooltip />
                        <Legend />
                      </PieChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="vkc-empty">
                      برای این شاخص هنوز نوع واکسن
                      متناظر در API پیدا نشد.
                    </div>
                  )}
                </div>
              </div>

              <div className="vkc-chart-card">
                <h3>
                  واحدهای باقیمانده
                </h3>

                <div className="vkc-big-number">
                  {fmt(
                    units.filter(
                      (x) =>
                        x.remaining_animals > 0,
                    ).length,
                  )}
                </div>

                <p>
                  واحد دارای دام واکسینه‌نشده
                </p>
              </div>
            </div>

            {unitStatusFilter && (
              <div className="vkc-unit-status-result">
                <h3>
                  جدول واحدهای{" "}
                  {statusLabel(
                    unitStatusFilter,
                  )}
                </h3>

                <div className="vkc-table-wrap">
                  <table className="vkc-table">
                    <thead>
                      <tr>
                        <th>واحد</th>
                        <th>شهرستان</th>
                        <th>نوع واحد</th>
                        <th>کل دام</th>
                        <th>واکسینه</th>
                        <th>باقی‌مانده</th>
                        <th>پوشش</th>
                        <th>وضعیت</th>
                        <th>جزییات</th>
                      </tr>
                    </thead>

                    <tbody>
                      {filteredUnits.map(
                        (unit) => (
                          <tr
                            key={
                              unit.unit_code
                            }
                          >
                            <td>
                              {unit.unit_name}
                            </td>
                            <td>
                              {unit.county_name ||
                                "-"}
                            </td>
                            <td>
                              {unit.unit_type ||
                                "-"}
                            </td>
                            <td>
                              {fmt(
                                unit.total_animals,
                              )}
                            </td>
                            <td>
                              {fmt(
                                unit.vaccinated_animals,
                              )}
                            </td>
                            <td>
                              {fmt(
                                unit.remaining_animals,
                              )}
                            </td>
                            <td>
                              {pct(
                                unit.coverage_percent,
                              )}
                            </td>
                            <td>
                              {statusLabel(
                                unit.status,
                              )}
                            </td>
                            <td>
                              <button
                                type="button"
                                onClick={() =>
                                  navigate(
                                    `/gis/kpi/vaccination/unit/${encodeURIComponent(
                                      unit.unit_code,
                                    )}`,
                                  )
                                }
                              >
                                مشاهده تاریخچه واحد
                              </button>
                            </td>
                          </tr>
                        ),
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </section>
        </>
      )}
    </div>
  );
}