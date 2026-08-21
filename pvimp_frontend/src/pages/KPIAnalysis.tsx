import { getToken } from "../utils/token";
import React, { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
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
import "./Dashboard.css";

type VaccinationUnit = {
  unit_code: string;
  unit_name: string;
  province_name: string | null;
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
};

type CountyKpi = {
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
  adverse_event_rate_percent: number;
  status: string;
};

type VaccineKpi = {
  vaccine_type: string | null;
  vaccine_brand: string | null;
  records: number;
  total_animals: number;
  eligible_animals: number;
  vaccinated_animals: number;
  coverage_percent: number;
  adverse_events: number;
  adverse_event_rate_percent: number;
};

type DashboardKpi = {
  records: number;
  total_animals: number;
  eligible_animals: number;
  vaccinated_animals: number;
  coverage_percent: number;
  remaining_animals: number;
  counties: number;
  units: number;
  vaccine_types: number;
  adverse_events: number;
  adverse_event_rate_percent: number;
  side_effects: {
    shock: number;
    death_or_culling: number;
    abortion: number;
    hypersensitivity: number;
    local_complication: number;
  };
};

const API_BASE =
  "http://127.0.0.1:8000/api/v1";

function formatNumber(value: number) {
  return new Intl.NumberFormat("fa-IR").format(value ?? 0);
}

function statusOf(coverage: number) {
  if (coverage < 50) return "بحرانی";
  if (coverage < 75) return "نیازمند بهبود";
  if (coverage < 90) return "قابل قبول";
  return "مطلوب";
}

function statusClass(coverage: number) {
  if (coverage < 50) return "kpi-danger";
  if (coverage < 75) return "kpi-warning";
  return "kpi-success";
}

const CHART_COLORS = {
  critical: "#dc2626",
  warning: "#f59e0b",
  onTrack: "#16a34a",
  vaccinated: "#2563eb",
  remaining: "#94a3b8",
};
export default function KPIAnalysis() {
  const { type } = useParams();
  const navigate = useNavigate();

  const [units, setUnits] = useState<VaccinationUnit[]>([]);
  const [counties, setCounties] = useState<CountyKpi[]>([]);
  const [vaccines, setVaccines] = useState<VaccineKpi[]>([]);
  const [dashboard, setDashboard] =
    useState<DashboardKpi | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  useEffect(() => {
    if (type && type !== "vaccination") {
      return;
    }

    const controller =
      new AbortController();

    async function getJson<T>(
      url: string
    ): Promise<T> {

      const token = getToken();

      const response =
        await fetch(url, {
          method: "GET",
          headers: {
            Accept:
              "application/json",
            Authorization:
              `Bearer ${token}`,
          },
          signal:
            controller.signal,
        });

      if (!response.ok) {
        throw new Error(
          `HTTP ${response.status}`
        );
      }

      return response.json();
    }


    async function load() {
      try {

        setLoading(true);
        setError("");

        const [
          dashboardData,
          unitsData,
          countiesData,
          vaccinesData,
        ] =
          await Promise.all([
            getJson<DashboardKpi>(
              `${API_BASE}/gis/kpi/vaccination/dashboard`
            ),

            getJson<VaccinationUnit[]>(
              `${API_BASE}/gis/kpi/vaccination/units`
            ),

            getJson<CountyKpi[]>(
              `${API_BASE}/gis/kpi/vaccination/counties`
            ),

            getJson<VaccineKpi[]>(
              `${API_BASE}/gis/kpi/vaccination/vaccines`
            ),
          ]);


        setDashboard(
          dashboardData
        );

        setUnits(
          Array.isArray(unitsData)
            ? unitsData
            : []
        );

        setCounties(
          Array.isArray(countiesData)
            ? countiesData
            : []
        );

        setVaccines(
          Array.isArray(vaccinesData)
            ? vaccinesData
            : []
        );


      } catch (err: any) {

        if (
          err?.name !==
          "AbortError"
        ) {
          setError(
            "Failed to load vaccination KPI data."
          );
        }

      } finally {

        setLoading(false);

      }
    }


    load();


    return () =>
      controller.abort();

  }, [type]);



  const summary = useMemo(() => {

    if (dashboard) {

      return {
        totalAnimals:
          dashboard.total_animals,

        vaccinatedAnimals:
          dashboard.vaccinated_animals,

        remainingAnimals:
          dashboard.remaining_animals,

        adverseEvents:
          dashboard.adverse_events,

        coverage:
          dashboard.coverage_percent,
      };
    }


    const totalAnimals =
      units.reduce(
        (sum, item) =>
          sum +
          (item.total_animals || 0),
        0
      );


    const vaccinatedAnimals =
      units.reduce(
        (sum, item) =>
          sum +
          (item.vaccinated_animals || 0),
        0
      );


    const remainingAnimals =
      units.reduce(
        (sum, item) =>
          sum +
          (item.remaining_animals || 0),
        0
      );


    const adverseEvents =
      units.reduce(
        (sum, item) =>
          sum +
          (item.adverse_events || 0),
        0
      );


    const coverage =
      totalAnimals > 0
        ? (
          vaccinatedAnimals /
          totalAnimals
        ) * 100
        : 0;


    return {
      totalAnimals,
      vaccinatedAnimals,
      remainingAnimals,
      adverseEvents,
      coverage,
    };


  }, [
    dashboard,
    units,
  ]);
  const unitStatusData = useMemo(() => {

    let critical = 0;
    let warning = 0;
    let onTrack = 0;


    units.forEach((unit) => {

      const coverage =
        Number(
          unit.coverage_percent || 0
        );


      if (coverage < 50) {
        critical++;
      }
      else if (coverage < 75) {
        warning++;
      }
      else {
        onTrack++;
      }

    });


    return [

      {
        name: "بحرانی",
        value: critical,
        fill:
          CHART_COLORS.critical,
      },

      {
        name:
          "نیازمند بهبود",
        value: warning,
        fill:
          CHART_COLORS.warning,
      },

      {
        name:
          "مطلوب",
        value: onTrack,
        fill:
          CHART_COLORS.onTrack,
      },

    ];

  }, [units]);



  const vaccinationSplitData =
    useMemo(
      () => [

        {
          name:
            "واحدهای واکسینه شده",
          value:
            summary.vaccinatedAnimals,
          fill:
            CHART_COLORS.vaccinated,
        },

        {
          name:
            "باقی‌مانده",
          value:
            summary.remainingAnimals,
          fill:
            CHART_COLORS.remaining,
        },

      ],
      [summary]
    );



  const countyChartData =
    useMemo(
      () =>

        counties.map(
          (county) => ({

            countyCode:
              county.county_code,

            name:
              county.county_name ||
              String(
                county.county_code
              ),

            coverage:
              Number(
                county.coverage_percent || 0
              ),

          })

        ),

      [counties]
    );



  const vaccineChartData =
    useMemo(
      () =>

        vaccines.map(
          (vaccine) => ({

            vaccineType:
              vaccine.vaccine_type ||
              "-",

            vaccineBrand:
              vaccine.vaccine_brand ||
              "-",

            coverage:
              Number(
                vaccine.coverage_percent || 0
              ),

            vaccinated:
              Number(
                vaccine.vaccinated_animals || 0
              ),

            adverseEvents:
              Number(
                vaccine.adverse_events || 0
              ),

          })

        ),

      [vaccines]
    );



  const topUnitCoverageData =
    useMemo(

      () =>

        [...units]

          .sort(
            (a, b) =>
              Number(
                a.coverage_percent || 0
              ) -
              Number(
                b.coverage_percent || 0
              )
          )

          .slice(0, 15)

          .map(
            (unit) => ({

              unitCode:
                unit.unit_code,

              name:
                unit.unit_name,

              coverage:
                Number(
                  unit.coverage_percent || 0
                ),

            })

          ),

      [units]

    );



  if (
    type &&
    type !== "vaccination"
  ) {

    return (

      <div
        className="dashboard-page"
        dir="rtl"
      >

        <div
          className="dashboard-header"
        >

          <h1>
            KPI
          </h1>

          <p>
            Selected KPI type is not supported.
          </p>

        </div>

      </div>

    );

  }

  return (
    <div
      className="dashboard-page"
      dir="rtl"
    >

      <div className="dashboard-header">

        <h1>
          تحلیل KPI واکسیناسیون
        </h1>

        <p>
          داشبورد مدیریتی شاخص‌های کلیدی
          پوشش واکسیناسیون و عملکرد واحدها
        </p>

      </div>



      {loading && (

        <div className="panel">

          <h2>
            در حال دریافت اطلاعات...
          </h2>

        </div>

      )}



      {error && (

        <div className="panel">

          <h2>
            خطا
          </h2>

          <p>
            {error}
          </p>

        </div>

      )}



      {!loading &&
        !error && (

          <>

            <div className="kpi-grid">


              <div className="kpi-card">

                <div className="kpi-title">
                  درصد پوشش واکسیناسیون
                </div>

                <div
                  className={
                    `kpi-value ${statusClass(
                      summary.coverage
                    )
                    }`
                  }
                >

                  {
                    summary.coverage.toFixed(1)
                  }%

                </div>

                <div>
                  {
                    statusOf(
                      summary.coverage
                    )
                  }
                </div>

              </div>



              <div className="kpi-card">

                <div className="kpi-title">
                  کل دام‌ها
                </div>

                <div className="kpi-value">

                  {
                    formatNumber(
                      summary.totalAnimals
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
                    formatNumber(
                      summary.vaccinatedAnimals
                    )
                  }

                </div>

              </div>



              <div className="kpi-card">

                <div className="kpi-title">
                  دام باقی‌مانده
                </div>

                <div className="kpi-value">

                  {
                    formatNumber(
                      summary.remainingAnimals
                    )
                  }

                </div>

              </div>



              <div className="kpi-card">

                <div className="kpi-title">
                  تعداد واحدها
                </div>

                <div className="kpi-value">

                  {
                    formatNumber(
                      units.length
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
                    formatNumber(
                      summary.adverseEvents
                    )
                  }

                </div>

              </div>


            </div>
            <div
              className="dashboard-grid"
              style={{
                marginTop: 24,
                gridTemplateColumns:
                  "repeat(auto-fit,minmax(420px,1fr))",
              }}
            >


              <div className="dashboard-panel">

                <h2>
                  وضعیت عملکرد واحدها
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

                        label={
                          ({
                            name,
                            value,
                          }) =>
                            `${name}: ${value}`
                        }


                        onClick={
                          (data: any) => {

                            const name =
                              data?.name ??
                              data?.payload?.name;


                            if (
                              name ===
                              "بحرانی"
                            ) {

                              navigate(
                                "/gis/kpi/vaccination/drilldown/critical"
                              );

                            }


                            if (
                              name ===
                              "نیازمند بهبود"
                            ) {

                              navigate(
                                "/gis/kpi/vaccination/drilldown/warning"
                              );

                            }


                            if (
                              name ===
                              "مطلوب"
                            ) {

                              navigate(
                                "/gis/kpi/vaccination/drilldown/ontrack"
                              );

                            }

                          }
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



                      <Tooltip

                        formatter={
                          (value) =>
                            formatNumber(
                              Number(
                                value ?? 0
                              )
                            )
                        }

                      />



                      <Legend />



                    </PieChart>


                  </ResponsiveContainer>


                </div>


              </div>





              <div className="dashboard-panel">


                <h2>
                  وضعیت واکسیناسیون
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
                        vaccinationSplitData
                      }


                      margin={{
                        top: 20,
                        right: 20,
                        left: 10,
                        bottom: 20,
                      }}

                    >


                      <XAxis
                        dataKey="name"
                      />


                      <YAxis

                        tickFormatter={
                          (value) =>
                            new Intl.NumberFormat(
                              "fa-IR"
                            )
                              .format(
                                Number(value)
                              )
                        }

                      />


                      <Tooltip

                        formatter={
                          (value) =>
                            formatNumber(
                              Number(
                                value ?? 0
                              )
                            )
                        }

                      />


                      <Legend />



                      <Bar

                        dataKey="value"

                        name="تعداد دام"

                        radius={
                          [8, 8, 0, 0]
                        }


                        onClick={
                          (data: any) => {

                            const name =
                              data?.payload?.name;


                            if (
                              name ===
                              "باقی‌مانده"
                            ) {

                              navigate(
                                "/gis/kpi/vaccination/drilldown/remaining"
                              );

                            }


                            if (
                              name ===
                              "واحدهای واکسینه شده"
                            ) {

                              navigate(
                                "/gis/kpi/vaccination/drilldown/vaccinated"
                              );

                            }


                          }
                        }

                      >


                        {
                          vaccinationSplitData.map(
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


                      </Bar>



                    </BarChart>


                  </ResponsiveContainer>


                </div>


              </div>



            </div>

            <div
              className="dashboard-panel"
              style={{
                marginTop: 24,
              }}
            >

              <h2>
                درصد پوشش واکسیناسیون شهرستان‌ها
              </h2>


              <div
                style={{
                  width: "100%",
                  height: 380,
                }}
              >

                <ResponsiveContainer>

                  <BarChart

                    data={
                      countyChartData
                    }


                    margin={{
                      top: 20,
                      right: 20,
                      left: 10,
                      bottom: 70,
                    }}

                  >


                    <XAxis

                      dataKey="name"

                      angle={-35}

                      textAnchor="end"

                      interval={0}

                      height={85}

                    />



                    <YAxis

                      domain={[0, 100]}

                      tickFormatter={
                        (value) =>
                          `${value}%`
                      }

                    />



                    <Tooltip

                      formatter={
                        (value) =>
                          `${Number(
                            value ?? 0
                          ).toFixed(1)}%`
                      }

                    />



                    <Bar

                      dataKey="coverage"

                      name="درصد پوشش"

                      fill={
                        CHART_COLORS.vaccinated
                      }

                      radius={
                        [6, 6, 0, 0]
                      }


                      onClick={
                        (data: any) => {

                          const county =
                            data?.payload;


                          if (
                            county?.countyCode !==
                            undefined
                          ) {

                            navigate(
                              `/gis/kpi/vaccination/drilldown/county/${county.countyCode}`
                            );

                          }

                        }
                      }


                    />


                  </BarChart>


                </ResponsiveContainer>


              </div>


            </div>





            <div
              className="dashboard-panel"
              style={{
                marginTop: 24,
              }}
            >

              <h2>
                پوشش واکسن‌ها
              </h2>



              <div
                style={{
                  width: "100%",
                  height: 420,
                }}
              >

                <ResponsiveContainer>


                  <BarChart

                    data={
                      vaccineChartData
                    }


                    margin={{
                      top: 20,
                      right: 20,
                      left: 10,
                      bottom: 90,
                    }}

                  >


                    <XAxis

                      dataKey="vaccineType"

                      angle={-35}

                      textAnchor="end"

                      interval={0}

                      height={110}

                    />



                    <YAxis

                      domain={[0, 100]}

                      tickFormatter={
                        (value) =>
                          `${value}%`
                      }

                    />



                    <Tooltip

                      formatter={
                        (value) =>
                          `${Number(
                            value ?? 0
                          ).toFixed(1)}%`
                      }

                    />



                    <Bar

                      dataKey="coverage"

                      name="درصد پوشش"

                      fill={
                        CHART_COLORS.vaccinated
                      }

                      radius={
                        [6, 6, 0, 0]
                      }


                      onClick={
                        (data: any) => {

                          const vaccine =
                            data?.payload;


                          if (
                            vaccine?.vaccineType &&
                            vaccine.vaccineType !== "-"
                          ) {

                            navigate(
                              `/gis/kpi/vaccination/vaccine/${encodeURIComponent(
                                vaccine.vaccineType
                              )}`
                            );

                          }

                        }
                      }


                    />


                  </BarChart>


                </ResponsiveContainer>


              </div>



              <p
                style={{
                  marginTop: 12,
                }}
              >

                مقایسه عملکرد انواع واکسن‌ها
                بر اساس درصد پوشش و تعداد ثبت شده.

              </p>


            </div>





            <div
              className="dashboard-panel"
              style={{
                marginTop: 24,
              }}
            >

              <h2>
                جزئیات واکسن‌ها
              </h2>



              <div
                style={{
                  overflowX: "auto",
                }}
              >

                <table

                  style={{
                    width: "100%",
                    borderCollapse: "collapse",
                  }}

                >


                  <thead>

                    <tr>

                      <th>
                        نوع واکسن
                      </th>

                      <th>
                        برند
                      </th>

                      <th>
                        رکورد
                      </th>

                      <th>
                        کل دام
                      </th>

                      <th>
                        واکسینه شده
                      </th>

                      <th>
                        پوشش
                      </th>

                      <th>
                        عوارض
                      </th>

                      <th>
                        نرخ عوارض
                      </th>


                    </tr>

                  </thead>



                  <tbody>


                    {
                      vaccines.map(
                        (vaccine) => (


                          <tr

                            key={
                              `${vaccine.vaccine_type}-${vaccine.vaccine_brand}`
                            }


                            onClick={
                              () => {

                                if (
                                  vaccine.vaccine_type
                                ) {

                                  navigate(
                                    `/gis/kpi/vaccination/vaccine/${encodeURIComponent(
                                      vaccine.vaccine_type
                                    )}`
                                  );

                                }

                              }
                            }


                            style={{
                              cursor: "pointer",
                              borderTop:
                                "1px solid #ddd",
                            }}

                          >


                            <td>
                              {
                                vaccine.vaccine_type || "-"
                              }
                            </td>


                            <td>
                              {
                                vaccine.vaccine_brand || "-"
                              }
                            </td>


                            <td>
                              {
                                formatNumber(
                                  vaccine.records
                                )
                              }
                            </td>


                            <td>
                              {
                                formatNumber(
                                  vaccine.total_animals
                                )
                              }
                            </td>


                            <td>
                              {
                                formatNumber(
                                  vaccine.vaccinated_animals
                                )
                              }
                            </td>


                            <td>
                              {
                                Number(
                                  vaccine.coverage_percent || 0
                                ).toFixed(1)
                              }%
                            </td>


                            <td>
                              {
                                formatNumber(
                                  vaccine.adverse_events
                                )
                              }
                            </td>


                            <td>
                              {
                                Number(
                                  vaccine.adverse_event_rate_percent || 0
                                ).toFixed(2)
                              }%
                            </td>


                          </tr>


                        )
                      )
                    }


                  </tbody>


                </table>


              </div>


            </div>

            <div
              className="dashboard-panel"
              style={{
                marginTop: 24,
              }}
            >

              <h2>
                پانزده واحد با کمترین پوشش
              </h2>



              <div
                style={{
                  width: "100%",
                  height: 520,
                }}
              >

                <ResponsiveContainer>


                  <BarChart

                    data={
                      topUnitCoverageData
                    }

                    layout="vertical"


                    margin={{
                      top: 20,
                      right: 110,
                      left: 20,
                      bottom: 20,
                    }}

                  >


                    <XAxis

                      type="number"

                      domain={[0, 100]}

                      tickFormatter={
                        (value) =>
                          `${value}%`
                      }

                    />


                    <YAxis

                      type="category"

                      dataKey="name"

                      width={110}

                    />



                    <Tooltip

                      formatter={
                        (value) =>
                          `${Number(
                            value ?? 0
                          ).toFixed(1)}%`
                      }

                    />



                    <Bar

                      dataKey="coverage"

                      name="درصد پوشش"

                      fill={
                        CHART_COLORS.warning
                      }


                      radius={
                        [0, 6, 6, 0]
                      }


                      onClick={
                        (data: any) => {

                          const unit =
                            data?.payload;


                          if (
                            unit?.unitCode
                          ) {

                            navigate(
                              `/gis/kpi/vaccination/unit/${unit.unitCode}`
                            );

                          }

                        }
                      }

                    />


                  </BarChart>


                </ResponsiveContainer>


              </div>


            </div>





            <div className="panel">


              <h2>
                خلاصه شاخص‌های کلیدی
              </h2>



              <table>


                <thead>

                  <tr>

                    <th>
                      شاخص
                    </th>

                    <th>
                      مقدار
                    </th>

                    <th>
                      وضعیت
                    </th>

                  </tr>


                </thead>



                <tbody>


                  <tr>

                    <td>
                      پوشش واکسیناسیون
                    </td>

                    <td>
                      {
                        summary.coverage.toFixed(1)
                      }%
                    </td>

                    <td>
                      {
                        statusOf(
                          summary.coverage
                        )
                      }
                    </td>

                  </tr>



                  <tr>

                    <td>
                      دام واکسینه شده
                    </td>

                    <td>
                      {
                        formatNumber(
                          summary.vaccinatedAnimals
                        )
                      }
                    </td>

                    <td>
                      موفق
                    </td>

                  </tr>




                  <tr>

                    <td>
                      دام باقی‌مانده
                    </td>

                    <td>
                      {
                        formatNumber(
                          summary.remainingAnimals
                        )
                      }
                    </td>

                    <td>
                      نیازمند اقدام
                    </td>

                  </tr>




                  <tr>

                    <td>
                      عوارض ثبت شده
                    </td>

                    <td>
                      {
                        formatNumber(
                          summary.adverseEvents
                        )
                      }
                    </td>

                    <td>

                      {
                        summary.adverseEvents > 0
                          ? "بررسی شود"
                          : "بدون مشکل"
                      }

                    </td>

                  </tr>


                </tbody>


              </table>


            </div>





            <div className="panel">


              <h2>
                جزئیات واحدهای واکسیناسیون
              </h2>



              <div
                style={{
                  overflowX: "auto",
                }}
              >

                <table

                  style={{
                    width: "100%",
                    borderCollapse: "collapse",
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
                        استان
                      </th>

                      <th>
                        شهرستان
                      </th>

                      <th>
                        نوع واحد
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
                      units.map(
                        (unit) => (


                          <tr

                            key={
                              unit.unit_code
                            }


                            onClick={
                              () => navigate(
                                `/gis/kpi/vaccination/unit/${unit.unit_code}`
                              )
                            }


                            style={{
                              cursor: "pointer",
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
                                unit.unit_name
                              }
                            </td>


                            <td>
                              {
                                unit.province_name || "-"
                              }
                            </td>


                            <td>
                              {
                                unit.county_name || "-"
                              }
                            </td>


                            <td>
                              {
                                unit.unit_type || "-"
                              }
                            </td>


                            <td>
                              {
                                formatNumber(
                                  unit.total_animals
                                )
                              }
                            </td>


                            <td>
                              {
                                formatNumber(
                                  unit.vaccinated_animals
                                )
                              }
                            </td>


                            <td>
                              {
                                formatNumber(
                                  unit.remaining_animals
                                )
                              }
                            </td>


                            <td>
                              {
                                Number(
                                  unit.coverage_percent || 0
                                ).toFixed(1)
                              }%
                            </td>


                            <td

                              className={
                                statusClass(
                                  Number(
                                    unit.coverage_percent || 0
                                  )
                                )
                              }

                            >

                              {
                                statusOf(
                                  Number(
                                    unit.coverage_percent || 0
                                  )
                                )
                              }


                            </td>


                          </tr>


                        )
                      )
                    }


                  </tbody>


                </table>



                {
                  units.length === 0 && (

                    <p>
                      داده‌ای برای نمایش واحدها وجود ندارد.
                    </p>

                  )
                }



              </div>


            </div>
            <div className="panel ai-box">

              <h2>
                تحلیل هوشمند
              </h2>


              <p>
                ماژول AI بر اساس شاخص‌های KPI
                وضعیت عملکرد را تحلیل کرده و
                نقاط نیازمند اقدام را مشخص می‌کند.
              </p>



              <button

                type="button"

                onClick={() =>
                  navigate(
                    "/gis/kpi/vaccination"
                  )
                }

              >

                بازگشت به داشبورد واکسیناسیون

              </button>


            </div>


          </>

        )}

    </div>

  );

}