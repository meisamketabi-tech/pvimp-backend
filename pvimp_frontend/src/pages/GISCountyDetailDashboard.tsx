import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getToken } from "../utils/token";

type Unit = {
    unit_id: number;
    unit_code: string;
    unit_name: string | null;
    province_name: string | null;
    county_name: string | null;
    unit_type: string | null;
    total_animals: number;
    vaccinated_animals: number;
    remaining_animals: number;
    coverage_percent: number;
    adverse_events: number;
    status: string;
};

type CountyResponse = {
    county_id: number;
    county_code: string | null;
    county_name: string | null;
    province_name: string | null;
    units_count: number;
    units: Unit[];
};

const API_BASE =
    import.meta.env.VITE_API_BASE_URL ||
    "http://127.0.0.1:8000/api/v1";

function formatNumber(value: number | null | undefined) {
    return new Intl.NumberFormat("fa-IR").format(value || 0);
}

function statusText(status: string) {
    switch (status) {
        case "CRITICAL":
            return "بحرانی";
        case "WARNING":
            return "نیازمند توجه";
        case "ON_TRACK":
            return "مطلوب";
        case "EXCELLENT":
            return "عالی";
        default:
            return status || "-";
    }
}

function statusStyle(status: string): React.CSSProperties {
    if (status === "CRITICAL") {
        return {
            background: "#fee2e2",
            color: "#991b1b",
            fontWeight: 700,
        };
    }

    if (status === "WARNING") {
        return {
            background: "#fef3c7",
            color: "#92400e",
            fontWeight: 700,
        };
    }

    if (status === "EXCELLENT" || status === "ON_TRACK") {
        return {
            background: "#dcfce7",
            color: "#166534",
            fontWeight: 700,
        };
    }

    return {};
}

