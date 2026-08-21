import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getToken } from "../utils/token";
import api from "../services/api";
import "../styles/index.css";

type UnitData = {
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

type HistoryItem = {
  date: string | null;
  operation: string;
  operation_code: string;
  title: string | null;
  detail: string | null;
  animal_count: number;
  animal_type: string | null;
  subtype: string | null;
};

type UnitHistoryResponse = {
  unit_code: string;
  unit_name: string | null;
  history: HistoryItem[];
};


const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000/api/v1";


function formatNumber(
  value: number | null | undefined
) {
  return new Intl.NumberFormat(
    "fa-IR"
  ).format(value ?? 0);
}



function formatDate(
  value: string | null | undefined
) {

  if (!value) {
    return "-";
  }


  const normalized =
    String(value).trim();


  const match =
    normalized.match(
      /^(\d{4})-(\d{1,2})-(\d{1,2})/
    );


  let formatted: string;


  if (match) {

    const [
      ,
      year,
      month,
      day
    ] = match;


    formatted =
      `${year}/${month.padStart(
        2,
        "0"
      )}/${day.padStart(
        2,
        "0"
      )}`;

  } else {


    const slashMatch =
      normalized.match(
        /^(\d{4})\/(\d{1,2})\/(\d{1,2})/
      );


    if (slashMatch) {

      const [
        ,
        year,
        month,
        day
      ] = slashMatch;


      formatted =
        `${year}/${month.padStart(
          2,
          "0"
        )}/${day.padStart(
          2,
          "0"
        )}`;

    } else {

      formatted =
        normalized;

    }
  }


  return formatted.replace(
    /\d/g,
    (digit) =>
      "۰۱۲۳۴۵۶۷۸۹"[
      Number(digit)
      ]
  );
}



function operationStyle(
  operationCode: string
): React.CSSProperties {


  if (
    operationCode === "VACCINATION"
  ) {

    return {
      background: "#dcfce7",
      color: "#166534",
      fontWeight: 700,
      padding: "4px 10px",
      borderRadius: 8,
      display: "inline-block",
    };

  }



  if (
    operationCode === "SPRAYING"
  ) {

    return {
      background: "#dbeafe",
      color: "#1e40af",
      fontWeight: 700,
      padding: "4px 10px",
      borderRadius: 8,
      display: "inline-block",
    };

  }



  return {

    background: "#f3f4f6",
    color: "#374151",
    fontWeight: 700,
    padding: "4px 10px",
    borderRadius: 8,
    display: "inline-block",

  };

}



export default function KpiDetail() {


  const {
    unitCode = ""
  } = useParams();


  const navigate =
    useNavigate();



  const [
    data,
    setData
  ] =
    useState<UnitData | null>(
      null
    );



  const [
    history,
    setHistory
  ] =
    useState<HistoryItem[]>(
      []
    );



  const [
    loading,
    setLoading
  ] =
    useState(true);



  const [
    historyLoading,
    setHistoryLoading
  ] =
    useState(true);



  const [
    error,
    setError
  ] =
    useState("");



  const [
    historyError,
    setHistoryError
  ] =
    useState("");

  useEffect(() => {

    if (!unitCode) {
      return;
    }


    const controller =
      new AbortController();



    async function loadUnit() {

      try {

        setLoading(true);

        setError("");



        const response =
          await fetch(
            `${API_BASE}/gis/kpi/vaccination/units?unit_code=${encodeURIComponent(
              unitCode
            )}`,
            {
              headers: {
                Accept: "application/json",
                Authorization: `Bearer ${getToken()}`,
              },

              signal:
                controller.signal,
            }
          );



        if (!response.ok) {

          throw new Error(
            `HTTP ${response.status}`
          );

        }



        const result =
          await response.json();



        if (
          !Array.isArray(result) ||
          result.length === 0
        ) {

          throw new Error(
            "UNIT_NOT_FOUND"
          );

        }



        setData(result[0]);



      } catch (err: any) {


        if (
          err?.name !==
          "AbortError"
        ) {

          setError(
            "خطا در دریافت اطلاعات واحد."
          );

        }


      } finally {

        setLoading(false);

      }

    }



    loadUnit();



    return () =>
      controller.abort();


  }, [unitCode]);





  useEffect(() => {


    if (!unitCode) {

      return;

    }



    const controller =
      new AbortController();




    async function loadHistory() {


      try {


        setHistoryLoading(true);

        setHistoryError("");




        const response =
          await fetch(
            `${API_BASE}/gis/kpi/vaccination/unit/${encodeURIComponent(
              unitCode
            )}/history`,
            {
              headers: {
                Accept: "application/json",
                Authorization: `Bearer ${getToken()}`,
              },

              signal:
                controller.signal,
            }
          );




        if (!response.ok) {


          throw new Error(
            `HTTP ${response.status}`
          );


        }




        const result =
          (
            await response.json()
          ) as UnitHistoryResponse;




        setHistory(
          Array.isArray(
            result.history
          )
            ? result.history
            : []
        );



      } catch (err: any) {



        if (
          err?.name !==
          "AbortError"
        ) {


          setHistoryError(
            "خطا در دریافت تاریخچه عملیات."
          );


        }


      } finally {


        setHistoryLoading(false);


      }

    }




    loadHistory();




    return () =>
      controller.abort();



  }, [unitCode]);





  return (

    <div
      className="dashboard-page"
      dir="rtl"
    >


      <header
        className="dashboard-header"
      >


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



        <h1>

          جزئیات KPI واحد اپیدمیولوژیک

        </h1>



        <p>
          کد واحد:
          {" "}
          {unitCode}
        </p>


      </header>




      {loading && (

        <div
          className="dashboard-panel"
        >

          <h2>
            در حال دریافت اطلاعات...
          </h2>

        </div>

      )}






      {error && (

        <div
          className="dashboard-panel"
        >

          <h2>
            خطا
          </h2>


          <p>
            {error}
          </p>


        </div>

      )}






      {data &&
        !loading &&
        !error && (

          <>

            <div
              className="dashboard-grid"
            >


              <div
                className="dashboard-panel"
              >

                <h2>
                  مشخصات واحد
                </h2>


                <p>
                  <strong>
                    کد:
                  </strong>
                  {" "}
                  {data.unit_code}
                </p>


                <p>
                  <strong>
                    نام:
                  </strong>
                  {" "}
                  {data.unit_name}
                </p>


                <p>
                  <strong>
                    استان:
                  </strong>
                  {" "}
                  {data.province_name || "-"}
                </p>


                <p>
                  <strong>
                    شهرستان:
                  </strong>
                  {" "}
                  {data.county_name || "-"}
                </p>


                <p>
                  <strong>
                    نوع واحد:
                  </strong>
                  {" "}
                  {data.unit_type || "-"}
                </p>


              </div>
              <div
                className="dashboard-panel"
              >

                <h2>
                  وضعیت واکسیناسیون
                </h2>


                <p>
                  <strong>
                    پوشش:
                  </strong>
                  {" "}
                  {Number(
                    data.coverage_percent || 0
                  ).toFixed(1)}
                  %
                </p>


                <p>
                  <strong>
                    کل دام:
                  </strong>
                  {" "}
                  {formatNumber(
                    data.total_animals
                  )}
                </p>


                <p>
                  <strong>
                    دام واجد شرایط:
                  </strong>
                  {" "}
                  {formatNumber(
                    data.eligible_animals
                  )}
                </p>


                <p>
                  <strong>
                    واکسینه شده:
                  </strong>
                  {" "}
                  {formatNumber(
                    data.vaccinated_animals
                  )}
                </p>


                <p>
                  <strong>
                    باقی‌مانده:
                  </strong>
                  {" "}
                  {formatNumber(
                    data.remaining_animals
                  )}
                </p>


                <p>
                  <strong>
                    تعداد رکورد:
                  </strong>
                  {" "}
                  {formatNumber(
                    data.records
                  )}
                </p>


              </div>





              <div
                className="dashboard-panel"
              >

                <h2>
                  عوارض
                </h2>


                <p>
                  <strong>
                    تعداد عوارض:
                  </strong>
                  {" "}
                  {formatNumber(
                    data.adverse_events
                  )}
                </p>


                <p>
                  <strong>
                    نرخ عوارض:
                  </strong>
                  {" "}
                  {Number(
                    data.adverse_event_rate_percent || 0
                  ).toFixed(2)}
                  %
                </p>


              </div>


            </div>





            <div
              className="dashboard-panel"
            >

              <h2>
                تاریخچه عملیات واحد
              </h2>




              {historyLoading && (

                <p>
                  در حال دریافت تاریخچه...
                </p>

              )}





              {historyError && (

                <p
                  style={{
                    color:
                      "#991b1b",
                  }}
                >
                  {historyError}
                </p>

              )}






              {
                !historyLoading &&
                !historyError &&
                history.length === 0 && (

                  <p>
                    هیچ عملیات ثبت شده‌ای برای این واحد وجود ندارد.
                  </p>

                )
              }





              {
                !historyLoading &&
                !historyError &&
                history.length > 0 && (

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

                        marginTop:
                          "16px",
                      }}

                    >

                      <thead>

                        <tr>

                          <th>
                            تاریخ
                          </th>


                          <th>
                            عملیات
                          </th>


                          <th>
                            عنوان
                          </th>


                          <th>
                            جزئیات
                          </th>


                          <th>
                            نوع دام
                          </th>


                          <th>
                            تعداد
                          </th>


                          <th>
                            زیرنوع
                          </th>


                        </tr>

                      </thead>





                      <tbody>


                        {
                          history.map(
                            (
                              item,
                              index
                            ) => (

                              <tr

                                key={
                                  `${item.operation_code}-${item.date}-${index}`
                                }

                                style={{
                                  borderTop:
                                    "1px solid #ddd",
                                }}

                              >


                                <td>
                                  {
                                    formatDate(
                                      item.date
                                    )
                                  }
                                </td>



                                <td>

                                  <span

                                    style={
                                      operationStyle(
                                        item.operation_code
                                      )
                                    }

                                  >

                                    {
                                      item.operation
                                    }

                                  </span>

                                </td>



                                <td>

                                  {
                                    item.title ||
                                    "-"
                                  }

                                </td>



                                <td>

                                  {
                                    item.detail ||
                                    "-"
                                  }

                                </td>



                                <td>

                                  {
                                    item.animal_type ||
                                    "-"
                                  }

                                </td>



                                <td>

                                  {
                                    formatNumber(
                                      item.animal_count
                                    )
                                  }

                                </td>



                                <td>

                                  {
                                    item.subtype ||
                                    "-"
                                  }

                                </td>



                              </tr>

                            )
                          )
                        }


                      </tbody>


                    </table>


                  </div>

                )
              }



            </div>
            <div
              className="dashboard-panel"
            >

              <h2>
                توضیحات KPI
              </h2>


              <p>

                KPI واکسیناسیون از جدول

                {" "}

                <code>
                  gis_vaccination_performances
                </code>

                {" "}

                خوانده می‌شود و وضعیت پوشش،
                تعداد دام، واکسینه شده و باقی‌مانده
                را نمایش می‌دهد.

              </p>


            </div>



          </>

        )}


    </div>

  );

}





