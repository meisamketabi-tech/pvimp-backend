import React, {
  useEffect,
  useMemo,
  useState,
} from "react";

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
import { displayUnitName } from "../utils/display";

import "./VaccinationDashboard.css";


/* =========================================================
   TYPES
   ========================================================= */

type CountyRow = {
  county_code: string | number;
  county_name: string;

  records: number;
  units: number;

  total_animals: number;
  eligible_animals: number;
  vaccinated_animals: number;
  remaining_animals: number;

  coverage_percent: number;

  adverse_events: number;

  status: string;
};


type UnitRow = {
  unit_code: string;
  unit_name: string;

  province_name: string | null;

  county_code: string | number;
  county_name: string | null;

  unit_type: string | null;

  records: number;

  total_animals: number;
  eligible_animals: number;
  vaccinated_animals: number;
  remaining_animals: number;

  coverage_percent: number;

  adverse_events: number;
  adverse_event_rate_percent: number;

  status: string;
  priority: string;
};


type VaccineData = {
  vaccine_type: string;
  vaccine_brand: string | null;

  records: number;

  total_animals: number;
  eligible_animals: number;
  vaccinated_animals: number;
  remaining_animals: number;

  coverage_percent: number;

  adverse_events: number;
  adverse_event_rate_percent: number;
};


type Report = {
  vaccine: VaccineData;

  summary: {
    counties: number;
    units: number;

    completed_units: number;
    incomplete_units: number;

    critical_units: number;
    zero_vaccination_units: number;

    total_remaining_animals: number;
  };

  counties: CountyRow[];

  units: UnitRow[];

  top_priority_counties: CountyRow[];

  top_priority_units: UnitRow[];
};


type PaginationResponse = {
  page: number;
  page_size: number;
  total: number;
  pages: number;
  items: UnitRow[];
};


/* =========================================================
   COLORS
   ========================================================= */

const COLORS = {
  critical: "#dc2626",
  warning: "#f59e0b",
  track: "#2563eb",
  excellent: "#16a34a",
  remaining: "#94a3b8",
};


/* =========================================================
   FORMATTERS
   ========================================================= */

function fmt(value: number) {
  return new Intl.NumberFormat("fa-IR").format(
    Number(value || 0)
  );
}


function pct(value: number) {
  return `${Number(value || 0).toFixed(1)}%`;
}


/* =========================================================
   LABEL HELPERS
   ========================================================= */

function statusLabel(status: string) {
  switch (status) {
    case "NO_COVERAGE":
      return "بدون پوشش";

    case "CRITICAL":
      return "بحرانی";

    case "WARNING":
      return "نیازمند توجه";

    case "ON_TRACK":
      return "در مسیر";

    case "EXCELLENT":
      return "عالی";

    default:
      return status || "-";
  }
}


function priorityLabel(priority: string) {
  switch (priority) {
    case "URGENT":
      return "فوری";

    case "HIGH":
      return "بالا";

    case "MEDIUM":
      return "متوسط";

    case "LOW":
      return "پایین";

    default:
      return priority || "-";
  }
}


function statusColor(status: string) {
  switch (status) {
    case "NO_COVERAGE":
    case "CRITICAL":
      return COLORS.critical;

    case "WARNING":
      return COLORS.warning;

    case "EXCELLENT":
      return COLORS.excellent;

    default:
      return COLORS.track;
  }
}


/* =========================================================
   ERROR HELPERS
   ========================================================= */

function isCanceledError(error: unknown) {
  const err = error as {
    code?: string;
    name?: string;
  } | null;

  return (
    err?.code === "ERR_CANCELED" ||
    err?.name === "CanceledError" ||
    err?.name === "AbortError"
  );
}


/* =========================================================
   NORMALIZERS
   ========================================================= */

function normalizeUnit(unit: Partial<UnitRow>): UnitRow {
  return {
    unit_code: String(
      unit?.unit_code ?? ""
    ),

    unit_name: String(
      unit?.unit_name ?? ""
    ),

    province_name:
      unit?.province_name ?? null,

    county_code:
      unit?.county_code ?? "",

    county_name:
      unit?.county_name ?? null,

    unit_type:
      unit?.unit_type ?? null,

    records:
      Number(
        unit?.records ?? 0
      ),

    total_animals:
      Number(
        unit?.total_animals ?? 0
      ),

    eligible_animals:
      Number(
        unit?.eligible_animals ?? 0
      ),

    vaccinated_animals:
      Number(
        unit?.vaccinated_animals ?? 0
      ),

    remaining_animals:
      Number(
        unit?.remaining_animals ?? 0
      ),

    coverage_percent:
      Number(
        unit?.coverage_percent ?? 0
      ),

    adverse_events:
      Number(
        unit?.adverse_events ?? 0
      ),

    adverse_event_rate_percent:
      Number(
        unit?.adverse_event_rate_percent ?? 0
      ),

    status:
      String(
        unit?.status ?? "CRITICAL"
      ),

    priority:
      String(
        unit?.priority ?? "HIGH"
      ),
  };
}