export default function GISCountyDetailDashboard() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();

    const [data, setData] =
        useState<CountyResponse | null>(null);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState<string | null>(null);

    useEffect(() => {
        if (!id) {
            setError("شناسه شهرستان ارسال نشده است.");
            setLoading(false);
            return;
        }

        const controller = new AbortController();

        async function load() {
            try {
                setLoading(true);
                setError(null);

                const response = await fetch(
                    `${API_BASE}/gis/county/${id}`,
                    {
                        headers: {
                            Accept: "application/json",
                            Authorization:
                                `Bearer ${getToken()}`,
                        },
                        signal: controller.signal,
                    }
                );

                if (!response.ok) {
                    throw new Error(
                        `HTTP ${response.status}`
                    );
                }

                const result =
                    await response.json();

                setData(result);
            } catch (err) {
                if (
                    err instanceof DOMException &&
                    err.name === "AbortError"
                ) {
                    return;
                }

                setError(
                    err instanceof Error
                        ? err.message
                        : "خطا در دریافت اطلاعات شهرستان"
                );
            } finally {
                setLoading(false);
            }
        }

        load();

        return () => controller.abort();
    }, [id]);

    return (
        <div
            style={{
                padding: 24,
                direction: "rtl",
            }}
        >
            <button
                type="button"
                onClick={() => navigate(-1)}
                style={{
                    marginBottom: 20,
                    padding: "8px 16px",
                    cursor: "pointer",
                }}
            >
                بازگشت
            </button>

            <h1>
                جزئیات شهرستان{" "}
                {data?.county_name || id}
            </h1>

            <p>
                اطلاعات واحدهای اپیدمیولوژیک شهرستان
            </p>

            {loading && (
                <div className="panel">
                    در حال دریافت اطلاعات...
                </div>
            )}

            {error && (
                <div
                    className="panel"
                    style={{
                        color: "#991b1b",
                        background: "#fee2e2",
                        padding: 16,
                    }}
                >
                    خطا: {error}
                </div>
            )}

            {!loading && !error && data && (
                <>
                    <div
                        style={{
                            display: "grid",
                            gridTemplateColumns:
                                "repeat(auto-fit,minmax(180px,1fr))",
                            gap: 16,
                            marginBottom: 24,
                        }}
                    >
                        <div
                            className="panel"
                            style={{
                                padding: 20,
                                textAlign: "center",
                            }}
                        >
                            <div
                                style={{
                                    fontSize: 14,
                                    color: "#475569",
                                    marginBottom: 8,
                                }}
                            >
                                تعداد واحدها
                            </div>

                            <div
                                style={{
                                    fontSize: 28,
                                    fontWeight: 700,
                                }}
                            >
                                {formatNumber(data.units_count)}
                            </div>
                        </div>

                        <div
                            className="panel"
                            style={{
                                padding: 20,
                                textAlign: "center",
                            }}
                        >
                            <div
                                style={{
                                    fontSize: 14,
                                    color: "#475569",
                                    marginBottom: 8,
                                }}
                            >
                                شهرستان
                            </div>

                            <div
                                style={{
                                    fontSize: 22,
                                    fontWeight: 700,
                                }}
                            >
                                {data.county_name || "-"}
                            </div>
                        </div>

                        <div
                            className="panel"
                            style={{
                                padding: 20,
                                textAlign: "center",
                            }}
                        >
                            <div
                                style={{
                                    fontSize: 14,
                                    color: "#475569",
                                    marginBottom: 8,
                                }}
                            >
                                استان
                            </div>

                            <div
                                style={{
                                    fontSize: 22,
                                    fontWeight: 700,
                                }}
                            >
                                {data.province_name || "-"}
                            </div>
                        </div>
                    </div>

                    <div className="panel">
                        <h2>
                            لیست واحدها
                        </h2>

                        {data.units.length === 0 ? (
                            <p>
                                هیچ واحدی یافت نشد.
                            </p>
                        ) : (
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
                                            <th>کد واحد</th>
                                            <th>نام واحد</th>
                                            <th>استان</th>
                                            <th>شهرستان</th>
                                            <th>نوع واحد</th>
                                            <th>کل دام</th>
                                            <th>واکسینه</th>
                                            <th>باقی‌مانده</th>
                                            <th>پوشش</th>
                                            <th>وضعیت</th>
                                        </tr>
                                    </thead>

                                    <tbody>
                                        {data.units.map((unit) => (
                                            <tr
                                                key={unit.unit_code}
                                                style={{
                                                    borderTop:
                                                        "1px solid #ddd",
                                                }}
                                            >
                                                <td>
                                                    {unit.unit_code}
                                                </td>

                                                <td>
                                                    <button
                                                        type="button"
                                                        onClick={() =>
                                                            navigate(
                                                                `/gis/unit/${unit.unit_code}`
                                                            )
                                                        }
                                                    >
                                                        {unit.unit_name || "-"}
                                                    </button>
                                                </td>

                                                <td>
                                                    {unit.province_name || "-"}
                                                </td>

                                                <td>
                                                    {unit.county_name || "-"}
                                                </td>

                                                <td>
                                                    {unit.unit_type || "-"}
                                                </td>

                                                <td>
                                                    {formatNumber(
                                                        unit.total_animals
                                                    )}
                                                </td>

                                                <td>
                                                    {formatNumber(
                                                        unit.vaccinated_animals
                                                    )}
                                                </td>

                                                <td>
                                                    {formatNumber(
                                                        unit.remaining_animals
                                                    )}
                                                </td>

                                                <td>
                                                    {Number(
                                                        unit.coverage_percent || 0
                                                    ).toFixed(1)}
                                                    %
                                                </td>

                                                <td
                                                    style={{
                                                        ...statusStyle(
                                                            unit.status
                                                        ),
                                                        padding: "6px 10px",
                                                    }}
                                                >
                                                    {statusText(unit.status)}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </div>
                </>
            )}
        </div>
    );
}
