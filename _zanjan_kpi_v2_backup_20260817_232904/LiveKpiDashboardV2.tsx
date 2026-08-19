import React, {
  useEffect,
  useMemo,
  useState
} from "react";

import "./LiveKpiDashboardV2.css";


const API = "/api/v1/gis/dashboard/kpi-v2";


type AnyObj = Record<string, any>;


const nf = new Intl.NumberFormat(
  "fa-IR",
  {
    maximumFractionDigits: 1
  }
);


function number(value: any) {

  return nf.format(
    Number(value || 0)
  );

}


function percent(value: any) {

  return `${nf.format(
    Number(value || 0)
  )}%`;

}


async function getJson(
  path: string
) {

  const response = await fetch(
    `${API}${path}`,
    {
      credentials: "include"
    }
  );

  if (!response.ok) {

    throw new Error(
      `${response.status}: ${await response.text()}`
    );

  }

  return response.json();

}


function Card(
  {
    label,
    value,
    sub,
    onClick
  }: {
    label: string;
    value: any;
    sub?: string;
    onClick?: () => void;
  }
) {

  return (

    <div
      className="kpi-v2-card"
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


function LineChart(
  {
    data
  }: {
    data: AnyObj[];
  }
) {

  if (!data?.length) {

    return (
      <div className="empty-state">
        Ø¯Ø§Ø¯Ù‡â€ŒØ§ÛŒ Ø¨Ø±Ø§ÛŒ Ù†Ù…ÙˆØ¯Ø§Ø± ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯
      </div>
    );

  }

  const width = 800;
  const height = 260;
  const padding = 40;

  const values =
    data.map(
      x => Number(x.value || 0)
    );

  const max =
    Math.max(
      ...values,
      1
    );

  const points =
    data.map(
      (x, i) => {

        const px =
          padding +
          (
            i *
            (
              (width - padding * 2) /
              Math.max(
                data.length - 1,
                1
              )
            )
          );

        const py =
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

        return {
          x: px,
          y: py,
          value: x.value,
          period: x.period
        };

      }
    );

  const polyline =
    points
      .map(
        p => `${p.x},${p.y}`
      )
      .join(" ");

  return (

    <svg
      viewBox={`0 0 ${width} ${height}`}
      width="100%"
      height="100%"
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
        (p, i) => (

          <g key={i}>

            <circle
              cx={p.x}
              cy={p.y}
              r="5"
              fill="#1bdcff"
            />

            <text
              x={p.x}
              y={height - 10}
              fill="#789aaa"
              fontSize="10"
              textAnchor="middle"
            >
              {String(
                p.period || ""
              ).slice(5)}
            </text>

          </g>

        )
      )}

    </svg>

  );

}