function normalizeCounty(
  county: Partial<CountyRow>
): CountyRow {
  return {
    county_code:
      county?.county_code ?? "",

    county_name:
      String(
        county?.county_name ?? ""
      ),

    records:
      Number(
        county?.records ?? 0
      ),

    units:
      Number(
        county?.units ?? 0
      ),

    total_animals:
      Number(
        county?.total_animals ?? 0
      ),

    eligible_animals:
      Number(
        county?.eligible_animals ?? 0
      ),

    vaccinated_animals:
      Number(
        county?.vaccinated_animals ?? 0
      ),

    remaining_animals:
      Number(
        county?.remaining_animals ?? 0
      ),

    coverage_percent:
      Number(
        county?.coverage_percent ?? 0
      ),

    adverse_events:
      Number(
        county?.adverse_events ?? 0
      ),

    status:
      String(
        county?.status ?? "CRITICAL"
      ),
  };
}


/* =========================================================
   PAGE
   ========================================================= */

export default function VaccinationVaccineReport() {
  const params =
    useParams<{
      vaccineType?: string;
    }>();

  const navigate =
    useNavigate();


  /*
   * بسیار مهم:
   *
   * vaccineType ممکن است undefined باشد.
   *
   * از اینجا به بعد فقط selectedVaccineType
   * استفاده می‌کنیم.
   */
  const selectedVaccineType =
    params.vaccineType ?? "";


  /* =======================================================
     STATE
     ======================================================= */

  const [
    report,
    setReport,
  ] = useState<Report | null>(null);


  const [
    pageUnits,
    setPageUnits,
  ] = useState<UnitRow[]>([]);


  const [
    unitPage,
    setUnitPage,
  ] = useState<number>(1);


  const [
    unitPageSize,
  ] = useState<number>(50);


  const [
    unitTotal,
    setUnitTotal,
  ] = useState<number>(0);


  const [
    unitTotalPages,
    setUnitTotalPages,
  ] = useState<number>(0);


  const [
    unitsLoading,
    setUnitsLoading,
  ] = useState<boolean>(false);


  const [
    loading,
    setLoading,
  ] = useState<boolean>(true);


  const [
    error,
    setError,
  ] = useState<string>("");


  /* =======================================================
     MAIN MANAGEMENT REPORT
     ======================================================= */

  useEffect(() => {
    if (!selectedVaccineType) {
      setLoading(false);
      setReport(null);
      setError(
        "نوع واکسن مشخص نشده است."
      );

      return;
    }


    const controller =
      new AbortController();


    let mounted = true;


    async function loadReport() {
      try {
        setLoading(true);
        setError("");


        const response =
          await api.get(
            "/api/v1/gis/kpi/vaccination/management-report",
            {
              params: {
                vaccine_type:
                  selectedVaccineType,
              },

              headers: {
                Accept:
                  "application/json",
              },

              signal:
                controller.signal,
            }
          );


        if (!mounted) {
          return;
        }


        const data =
          response.data;


        console.log(
          "[VACCINE MANAGEMENT REPORT]",
          data
        );


        /*
         * پیدا کردن دقیق واکسن انتخاب‌شده
         */
        const vaccineData =
          Array.isArray(
            data?.vaccines
          )
            ? data.vaccines.find(
              (item: VaccineData) =>
                String(
                  item?.vaccine_type ?? ""
                ) ===
                selectedVaccineType
            )
            : null;


        if (!vaccineData) {
          console.error(
            "[VACCINE REPORT] vaccine not found",
            {
              selectedVaccineType,
              vaccines:
                data?.vaccines,
            }
          );


          throw new Error(
            "گزارش این واکسن در سامانه موجود نیست."
          );
        }


        /*
         * شهرستان‌ها
         */
        const countiesData =
          Array.isArray(
            data?.counties
          )
            ? data.counties.map(
              normalizeCounty
            )
            : [];


        /*
         * واحدها
         */
        const unitsData =
          Array.isArray(
            data?.units
          )
            ? data.units.map(
              normalizeUnit
            )
            : [];


        /*
         * تعداد شهرستان
         */
        const totalCounties =
          Number(
            data?.dashboard?.counties ??
            countiesData.length
          );


        /*
         * تعداد واحد
         */
        const totalUnits =
          Number(
            data?.dashboard?.units ??
            unitsData.length
          );


        /*
         * واحدهای بحرانی
         */
        const criticalUnits =
          unitsData.filter(
            (unit: UnitRow) =>
              unit.status ===
              "CRITICAL" ||
              unit.status ===
              "NO_COVERAGE"
          ).length;


        /*
         * واحدهای بدون واکسیناسیون
         */
        const zeroVaccinationUnits =
          unitsData.filter(
            (unit: UnitRow) =>
              Number(
                unit.vaccinated_animals
              ) === 0
          ).length;


        /*
         * واحدهای تکمیل‌شده
         */
        const completedUnits =
          unitsData.filter(
            (unit: UnitRow) =>
              Number(
                unit.coverage_percent
              ) >= 90
          ).length;


        /*
         * واحدهای ناقص
         */
        const incompleteUnits =
          Math.max(
            totalUnits -
            completedUnits,
            0
          );


        /*
         * دام باقی‌مانده
         *
         * اولویت با dashboard backend
         */
        const totalRemainingAnimals =
          Number(
            data?.dashboard
              ?.remaining_animals ??
            vaccineData
              ?.remaining_animals ??
            Math.max(
              Number(
                vaccineData
                  ?.total_animals ??
                0
              ) -
              Number(
                vaccineData
                  ?.vaccinated_animals ??
                0
              ),
              0
            )
          );


        /*
         * گزارش نهایی
         */
        const normalizedReport:
          Report = {
          vaccine: {
            vaccine_type:
              String(
                vaccineData
                  ?.vaccine_type ??
                selectedVaccineType
              ),

            vaccine_brand:
              vaccineData
                ?.vaccine_brand ??
              null,

            records:
              Number(
                vaccineData
                  ?.records ??
                0
              ),

            total_animals:
              Number(
                vaccineData
                  ?.total_animals ??
                0
              ),

            eligible_animals:
              Number(
                vaccineData
                  ?.eligible_animals ??
                0
              ),

            vaccinated_animals:
              Number(
                vaccineData
                  ?.vaccinated_animals ??
                0
              ),

            remaining_animals:
              Number(
                vaccineData
                  ?.remaining_animals ??
                0
              ),

            coverage_percent:
              Number(
                vaccineData
                  ?.coverage_percent ??
                0
              ),

            adverse_events:
              Number(
                vaccineData
                  ?.adverse_events ??
                0
              ),

            adverse_event_rate_percent:
              Number(
                vaccineData
                  ?.adverse_event_rate_percent ??
                0
              ),
          },


          summary: {
            counties:
              totalCounties,

            units:
              totalUnits,

            completed_units:
              completedUnits,

            incomplete_units:
              incompleteUnits,

            critical_units:
              criticalUnits,

            zero_vaccination_units:
              zeroVaccinationUnits,

            total_remaining_animals:
              totalRemainingAnimals,
          },


          counties:
            countiesData,


          units:
            unitsData,


          top_priority_counties:
            [...countiesData]
              .sort(
                (a, b) =>
                  Number(
                    b.remaining_animals
                  ) -
                  Number(
                    a.remaining_animals
                  )
              )
              .slice(0, 5),


          top_priority_units:
            [...unitsData]
              .sort(
                (a, b) =>
                  Number(
                    b.remaining_animals
                  ) -
                  Number(
                    a.remaining_animals
                  )
              )
              .slice(0, 10),
        };


        console.log(
          "[NORMALIZED VACCINE REPORT]",
          normalizedReport
        );


        setReport(
          normalizedReport
        );

        setError("");


      } catch (err: unknown) {
        if (
          isCanceledError(err)
        ) {
          return;
        }


        if (!mounted) {
          return;
        }


        const errorObject =
          err as {
            response?: {
              data?: {
                detail?: string;
              };
            };
            message?: string;
          };


        console.error(
          "[VACCINE REPORT ERROR]",
          err
        );


        setReport(null);


        setError(
          errorObject
            ?.response
            ?.data
            ?.detail ||
          errorObject
            ?.message ||
          "خطا در دریافت گزارش واکسن"
        );


      } finally {
        if (
          mounted &&
          !controller.signal.aborted
        ) {
          setLoading(false);
        }
      }
    }


    loadReport();


    return () => {
      mounted = false;
      controller.abort();
    };

  }, [
    selectedVaccineType,
  ]);


  /* =======================================================
     PAGINATED UNITS
     ======================================================= */

  useEffect(() => {
    if (!selectedVaccineType) {
      setPageUnits([]);
      setUnitTotal(0);
      setUnitTotalPages(0);

      return;
    }


    const controller =
      new AbortController();


    let mounted = true;


    async function loadPaginatedUnits() {
      try {
        setUnitsLoading(true);


        /*
         * نکته مهم:
         *
         * selectedVaccineType حتماً string است.
         *
         * بنابراین دیگر خطای:
         *
         * string | undefined
         *
         * نداریم.
         */
        const encodedVaccineType =
          encodeURIComponent(
            selectedVaccineType
          );


        const response =
          await api.get(
            `/api/v1/gis/kpi/vaccination/vaccine/${encodedVaccineType}/units-paginated`,
            {
              params: {
                page:
                  unitPage,

                page_size:
                  unitPageSize,
              },

              headers: {
                Accept:
                  "application/json",
              },

              signal:
                controller.signal,
            }
          );


        if (!mounted) {
          return;
        }


        const rawData =
          response.data;


        console.log(
          "[VACCINE PAGINATION RESPONSE]",
          rawData
        );


        const data:
          PaginationResponse = {
          page:
            Number(
              rawData?.page ?? 1
            ),

          page_size:
            Number(
              rawData?.page_size ??
              unitPageSize
            ),

          total:
            Number(
              rawData?.total ?? 0
            ),

          pages:
            Number(
              rawData?.pages ?? 0
            ),

          items:
            Array.isArray(
              rawData?.items
            )
              ? rawData.items.map(
                normalizeUnit
              )
              : [],
        };


        setPageUnits(
          data.items
        );


        setUnitTotal(
          data.total
        );


        setUnitTotalPages(
          data.pages
        );


      } catch (err: unknown) {
        if (
          isCanceledError(err)
        ) {
          return;
        }


        if (!mounted) {
          return;
        }


        console.error(
          "[VACCINE PAGINATION ERROR]",
          err
        );


        setPageUnits([]);

        setUnitTotal(0);

        setUnitTotalPages(0);


      } finally {
        if (mounted) {
          setUnitsLoading(false);
        }
      }
    }


    loadPaginatedUnits();


    return () => {
      mounted = false;
      controller.abort();
    };

  }, [
    selectedVaccineType,
    unitPage,
    unitPageSize,
  ]);


  /* =======================================================
     CHART DATA
     ======================================================= */

  const unitStatusData =
    useMemo(() => {
      if (!report) {
        return [];
      }


      return [
        {
          name: "بحرانی",

          value:
            report.summary
              .critical_units,

          fill:
            COLORS.critical,
        },

        {
          name:
            "نیازمند توجه",

          value:
            Math.max(
              report.summary
                .incomplete_units -
              report.summary
                .critical_units,
              0
            ),

          fill:
            COLORS.warning,
        },

        {
          name:
            "تکمیل شده",

          value:
            report.summary
              .completed_units,

          fill:
            COLORS.excellent,
        },
      ].filter(
        (item) =>
          item.value > 0
      );

    }, [
      report,
    ]);


  const countyChart =
    useMemo(
      () =>
        (
          report?.counties ||
          []
        ).map(
          (county) => ({
            countyCode:
              county.county_code,

            name:
              county.county_name,

            coverage:
              Number(
                county.coverage_percent ||
                0
              ),
          })
        ),

      [
        report,
      ]
    );


  const remainingByCounty =
    useMemo(
      () =>
        [
          ...(report?.counties ||
            []),
        ]
          .sort(
            (a, b) =>
              Number(
                b.remaining_animals ||
                0
              ) -
              Number(
                a.remaining_animals ||
                0
              )
          )
          .map(
            (county) => ({
              countyCode:
                county.county_code,

              name:
                county.county_name,

              remaining:
                Number(
                  county.remaining_animals ||
                  0
                ),
            })
          ),

      [
        report,
      ]
    );


  /* =======================================================
     LOADING
     ======================================================= */

  if (loading) {
    return (
      <div
        className="dashboard-page vaccination-command-center"
        dir="rtl"
      >
        <div className="panel">
          <h2>
            در حال دریافت گزارش واکسن...
          </h2>
        </div>
      </div>
    );
  }


  /* =======================================================
     ERROR
     ======================================================= */

  if (
    error ||
    !report
  ) {
    return (
      <div
        className="dashboard-page vaccination-command-center"
        dir="rtl"
      >
        <div className="panel">
          <h2>
            خطا
          </h2>

          <p>
            {error ||
              "گزارش موجود نیست."}
          </p>

          <button
            type="button"
            onClick={() =>
              navigate(
                "/gis/kpi/vaccination"
              )
            }
          >
            بازگشت
          </button>
        </div>
      </div>
    );
  }


  /* =======================================================
     MAIN PAGE
     ======================================================= */

  return (
    <div
      className="dashboard-page vaccination-command-center"
      dir="rtl"
    >

      {/* =================================================
          HEADER
          ================================================= */}

      <div className="dashboard-header">

        <button
          type="button"
          onClick={() =>
            navigate(
              "/gis/kpi/vaccination"
            )
          }
        >
          بازگشت به KPI واکسیناسیون
        </button>


        <h1>
          گزارش مدیریتی واکسن{" "}
          {
            report.vaccine
              .vaccine_type
          }
        </h1>


        <p>
          برند:{" "}
          {
            report.vaccine
              .vaccine_brand ||
            "-"
          }
        </p>

      </div>


      {/* =================================================
          KPI CARDS
          ================================================= */}

      <div className="kpi-grid">

        <div className="kpi-card">

          <div className="kpi-title">
            درصد پوشش واکسیناسیون
          </div>

          <div
            className="kpi-value"
            style={{
              color:
                statusColor(
                  report
                    .vaccine
                    .coverage_percent <
                    50
                    ? "CRITICAL"
                    : report
                      .vaccine
                      .coverage_percent <
                      75
                      ? "WARNING"
                      : report
                        .vaccine
                        .coverage_percent >=
                        90
                        ? "EXCELLENT"
                        : "ON_TRACK"
                ),
            }}
          >
            {
              pct(
                report
                  .vaccine
                  .coverage_percent
              )
            }
          </div>

        </div>


        <div className="kpi-card">

          <div className="kpi-title">
            کل دام هدف
          </div>

          <div className="kpi-value">
            {
              fmt(
                report
                  .vaccine
                  .total_animals
              )
            }
          </div>

        </div>


        <div className="kpi-card">

          <div className="kpi-title">
            دام واکسینه شده
          </div>

          <div className="kpi-value">
            {
              fmt(
                report
                  .vaccine
                  .vaccinated_animals
              )
            }
          </div>

        </div>


        <div className="kpi-card">

          <div className="kpi-title">
            باقی مانده
          </div>

          <div className="kpi-value">
            {
              fmt(
                report.summary
                  .total_remaining_animals
              )
            }
          </div>

        </div>


        <div className="kpi-card">

          <div className="kpi-title">
            شهرستان‌ها
          </div>

          <div className="kpi-value">
            {
              fmt(
                report.summary
                  .counties
              )
            }
          </div>

        </div>


        <div className="kpi-card">

          <div className="kpi-title">
            واحدهای دامپزشکی
          </div>

          <div className="kpi-value">
            {
              fmt(
                report.summary
                  .units
              )
            }
          </div>

        </div>


        <div className="kpi-card">

          <div className="kpi-title">
            واحد بحرانی
          </div>

          <div className="kpi-value">
            {
              fmt(
                report.summary
                  .critical_units
              )
            }
          </div>

        </div>


        <div className="kpi-card">

          <div className="kpi-title">
            واحد بدون واکسیناسیون
          </div>

          <div className="kpi-value">
            {
              fmt(
                report.summary
                  .zero_vaccination_units
              )
            }
          </div>

        </div>


        <div className="kpi-card">

          <div className="kpi-title">
            عوارض ثبت شده
          </div>

          <div className="kpi-value">
            {
              fmt(
                report.vaccine
                  .adverse_events
              )
            }
          </div>

        </div>

      </div>


      {/* =================================================
          CHARTS
          ================================================= */}

      <div
        className="dashboard-grid"
        style={{
          marginTop: 24,

          gridTemplateColumns:
            "repeat(auto-fit, minmax(420px, 1fr))",
        }}
      >

        {/* UNIT STATUS */}

        <div className="dashboard-panel">

          <h2>
            وضعیت واحدهای واکسیناسیون
          </h2>

          <div
            style={{
              width: "100%",
              height: 320,
            }}
          >

            <ResponsiveContainer>

              <PieChart>

                <Pie
                  data={
                    unitStatusData
                  }

                  dataKey="value"

                  nameKey="name"

                  cx="50%"

                  cy="50%"

                  outerRadius={105}

                  label={({
                    name,
                    value,
                  }) =>
                    `${name}: ${value}`
                  }
                >

                  {
                    unitStatusData.map(
                      (entry) => (
                        <Cell
                          key={
                            entry.name
                          }

                          fill={
                            entry.fill
                          }
                        />
                      )
                    )
                  }

                </Pie>

                <Tooltip />

                <Legend />

              </PieChart>

            </ResponsiveContainer>

          </div>

        </div>


        {/* COUNTY COVERAGE */}

        <div className="dashboard-panel">

          <h2>
            درصد پوشش شهرستان‌ها
          </h2>

          <div
            style={{
              width: "100%",
              height: 320,
            }}
          >

            <ResponsiveContainer>

              <BarChart
                data={
                  countyChart
                }
              >

                <XAxis
                  dataKey="name"

                  angle={-35}

                  textAnchor="end"

                  interval={0}

                  height={90}
                />


                <YAxis
                  domain={[
                    0,
                    100,
                  ]}

                  tickFormatter={
                    (value) =>
                      `${value}%`
                  }
                />


                <Tooltip
                  formatter={
                    (value) =>
                      pct(
                        Number(
                          value || 0
                        )
                      )
                  }
                />


                <Bar
                  dataKey="coverage"

                  name="پوشش"
                >

                  {
                    countyChart.map(
                      (entry) => (
                        <Cell
                          key={
                            String(
                              entry.countyCode
                            )
                          }

                          fill={
                            entry.coverage <
                              50
                              ? COLORS.critical
                              : entry.coverage <
                                75
                                ? COLORS.warning
                                : COLORS.excellent
                          }

                          cursor="pointer"

                          onClick={() =>
                            navigate(
                              `/gis/kpi/vaccination/drilldown/county/${entry.countyCode}`
                            )
                          }
                        />
                      )
                    )
                  }

                </Bar>

              </BarChart>

            </ResponsiveContainer>

          </div>

        </div>

      </div>


      {/* =================================================
          COUNTIES
          ================================================= */}

      <div
        className="dashboard-panel"
        style={{
          marginTop: 24,
        }}
      >

        <h2>
          گزارش شهرستان‌های واکسیناسیون
        </h2>


        <div
          style={{
            overflowX:
              "auto",
          }}
        >

          <table
            style={{
              width:
                "100%",

              borderCollapse:
                "collapse",
            }}
          >

            <thead>

              <tr>

                <th>
                  شهرستان
                </th>

                <th>
                  کل دام
                </th>

                <th>
                  واکسینه شده
                </th>

                <th>
                  باقی‌مانده
                </th>

                <th>
                  پوشش
                </th>

                <th>
                  واحدها
                </th>

                <th>
                  عوارض
                </th>

                <th>
                  وضعیت
                </th>

              </tr>

            </thead>


            <tbody>

              {
                report.counties.map(
                  (county) => (
                    <tr
                      key={
                        String(
                          county.county_code
                        )
                      }

                      onClick={() =>
                        navigate(
                          `/gis/kpi/vaccination/drilldown/county/${county.county_code}`
                        )
                      }

                      style={{
                        cursor:
                          "pointer",

                        borderTop:
                          "1px solid #ddd",
                      }}
                    >

                      <td>
                        {
                          county.county_name
                        }
                      </td>

                      <td>
                        {
                          fmt(
                            county.total_animals
                          )
                        }
                      </td>

                      <td>
                        {
                          fmt(
                            county.vaccinated_animals
                          )
                        }
                      </td>

                      <td>
                        {
                          fmt(
                            county.remaining_animals
                          )
                        }
                      </td>

                      <td>
                        {
                          pct(
                            county.coverage_percent
                          )
                        }
                      </td>

                      <td>
                        {
                          fmt(
                            county.units
                          )
                        }
                      </td>

                      <td>
                        {
                          fmt(
                            county.adverse_events
                          )
                        }
                      </td>

                      <td>
                        {
                          statusLabel(
                            county.status
                          )
                        }
                      </td>

                    </tr>
                  )
                )
              }

            </tbody>

          </table>

        </div>


        <p
          style={{
            marginTop: 12,
          }}
        >
          برای مشاهده جزئیات بیشتر روی هر شهرستان کلیک کنید.
        </p>

      </div>


      {/* =================================================
          REMAINING BY COUNTY
          ================================================= */}

      <div
        className="dashboard-panel"
        style={{
          marginTop: 24,
        }}
      >

        <h2>
          شهرستان‌های دارای بیشترین دام باقی‌مانده
        </h2>


        <div
          style={{
            width:
              "100%",

            height:
              380,
          }}
        >

          <ResponsiveContainer>

            <BarChart
              data={
                remainingByCounty
              }

              layout="vertical"

              margin={{
                left: 20,
                right: 40,
                top: 20,
                bottom: 20,
              }}
            >

              <XAxis
                type="number"
              />


              <YAxis
                type="category"

                dataKey="name"

                width={130}
              />


              <Tooltip
                formatter={
                  (value) =>
                    fmt(
                      Number(
                        value || 0
                      )
                    )
                }
              />


              <Bar
                dataKey="remaining"

                name="دام باقی‌مانده"
              >

                {
                  remainingByCounty.map(
                    (entry) => (
                      <Cell
                        key={
                          String(
                            entry.countyCode
                          )
                        }

                        fill={
                          COLORS.remaining
                        }

                        cursor="pointer"

                        onClick={() =>
                          navigate(
                            `/gis/kpi/vaccination/drilldown/county/${entry.countyCode}`
                          )
                        }
                      />
                    )
                  )
                }

              </Bar>

            </BarChart>

          </ResponsiveContainer>

        </div>

      </div>


      {/* =================================================
          PRIORITY UNITS
          ================================================= */}

      <div
        className="dashboard-panel"
        style={{
          marginTop: 24,
        }}
      >

        <h2>
          واحدهای دارای اولویت اقدام
        </h2>


        <div
          style={{
            overflowX:
              "auto",
          }}
        >

          <table
            style={{
              width:
                "100%",

              borderCollapse:
                "collapse",
            }}
          >

            <thead>

              <tr>

                <th>
                  اولویت
                </th>

                <th>
                  شهرستان
                </th>

                <th>
                  واحد
                </th>

                <th>
                  کل دام
                </th>

                <th>
                  واکسینه
                </th>

                <th>
                  باقی‌مانده
                </th>

                <th>
                  پوشش
                </th>

                <th>
                  وضعیت
                </th>

              </tr>

            </thead>


            <tbody>

              {
                report.top_priority_units.map(
                  (unit) => (
                    <tr
                      key={
                        unit.unit_code
                      }

                      onClick={() =>
                        navigate(
                          `/gis/kpi/vaccination/unit/${unit.unit_code}`
                        )
                      }

                      style={{
                        cursor:
                          "pointer",

                        borderTop:
                          "1px solid #ddd",
                      }}
                    >

                      <td>
                        {
                          priorityLabel(
                            unit.priority
                          )
                        }
                      </td>

                      <td>
                        {
                          unit.county_name ||
                          "-"
                        }
                      </td>

                      <td>
                        {
                          displayUnitName(
                            unit.unit_name
                          )
                        }
                      </td>

                      <td>
                        {
                          fmt(
                            unit.total_animals
                          )
                        }
                      </td>

                      <td>
                        {
                          fmt(
                            unit.vaccinated_animals
                          )
                        }
                      </td>

                      <td>
                        {
                          fmt(
                            unit.remaining_animals
                          )
                        }
                      </td>

                      <td>
                        {
                          pct(
                            unit.coverage_percent
                          )
                        }
                      </td>

                      <td>
                        {
                          statusLabel(
                            unit.status
                          )
                        }
                      </td>

                    </tr>
                  )
                )
              }

            </tbody>

          </table>

        </div>

      </div>


      {/* =================================================
          PAGINATED UNITS
          ================================================= */}

      <div
        className="dashboard-panel"
        style={{
          marginTop: 24,
        }}
      >

        <h2>
          فهرست کامل واحدهای واکسیناسیون
        </h2>


        <div
          style={{
            display:
              "flex",

            gap:
              12,

            flexWrap:
              "wrap",

            alignItems:
              "center",

            marginBottom:
              16,
          }}
        >

          <strong>
            تعداد کل واحدها:{" "}
            {fmt(unitTotal)}
          </strong>


          <span>
            صفحه{" "}
            {fmt(unitPage)}
            {" "}
            از{" "}
            {fmt(unitTotalPages)}
          </span>


          {
            unitsLoading && (
              <span>
                در حال دریافت اطلاعات...
              </span>
            )
          }

        </div>


        <div
          style={{
            overflowX:
              "auto",
          }}
        >

          <table
            style={{
              width:
                "100%",

              borderCollapse:
                "collapse",
            }}
          >

            <thead>

              <tr>

                <th>
                  کد
                </th>

                <th>
                  واحد
                </th>

                <th>
                  شهرستان
                </th>

                <th>
                  کل دام
                </th>

                <th>
                  واکسینه
                </th>

                <th>
                  باقی‌مانده
                </th>

                <th>
                  پوشش
                </th>

                <th>
                  اولویت
                </th>

                <th>
                  وضعیت
                </th>

              </tr>

            </thead>


            <tbody>

              {
                pageUnits.map(
                  (unit) => (
                    <tr
                      key={
                        unit.unit_code
                      }

                      onClick={() =>
                        navigate(
                          `/gis/kpi/vaccination/unit/${unit.unit_code}`
                        )
                      }

                      style={{
                        cursor:
                          "pointer",

                        borderTop:
                          "1px solid #ddd",
                      }}
                    >

                      <td>
                        {
                          unit.unit_code
                        }
                      </td>

                      <td>
                        {
                          displayUnitName(
                            unit.unit_name
                          )
                        }
                      </td>

                      <td>
                        {
                          unit.county_name ||
                          "-"
                        }
                      </td>

                      <td>
                        {
                          fmt(
                            unit.total_animals
                          )
                        }
                      </td>

                      <td>
                        {
                          fmt(
                            unit.vaccinated_animals
                          )
                        }
                      </td>

                      <td>
                        {
                          fmt(
                            unit.remaining_animals
                          )
                        }
                      </td>

                      <td>
                        {
                          pct(
                            unit.coverage_percent
                          )
                        }
                      </td>

                      <td>
                        {
                          priorityLabel(
                            unit.priority
                          )
                        }
                      </td>

                      <td>
                        {
                          statusLabel(
                            unit.status
                          )
                        }
                      </td>

                    </tr>
                  )
                )
              }

            </tbody>

          </table>

        </div>


        {
          !unitsLoading &&
          pageUnits.length === 0 && (
            <p
              style={{
                marginTop:
                  16,
              }}
            >
              اطلاعاتی برای نمایش وجود ندارد.
            </p>
          )
        }


        {/* PAGINATION */}

        <div
          style={{
            display:
              "flex",

            justifyContent:
              "center",

            alignItems:
              "center",

            gap:
              12,

            marginTop:
              20,

            flexWrap:
              "wrap",
          }}
        >

          <button
            type="button"

            disabled={
              unitsLoading ||
              unitPage <= 1
            }

            onClick={() =>
              setUnitPage(
                (page) =>
                  Math.max(
                    page - 1,
                    1
                  )
              )
            }
          >
            قبلی
          </button>


          <span>
            {fmt(unitPage)}
            {" / "}
            {fmt(unitTotalPages)}
          </span>


          <button
            type="button"

            disabled={
              unitsLoading ||
              unitTotalPages <= 0 ||
              unitPage >=
              unitTotalPages
            }

            onClick={() =>
              setUnitPage(
                (page) =>
                  Math.min(
                    page + 1,
                    unitTotalPages
                  )
              )
            }
          >
            بعدی
          </button>


          <button
            type="button"

            disabled={
              unitsLoading ||
              unitPage <= 1
            }

            onClick={() =>
              setUnitPage(1)
            }
          >
            صفحه اول
          </button>


          <button
            type="button"

            disabled={
              unitsLoading ||
              unitTotalPages <= 0 ||
              unitPage >=
              unitTotalPages
            }

            onClick={() =>
              setUnitPage(
                unitTotalPages ||
                1
              )
            }
          >
            صفحه آخر
          </button>

        </div>

      </div>


      {/* =================================================
          AI BOX
          ================================================= */}

      <div
        className="panel ai-box"
        style={{
          marginTop: 24,
        }}
      >

        <h2>
          تحلیل هوشمند واکسیناسیون
        </h2>


        <p>
          بر اساس اطلاعات ثبت شده در{" "}
          {fmt(
            report.summary
              .counties
          )}
          {" "}
          شهرستان و{" "}
          {fmt(
            report.summary
              .units
          )}
          {" "}
          واحد، وضعیت واکسیناسیون این واکسن بررسی شده است.
        </p>


        <p>
          میزان پوشش کلی:
          {" "}
          <strong>
            {
              pct(
                report.vaccine
                  .coverage_percent
              )
            }
          </strong>
          {" "}
          و تعداد دام باقی‌مانده:
          {" "}
          <strong>
            {
              fmt(
                report.summary
                  .total_remaining_animals
              )
            }
          </strong>
          {" "}
          رأس می‌باشد.
        </p>


        <p>
          تعداد واحدهای بحرانی:
          {" "}
          <strong>
            {
              fmt(
                report.summary
                  .critical_units
              )
            }
          </strong>
          {" "}
          واحد است و نیاز به بررسی و اقدام اصلاحی دارد.
        </p>


        <p>
          پیشنهاد مدیریتی:
          {" "}
          واحدهای دارای اولویت بالا ابتدا بررسی شوند،
          سپس برای شهرستان‌هایی که بیشترین دام باقی‌مانده دارند
          برنامه تکمیلی واکسیناسیون اجرا گردد.
        </p>

      </div>

    </div>
  );
}