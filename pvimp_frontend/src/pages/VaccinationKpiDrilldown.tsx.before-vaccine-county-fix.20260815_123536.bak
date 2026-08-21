import React, { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getToken } from "../utils/token";

type Unit = {
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

const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000/api/v1";

function formatNumber(value: number) {
  return new Intl.NumberFormat("fa-IR").format(value ?? 0);
}

function statusOf(value: number) {
  if (value < 50) return "بحرانی";
  if (value < 75) return "نیازمند توجه";
  if (value < 90) return "مناسب";
  return "عالی";
}

export default function VaccinationKpiDrilldown() {
  const { view, code } = useParams();
  const navigate = useNavigate();

  const [units, setUnits] = useState<Unit[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const controller = new AbortController();

    async function load() {
      try {
        setLoading(true);
        setError("");

        let url = `${API_BASE}/gis/kpi/vaccination/units`;

        if (view === "county" && code) {
          url += `?county_code=${encodeURIComponent(code)}`;
        }

        const response = await fetch(url, {
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${getToken()}`
          },
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        if (!Array.isArray(data)) {
          throw new Error("INVALID_RESPONSE");
        }

        setUnits(data);

      } catch (err: any) {
        if (err?.name !== "AbortError") {
          setError("خطا در دریافت اطلاعات.");
        }
      } finally {
        setLoading(false);
      }
    }

    load();

    return () => controller.abort();

  }, [view, code]);


  const filteredUnits = useMemo(() => {

    if (view === "remaining") {
      return [...units]
        .filter(x => Number(x.remaining_animals || 0) > 0)
        .sort(
          (a, b) =>
            Number(b.remaining_animals || 0) -
            Number(a.remaining_animals || 0)
        );
    }


    if (view === "vaccinated") {
      return [...units].sort(
        (a, b) =>
          Number(b.vaccinated_animals || 0) -
          Number(a.vaccinated_animals || 0)
      );
    }


    if (view === "critical") {
      return units
        .filter(x => Number(x.coverage_percent || 0) < 50)
        .sort(
          (a, b) =>
            Number(a.coverage_percent || 0) -
            Number(b.coverage_percent || 0)
        );
    }


    if (view === "warning") {
      return units
        .filter(
          x =>
            Number(x.coverage_percent || 0) >= 50 &&
            Number(x.coverage_percent || 0) < 75
        );
    }


    if (view === "ontrack") {
      return units
        .filter(x => Number(x.coverage_percent || 0) >= 75)
        .sort(
          (a, b) =>
            Number(b.coverage_percent || 0) -
            Number(a.coverage_percent || 0)
        );
    }


    return units;

  }, [units, view]);


  const title = useMemo(() => {

    switch (view) {

      case "remaining":
        return "دام باقی مانده واکسیناسیون";

      case "vaccinated":
        return "دام واکسینه شده";

      case "critical":
        return "واحدهای بحرانی";

      case "warning":
        return "واحدهای نیازمند توجه";

      case "ontrack":
        return "واحدهای در مسیر مناسب";

      case "county":
        return `جزئیات شهرستان ${code ?? ""}`;

      default:
        return "جزئیات KPI واکسیناسیون";
    }

  }, [view, code]);


  const description = useMemo(() => {

    switch (view) {

      case "remaining":
        return "واحدهایی که هنوز دام واکسینه نشده دارند.";

      case "vaccinated":
        return "نمایش میزان واکسیناسیون انجام شده.";

      case "critical":
        return "واحدهای با پوشش پایین.";

      case "warning":
        return "واحدهای نیازمند بررسی.";

      case "ontrack":
        return "واحدهای با عملکرد مناسب.";

      case "county":
        return "جزئیات واحدهای شهرستان.";

      default:
        return "اطلاعات KPI واکسیناسیون.";

    }

  }, [view]);


  const totalValue = filteredUnits.reduce(
    (sum, unit) =>
      sum +
      Number(
        view === "remaining"
          ? unit.remaining_animals
          : unit.vaccinated_animals
      ),
    0
  );


  return (

    <div className="dashboard-page" dir="rtl">

      <div className="dashboard-header">

        <button
          type="button"
          onClick={() =>
            navigate("/gis/kpi/vaccination")
          }
        >
          بازگشت
        </button>


        <h1>{title}</h1>

        <p>{description}</p>

      </div>


      {loading && (
        <div className="panel">
          <h2>در حال دریافت اطلاعات...</h2>
        </div>
      )}


      {error && (
        <div className="panel">
          <h2>خطا</h2>
          <p>{error}</p>
        </div>
      )}



      {!loading && !error && (

        <>

          <div className="kpi-grid">

            <div className="kpi-card">
              <div className="kpi-title">
                تعداد واحدها
              </div>

              <div className="kpi-value">
                {formatNumber(filteredUnits.length)}
              </div>
            </div>


            {(view === "remaining" || view === "vaccinated") && (

              <div className="kpi-card">

                <div className="kpi-title">
                  {view === "remaining"
                    ? "تعداد دام باقی مانده"
                    : "تعداد دام واکسینه شده"}
                </div>

                <div className="kpi-value">
                  {formatNumber(totalValue)}
                </div>

              </div>

            )}

          </div>


          <div className="panel">

            <h2>لیست واحدها</h2>


            <table
              style={{
                width: "100%",
                borderCollapse: "collapse"
              }}
            >

              <thead>

                <tr>

                  <th>کد</th>
                  <th>نام واحد</th>
                  <th>استان</th>
                  <th>شهرستان</th>
                  <th>نوع</th>
                  <th>کل دام</th>
                  <th>واکسینه</th>
                  <th>باقی مانده</th>
                  <th>پوشش</th>
                  <th>وضعیت</th>

                </tr>

              </thead>


              <tbody>

                {
                  filteredUnits.map(unit => (

                    <tr
                      key={unit.unit_code}
                      onClick={() => navigate(
                        `/gis/kpi/vaccination/unit/${unit.unit_code}`
                      )}
                      style={{
                        cursor: "pointer"
                      }}
                    >

                      <td>{unit.unit_code}</td>

                      <td>{unit.unit_name}</td>

                      <td>{unit.province_name || "-"}</td>

                      <td>{unit.county_name || "-"}</td>

                      <td>{unit.unit_type || "-"}</td>

                      <td>{formatNumber(unit.total_animals)}</td>

                      <td>{formatNumber(unit.vaccinated_animals)}</td>

                      <td>{formatNumber(unit.remaining_animals)}</td>

                      <td>
                        {Number(unit.coverage_percent || 0).toFixed(1)}%
                      </td>

                      <td>
                        {
                          statusOf(
                            Number(unit.coverage_percent || 0)
                          )
                        }
                      </td>

                    </tr>

                  ))
                }

              </tbody>

            </table>


            {
              filteredUnits.length === 0 &&
              <p>
                اطلاعاتی برای نمایش وجود ندارد.
              </p>
            }


          </div>

        </>

      )}

    </div>

  );

}