function BarChart(
  {
    data,
    onClick
  }: {
    data: AnyObj[];
    onClick?: (item: AnyObj) => void;
  }
) {

  if (!data?.length) {

    return (
      <div className="empty-state">
        Ø¯Ø§Ø¯Ù‡â€ŒØ§ÛŒ Ø¨Ø±Ø§ÛŒ Ù†Ù…ÙˆØ¯Ø§Ø± ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯
      </div>
    );

  }

  const max =
    Math.max(
      ...data.map(
        x => Number(x.value || 0)
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
        padding: "10px 5px"
      }}
    >

      {data.slice(0, 15).map(
        (item, index) => {

          const value =
            Number(
              item.value || 0
            );

          const height =
            Math.max(
              5,
              value / max * 185
            );

          return (

            <div
              key={index}
              style={{
                flex: 1,
                minWidth: 30,
                cursor:
                  onClick
                    ? "pointer"
                    : "default",
                textAlign: "center"
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
                    "linear-gradient(180deg,#1bdcff,#07506b)"
                }}
              />

              <div
                style={{
                  color: "#8caebe",
                  fontSize: 9,
                  marginTop: 5,
                  overflow: "hidden"
                }}
              >
                {String(
                  item.name ||
                  item.period ||
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


function Breadcrumb(
  {
    level,
    province,
    county,
    unit,
    onRoot,
    onProvince,
    onCounty
  }: AnyObj
) {

  return (

    <div className="kpi-v2-drill">

      <button
        className={
          `kpi-v2-crumb ${
            level === "root"
              ? "current"
              : ""
          }`
        }
        onClick={onRoot}
      >
        Ú©Ù„ Ú©Ø´ÙˆØ±
      </button>

      {province && (

        <>

          <span className="kpi-v2-arrow">
            â†
          </span>

          <button
            className={
              `kpi-v2-crumb ${
                level === "province"
                  ? "current"
                  : ""
              }`
            }
            onClick={onProvince}
          >
            {province.name}
          </button>

        </>

      )}

      {county && (

        <>

          <span className="kpi-v2-arrow">
            â†
          </span>

          <button
            className={
              `kpi-v2-crumb ${
                level === "county"
                  ? "current"
                  : ""
              }`
            }
            onClick={onCounty}
          >
            {county.name}
          </button>

        </>

      )}

      {unit && (

        <>

          <span className="kpi-v2-arrow">
            â†
          </span>

          <button
            className="kpi-v2-crumb current"
          >
            {unit.name}
          </button>

        </>

      )}

    </div>

  );

}


function UnitTimeline(
  {
    operations,
    unitId
  }: {
    operations: AnyObj[];
    unitId: number;
  }
) {

  const [
    selected,
    setSelected
  ] = useState<AnyObj | null>(
    null
  );

  const [
    chain,
    setChain
  ] = useState<AnyObj[]>([]);

  async function openOperation(
    operation: AnyObj
  ) {

    setSelected(operation);

    try {

      const result =
        await getJson(
          `/units/${unitId}/chain?operation_id=${operation.source_id}`
        );

      setChain(
        result.items || []
      );

    } catch {

      setChain([]);

    }

  }

  return (

    <div className="kpi-v2-panel">

      <h2>
        ØªØ§Ø±ÛŒØ®Ú†Ù‡ Ùˆ Ø²Ù†Ø¬ÛŒØ±Ù‡ ØªÙ…Ø§Ù… Ø¹Ù…Ù„ÛŒØ§Øª Ù…Ø±ØªØ¨Ø· ÙˆØ§Ø­Ø¯
      </h2>

      <p
        style={{
          color: "#789",
          fontSize: 11
        }}
      >
        Ù‡Ø± Ø±Ø¯ÛŒÙ Ù‚Ø§Ø¨Ù„ Ú©Ù„ÛŒÚ© Ø§Ø³Øª Ùˆ Ø¯Ø± ØµÙˆØ±Øª ÙˆØ¬ÙˆØ¯
        FK Ù…Ø´ØªØ±Ú©ØŒ Ø²Ù†Ø¬ÛŒØ±Ù‡ Ù…Ø±ØªØ¨Ø· Ù‡Ù…Ø§Ù† Ø¹Ù…Ù„ÛŒØ§Øª Ø±Ø§
        Ù†Ù…Ø§ÛŒØ´ Ù…ÛŒâ€ŒØ¯Ù‡Ø¯.
      </p>

      <div className="kpi-v2-timeline">

        {operations.length === 0 && (

          <div className="empty-state">
            Ø¨Ø±Ø§ÛŒ Ø§ÛŒÙ† ÙˆØ§Ø­Ø¯ Ù‡Ù†ÙˆØ² Ø¹Ù…Ù„ÛŒØ§Øª Ù‚Ø§Ø¨Ù„ Ù†Ù…Ø§ÛŒØ´
            Ø¯Ø± Ø¬Ø¯Ø§ÙˆÙ„ Ù…Ù†Ø¨Ø¹ Ù¾ÛŒØ¯Ø§ Ù†Ø´Ø¯.
          </div>

        )}

        {operations.map(
          (operation, index) => (

            <React.Fragment
              key={`${operation.source_id}-${index}`}
            >

              <div
                className="timeline-row"
                onClick={() =>
                  openOperation(operation)
                }
              >

                <div className="timeline-date">
                  {String(
                    operation.event_date || ""
                  ).slice(0, 19)}
                </div>

                <div className="timeline-type">
                  {operation.operation_type}
                </div>

                <div className="timeline-detail">

                  {operation.disease_id && (
                    <span>
                      Ø¨ÛŒÙ…Ø§Ø±ÛŒ: {operation.disease_id}
                      {" | "}
                    </span>
                  )}

                  {operation.sample_id && (
                    <span>
                      Ù†Ù…ÙˆÙ†Ù‡: {operation.sample_id}
                      {" | "}
                    </span>
                  )}

                  {operation.laboratory_result_id && (
                    <span>
                      Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡:
                      {" "}
                      {operation.laboratory_result_id}
                      {" | "}
                    </span>
                  )}

                  {operation.result_status && (
                    <span>
                      Ù†ØªÛŒØ¬Ù‡:
                      {" "}
                      {operation.result_status}
                    </span>
                  )}

                </div>

              </div>

              {selected?.source_id ===
                operation.source_id && (

                <div className="timeline-chain">

                  <strong>
                    Ø²Ù†Ø¬ÛŒØ±Ù‡ Ù…Ø±ØªØ¨Ø· Ø¹Ù…Ù„ÛŒØ§Øª
                  </strong>

                  {chain.length === 0 && (

                    <div
                      style={{
                        color: "#789",
                        marginTop: 8
                      }}
                    >
                      Ø±Ø§Ø¨Ø·Ù‡ FK Ù…Ø´ØªØ±Ú© Ø¨Ø±Ø§ÛŒ Ø§ÛŒÙ† Ø¹Ù…Ù„ÛŒØ§Øª
                      Ù¾ÛŒØ¯Ø§ Ù†Ø´Ø¯ ÛŒØ§ Ø±Ú©ÙˆØ±Ø¯ Ù…Ø±ØªØ¨Ø· ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯.
                    </div>

                  )}

                  {chain.map(
                    (item, i) => (

                      <div
                        className="chain-item"
                        key={i}
                      >

                        <div>
                          {String(
                            item.event_date || ""
                          ).slice(0, 19)}
                        </div>

                        <div>
                          {item.operation_type}
                        </div>

                        <div>
                          {item.disease_id
                            ? `Ø¨ÛŒÙ…Ø§Ø±ÛŒ: ${item.disease_id}`
                            : ""}
                          {" "}
                          {item.sample_id
                            ? `Ù†Ù…ÙˆÙ†Ù‡: ${item.sample_id}`
                            : ""}
                          {" "}
                          {item.laboratory_result_id
                            ? `Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡: ${item.laboratory_result_id}`
                            : ""}
                          {" "}
                          {item.result_status
                            ? `Ù†ØªÛŒØ¬Ù‡: ${item.result_status}`
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


export default function LiveKpiDashboardV2() {

  const [
    data,
    setData
  ] = useState<AnyObj | null>(
    null
  );

  const [
    metric,
    setMetric
  ] = useState("all");

  const [
    level,
    setLevel
  ] = useState<
    "root" |
    "province" |
    "county" |
    "unit"
  >("root");

  const [
    province,
    setProvince
  ] = useState<AnyObj | null>(
    null
  );

  const [
    county,
    setCounty
  ] = useState<AnyObj | null>(
    null
  );

  const [
    unit,
    setUnit
  ] = useState<AnyObj | null>(
    null
  );

  const [
    locations,
    setLocations
  ] = useState<AnyObj[]>([]);

  const [
    unitDetail,
    setUnitDetail
  ] = useState<AnyObj | null>(
    null
  );

  const [
    loading,
    setLoading
  ] = useState(true);

  const [
    error,
    setError
  ] = useState("");

  const [
    refresh,
    setRefresh
  ] = useState(0);


  useEffect(
    () => {

      setLoading(true);
      setError("");

      getJson("/overview")
        .then(setData)
        .catch(
          e => setError(
            String(e)
          )
        )
        .finally(
          () => setLoading(false)
        );

    },
    [refresh]
  );


  useEffect(
    () => {

      if (level === "root") {

        setLocations([]);

        return;

      }

      setLoading(true);

      let request = "";

      if (level === "province") {

        request =
          `/provinces?metric=${metric}`;

      }

      if (
        level === "county" &&
        province
      ) {

        request =
          `/provinces/${province.id}/counties?metric=${metric}`;

      }

      if (
        level === "unit" &&
        county
      ) {

        request =
          `/counties/${county.id}/units?metric=${metric}`;

      }

      if (!request) {

        setLoading(false);
        return;

      }

      getJson(request)
        .then(
          result =>
            setLocations(
              result.items || []
            )
        )
        .catch(
          e =>
            setError(
              String(e)
            )
        )
        .finally(
          () =>
            setLoading(false)
        );

    },
    [
      level,
      province,
      county,
      metric
    ]
  );


  useEffect(
    () => {

      if (!unit) {

        setUnitDetail(null);
        return;

      }

      setLoading(true);

      getJson(
        `/units/${unit.id}`
      )
        .then(
          setUnitDetail
        )
        .catch(
          e =>
            setError(
              String(e)
            )
        )
        .finally(
          () =>
            setLoading(false)
        );

    },
    [unit]
  );


  const cards =
    data?.cards || {};

  const charts =
    data?.charts || {};


  function drillMetric(
    selectedMetric: string
  ) {

    setMetric(
      selectedMetric
    );

    setProvince(null);
    setCounty(null);
    setUnit(null);
    setUnitDetail(null);

    setLevel(
      "province"
    );

  }


  function root() {

    setMetric("all");

    setProvince(null);
    setCounty(null);
    setUnit(null);
    setUnitDetail(null);

    setLevel("root");

  }


  function openProvince(
    item: AnyObj
  ) {

    setProvince(item);
    setCounty(null);
    setUnit(null);
    setUnitDetail(null);

    setLevel("county");

  }


  function openCounty(
    item: AnyObj
  ) {

    setCounty(item);
    setUnit(null);
    setUnitDetail(null);

    setLevel("unit");

  }


  function openUnit(
    item: AnyObj
  ) {

    setUnit(item);

    setLevel("unit");

  }


  if (
    loading &&
    !data
  ) {

    return (
      <div className="live-kpi-v2">
        Ø¯Ø± Ø­Ø§Ù„ Ø¯Ø±ÛŒØ§ÙØª KPIÙ‡Ø§ÛŒ Ø²Ù†Ø¯Ù‡ Ø§Ø² PostgreSQL...
      </div>
    );

  }


  if (
    error &&
    !data
  ) {

    return (
      <div className="live-kpi-v2">

        <div className="kpi-v2-panel">

          <b>Ø®Ø·Ø§:</b>

          {" "}

          {error}

        </div>

      </div>
    );

  }


  return (

    <div className="live-kpi-v2">

      <div className="kpi-v2-header">

        <div>

          <h1>
            Ø¯Ø§Ø´Ø¨ÙˆØ±Ø¯ Ø²Ù†Ø¯Ù‡ Ú©Ù†ØªØ±Ù„ Ø¨ÛŒÙ…Ø§Ø±ÛŒ Ùˆ Ø¹Ù…Ù„ÛŒØ§Øª Ø¯Ø§Ù…Ù¾Ø²Ø´Ú©ÛŒ
          </h1>

          <p>
            ØªÙ…Ø§Ù… KPIÙ‡Ø§ Ùˆ Ù†Ù…ÙˆØ¯Ø§Ø±Ù‡Ø§ Ø¯Ø± ÛŒÚ© ØµÙØ­Ù‡ â€”
            Ú©Ù„ÛŒÚ© Ø±ÙˆÛŒ Ù‡Ø± KPI Ø´Ù…Ø§ Ø±Ø§ ØªØ§ Ø§Ø³ØªØ§Ù†ØŒ
            Ø´Ù‡Ø±Ø³ØªØ§Ù† Ùˆ ÙˆØ§Ø­Ø¯ Ù‡Ø¯Ø§ÛŒØª Ù…ÛŒâ€ŒÚ©Ù†Ø¯.
          </p>

        </div>

        <div
          style={{
            display: "flex",
            gap: 8,
            alignItems: "center"
          }}
        >

          <span className="live-badge">
            â— LIVE PostgreSQL
          </span>

          <button
            className="refresh-button"
            onClick={() =>
              setRefresh(
                x => x + 1
              )
            }
          >
            â†» Ø¨Ø±ÙˆØ²Ø±Ø³Ø§Ù†ÛŒ
          </button>

        </div>

      </div>


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

            setLevel("county");

          }}

          onCounty={() => {

            setUnit(null);
            setUnitDetail(null);

            setLevel("unit");

          }}

        />

      )}


      {level === "root" && (

        <>

          <div className="kpi-v2-grid">

            <Card
              label="ÙˆØ§Ø­Ø¯Ù‡Ø§ÛŒ Ø§Ù¾ÛŒØ¯Ù…ÛŒÙˆÙ„ÙˆÚ˜ÛŒÚ©"
              value={number(
                cards.total_units
              )}
              onClick={() =>
                drillMetric("units")
              }
            />

            <Card
              label="ÙˆØ§Ø­Ø¯Ù‡Ø§ÛŒ ÙØ¹Ø§Ù„"
              value={number(
                cards.active_units
              )}
              onClick={() =>
                drillMetric("units")
              }
            />

            <Card
              label="Ú¯Ø²Ø§Ø±Ø´ Ø¨ÛŒÙ…Ø§Ø±ÛŒ"
              value={number(
                cards.disease_reports
              )}
              onClick={() =>
                drillMetric("disease")
              }
            />

            <Card
              label="ÙˆÙ‚ÙˆØ¹ Ø¨ÛŒÙ…Ø§Ø±ÛŒ"
              value={number(
                cards.disease_occurrences
              )}
              onClick={() =>
                drillMetric("disease")
              }
            />

            <Card
              label="Ù…Ø±Ø§Ù‚Ø¨Øª ÙØ¹Ø§Ù„"
              value={number(
                cards.care_records
              )}
              onClick={() =>
                drillMetric("care")
              }
            />

            <Card
              label="ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ† Ø§Ù†Ø¬Ø§Ù…â€ŒØ´Ø¯Ù‡"
              value={number(
                cards.vaccinated
              )}
              sub={
                "Ú©Ù„ÛŒÚ© Ø¨Ø±Ø§ÛŒ Drill-down"
              }
              onClick={() =>
                drillMetric("vaccination")
              }
            />

            <Card
              label="Ø¯Ø§Ù… ÙˆØ§Ø¬Ø¯ Ø´Ø±Ø§ÛŒØ·"
              value={number(
                cards.eligible
              )}
              onClick={() =>
                drillMetric("vaccination")
              }
            />

            <Card
              label="Ù¾ÙˆØ´Ø´ ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†"
              value={percent(
                cards.vaccination_coverage
              )}
              onClick={() =>
                drillMetric("vaccination")
              }
            />

            <Card
              label="Ø¨Ø§Ù‚ÛŒâ€ŒÙ…Ø§Ù†Ø¯Ù‡ ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†"
              value={number(
                cards.vaccination_remaining
              )}
              onClick={() =>
                drillMetric("vaccination")
              }
            />

            <Card
              label="Ù†ØªØ§ÛŒØ¬ Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡ÛŒ"
              value={number(
                cards.lab_results
              )}
              onClick={() =>
                drillMetric("lab")
              }
            />

            <Card
              label="Ù…Ø«Ø¨Øª Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡"
              value={number(
                cards.lab_positive
              )}
              onClick={() =>
                drillMetric("lab")
              }
            />

            <Card
              label="Ù†Ø±Ø® Ù…Ø«Ø¨Øª Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡"
              value={percent(
                cards.lab_positive_rate
              )}
              onClick={() =>
                drillMetric("lab")
              }
            />

            <Card
              label="Ù†Ù…ÙˆÙ†Ù‡â€ŒÙ‡Ø§"
              value={number(
                cards.sample_records
              )}
              onClick={() =>
                drillMetric("samples")
              }
            />

            <Card
              label="Ù…ÙˆØ¬ÙˆØ¯ÛŒ ÙˆØ§Ú©Ø³Ù†"
              value={number(
                cards.inventory
              )}
            />

            <Card
              label="ØªÙˆØ²ÛŒØ¹ ÙˆØ§Ú©Ø³Ù†"
              value={number(
                cards.distributed
              )}
            />

            <Card
              label="Ø¯ÙØ¹ ÙˆØ§Ú©Ø³Ù†"
              value={number(
                cards.disposed
              )}
            />

          </div>


          <div className="kpi-v2-layout">

            <div>

              <div className="kpi-v2-panel">

                <h2>
                  Ø±ÙˆÙ†Ø¯ ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†
                </h2>

                <div className="kpi-v2-chart">

                  <LineChart
                    data={
                      charts.vaccination || []
                    }
                  />

                </div>

              </div>


              <div className="kpi-v2-panel">

                <h2>
                  Ø±ÙˆÙ†Ø¯ Ú¯Ø²Ø§Ø±Ø´ Ø¨ÛŒÙ…Ø§Ø±ÛŒ
                </h2>

                <div className="kpi-v2-chart">

                  <LineChart
                    data={
                      charts.disease || []
                    }
                  />

                </div>

              </div>

            </div>


            <div>

              <div className="kpi-v2-panel">

                <h2>
                  Ø±ÙˆÙ†Ø¯ Ù…Ø±Ø§Ù‚Ø¨Øª
                </h2>

                <div className="kpi-v2-chart">

                  <LineChart
                    data={
                      charts.care || []
                    }
                  />

                </div>

              </div>


              <div className="kpi-v2-panel">

                <h2>
                  Ø±ÙˆÙ†Ø¯ Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡
                </h2>

                <div className="kpi-v2-chart">

                  <LineChart
                    data={
                      charts.laboratory || []
                    }
                  />

                </div>

              </div>

            </div>

          </div>

        </>

      )}


      {level !== "root" &&
       level !== "unit" && (

        <div className="kpi-v2-panel">

          <h2>

            {level === "province"
              ? `Ø§Ø³ØªØ§Ù†â€ŒÙ‡Ø§ â€” Ø´Ø§Ø®Øµ: ${metric}`
              : `Ø´Ù‡Ø±Ø³ØªØ§Ù†â€ŒÙ‡Ø§ â€” Ø´Ø§Ø®Øµ: ${metric}`
            }

          </h2>

          {loading ? (

            <div className="empty-state">
              Ø¯Ø± Ø­Ø§Ù„ Ø¯Ø±ÛŒØ§ÙØª Ø§Ø·Ù„Ø§Ø¹Ø§Øª...
            </div>

          ) : (

            <div className="kpi-v2-list">

              {locations.map(
                item => (

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


      {level === "unit" &&
       !unit && (

        <div className="kpi-v2-panel">

          <h2>
            ÙˆØ§Ø­Ø¯Ù‡Ø§ÛŒ Ø§Ù¾ÛŒØ¯Ù…ÛŒÙˆÙ„ÙˆÚ˜ÛŒÚ©
          </h2>

          {loading ? (

            <div className="empty-state">
              Ø¯Ø± Ø­Ø§Ù„ Ø¯Ø±ÛŒØ§ÙØª ÙˆØ§Ø­Ø¯Ù‡Ø§...
            </div>

          ) : (

            <div className="kpi-v2-list">

              {locations.map(
                item => (

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
                        marginTop: 5
                      }}
                    >
                      Ù…Ø´Ø§Ù‡Ø¯Ù‡ Ø¬Ø²Ø¦ÛŒØ§Øª Ú©Ø§Ù…Ù„ ÙˆØ§Ø­Ø¯ â†’
                    </div>

                  </div>

                )
              )}

            </div>

          )}

        </div>

      )}


      {unit &&
       unitDetail && (

        <>

          <div className="kpi-v2-panel">

            <div className="kpi-v2-unit-header">

              <div>

                <h2>
                  ÙˆØ§Ø­Ø¯:
                  {" "}
                  {unit.name}
                </h2>

                <div
                  style={{
                    color: "#789",
                    fontSize: 11
                  }}
                >
                  Ø¬Ø²Ø¦ÛŒØ§Øª Ú©Ø§Ù…Ù„ Ø¹Ù…Ù„ÛŒØ§Øª ÙˆØ§Ù‚Ø¹ÛŒ
                  Ø«Ø¨Øªâ€ŒØ´Ø¯Ù‡ Ø¨Ø±Ø§ÛŒ Ø§ÛŒÙ† ÙˆØ§Ø­Ø¯
                </div>

              </div>

            </div>

          </div>


          <div className="kpi-v2-grid">

            <Card
              label="ØªÙ…Ø§Ù… Ø¹Ù…Ù„ÛŒØ§Øª"
              value={number(
                unitDetail.cards?.all
              )}
            />

            <Card
              label="Ø¨ÛŒÙ…Ø§Ø±ÛŒ"
              value={number(
                unitDetail.cards?.disease
              )}
            />

            <Card
              label="Ù…Ø±Ø§Ù‚Ø¨Øª"
              value={number(
                unitDetail.cards?.care
              )}
            />

            <Card
              label="ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†"
              value={number(
                unitDetail.cards?.vaccination
              )}
            />

            <Card
              label="Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡"
              value={number(
                unitDetail.cards?.lab
              )}
            />

            <Card
              label="Ù†Ù…ÙˆÙ†Ù‡"
              value={number(
                unitDetail.cards?.samples
              )}
            />

            <Card
              label="Ø³Ù…Ù¾Ø§Ø´ÛŒ"
              value={number(
                unitDetail.cards?.spraying
              )}
            />

            <Card
              label="Ø§Ù…Ø­Ø§Ø¡"
              value={number(
                unitDetail.cards?.slaughter
              )}
            />

          </div>


          <UnitTimeline
            operations={
              unitDetail.operations || []
            }
            unitId={
              Number(unit.id)
            }
          />

        </>

      )}

    </div>

  );

}