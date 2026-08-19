import React, { useEffect, useState } from "react";
import "./Dashboard.css";
import api from "../services/api";

interface DashboardStats {
    total_units: number;
    total_users: number;
    total_positions: number;
    filled_positions: number;
    empty_positions: number;
}

interface GISPoint {
    type: string;
    title: unknown;
    province?: unknown;
    county?: unknown;
    latitude?: number;
    longitude?: number;
    unit_type?: unknown;
    is_active?: boolean;
}

/**
 * Safely converts API values to something React can render.
 */
function displayValue(
    value: unknown,
    fallback = "-"
): string {
    if (value === null || value === undefined) {
        return fallback;
    }

    if (typeof value === "string") {
        const text = value.trim();

        return text === ""
            ? fallback
            : text;
    }

    if (
        typeof value === "number" ||
        typeof value === "boolean"
    ) {
        return String(value);
    }

    if (typeof value === "object") {
        try {
            return JSON.stringify(value);
        } catch {
            return fallback;
        }
    }

    return String(value);
}

/**
 * Safely converts an API value to a finite number.
 */
function displayNumber(
    value: unknown,
    fallback = 0
): number {
    if (
        typeof value === "number" &&
        Number.isFinite(value)
    ) {
        return value;
    }

    const parsed = Number(value);

    return Number.isFinite(parsed)
        ? parsed
        : fallback;
}

/**
 * Formats dashboard numbers consistently.
 */
function formatNumber(
    value: unknown
): string {
    return displayNumber(value).toLocaleString(
        "fa-IR"
    );
}

/**
 * Converts boolean GIS status into Persian UI text.
 */
function statusText(
    value: boolean | undefined
): string {
    return value
        ? "فعال"
        : "غیرفعال";
}

export default function Dashboard() {
    const [stats, setStats] =
        useState<DashboardStats | null>(null);

    const [gisPoints, setGisPoints] =
        useState<GISPoint[]>([]);

    const [loading, setLoading] =
        useState(true);

    const [errorMessage, setErrorMessage] =
        useState<string | null>(null);

    useEffect(() => {
        let mounted = true;

        const loadDashboard = async () => {
            try {
                setLoading(true);
                setErrorMessage(null);

                const [
                    statsResponse,
                    gisResponse,
                ] = await Promise.all([
                    api.get<DashboardStats>(
                        "/organization/dashboard"
                    ),

                    api.get<GISPoint[]>(
                        "/gis-dashboard/map-points"
                    ),
                ]);

                if (!mounted) {
                    return;
                }

                setStats(
                    statsResponse.data ?? null
                );

                if (
                    Array.isArray(
                        gisResponse.data
                    )
                ) {
                    setGisPoints(
                        gisResponse.data
                    );
                } else {
                    setGisPoints([]);
                }
            } catch (error: unknown) {
                console.error(
                    "Dashboard loading error:",
                    error
                );

                if (!mounted) {
                    return;
                }

                setErrorMessage(
                    "دریافت اطلاعات داشبورد با خطا مواجه شد."
                );

                setStats(null);
                setGisPoints([]);
            } finally {
                if (mounted) {
                    setLoading(false);
                }
            }
        };

        loadDashboard();

        return () => {
            mounted = false;
        };
    }, []);

    const cards = [
        {
            key: "units",
            title: "واحدهای سازمانی فعال",
            value: stats?.total_units,
            desc:
                "واحدهای فعال در ساختار سازمانی",
            className:
                "dashboard-stat-primary",
        },

        {
            key: "users",
            title: "کاربران فعال",
            value: stats?.total_users,
            desc:
                "کاربران دارای انتساب فعال",
            className:
                "dashboard-stat-success",
        },

        {
            key: "positions",
            title: "پست‌های سازمانی",
            value: stats?.total_positions,
            desc:
                "مجموع پست‌های فعال سازمان",
            className:
                "dashboard-stat-warning",
        },

        {
            key: "empty",
            title: "پست‌های خالی",
            value: stats?.empty_positions,
            desc:
                "پست‌های فعال بدون انتساب",
            className:
                "dashboard-stat-danger",
        },
    ];

    const filledPositions =
        displayNumber(
            stats?.filled_positions
        );

    const emptyPositions =
        displayNumber(
            stats?.empty_positions
        );

    const totalPositions =
        displayNumber(
            stats?.total_positions
        );

    const filledPercent =
        totalPositions > 0
            ? Math.round(
                (filledPositions /
                    totalPositions) *
                100
            )
            : 0;

    const activeGISCount =
        gisPoints.filter(
            (point) =>
                point.is_active !== false
        ).length;

    return (
        <div
            className="dashboard-page"
            dir="rtl"
        >
            {/* =====================================================
                HEADER
               ===================================================== */}

            <header className="dashboard-header">
                <div className="dashboard-header-content">
                    <div>
                        <div className="dashboard-eyebrow">
                            PVIMP
                        </div>

                        <h1>
                            داشبورد مدیریتی سامانه دامپزشکی
                        </h1>

                        <p>
                            نمای کلی وضعیت ساختار سازمانی،
                            عملکرد و اطلاعات مکانی سامانه
                        </p>
                    </div>

                    <div className="dashboard-header-status">
                        <span className="dashboard-status-dot" />

                        <span>
                            سامانه فعال
                        </span>
                    </div>
                </div>
            </header>

            {/* =====================================================
                ERROR
               ===================================================== */}

            {errorMessage && (
                <section className="dashboard-box dashboard-alert-box">
                    <div className="dashboard-alert">
                        <div className="dashboard-alert-icon">
                            !
                        </div>

                        <div>
                            <strong>
                                دریافت اطلاعات داشبورد با خطا مواجه شد
                            </strong>

                            <p>
                                {errorMessage}
                            </p>
                        </div>
                    </div>
                </section>
            )}

            {/* =====================================================
                KPI CARDS
               ===================================================== */}

            <section className="dashboard-section">
                <div className="dashboard-section-header">
                    <div>
                        <span className="dashboard-section-kicker">
                            شاخص‌های کلیدی
                        </span>

                        <h2>
                            وضعیت کلی سامانه
                        </h2>
                    </div>
                </div>

                <div className="dashboard-grid">
                    {cards.map(
                        (item) => (
                            <div
                                className={`dashboard-box dashboard-stat-card ${item.className}`}
                                key={item.key}
                            >
                                <div className="dashboard-stat-top">
                                    <span className="dashboard-stat-title">
                                        {item.title}
                                    </span>

                                    <span className="dashboard-stat-indicator">
                                        ●
                                    </span>
                                </div>

                                <strong className="dashboard-stat-value">
                                    {loading
                                        ? "..."
                                        : formatNumber(
                                            item.value
                                        )}
                                </strong>

                                <p className="dashboard-stat-desc">
                                    {item.desc}
                                </p>
                            </div>
                        )
                    )}
                </div>
            </section>

            {/* =====================================================
                ORGANIZATION STRUCTURE
               ===================================================== */}

            <section className="dashboard-box dashboard-section-panel">
                <div className="dashboard-section-header">
                    <div>
                        <span className="dashboard-section-kicker">
                            ORGANIZATION
                        </span>

                        <h2>
                            وضعیت ساختار سازمانی
                        </h2>
                    </div>

                    <span className="dashboard-section-badge">
                        ساختار سازمانی
                    </span>
                </div>

                <div className="dashboard-table-wrapper">
                    <table className="dashboard-table">
                        <thead>
                            <tr>
                                <th>
                                    شاخص
                                </th>

                                <th>
                                    تعداد
                                </th>

                                <th>
                                    وضعیت
                                </th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr>
                                <td>
                                    واحدهای سازمانی فعال
                                </td>

                                <td className="dashboard-number-cell">
                                    {loading
                                        ? "..."
                                        : formatNumber(
                                            stats?.total_units
                                        )}
                                </td>

                                <td>
                                    <span className="dashboard-badge dashboard-badge-success">
                                        فعال
                                    </span>
                                </td>
                            </tr>

                            <tr>
                                <td>
                                    کاربران فعال
                                </td>

                                <td className="dashboard-number-cell">
                                    {loading
                                        ? "..."
                                        : formatNumber(
                                            stats?.total_users
                                        )}
                                </td>

                                <td>
                                    <span className="dashboard-badge dashboard-badge-success">
                                        فعال
                                    </span>
                                </td>
                            </tr>

                            <tr>
                                <td>
                                    پست‌های سازمانی
                                </td>

                                <td className="dashboard-number-cell">
                                    {loading
                                        ? "..."
                                        : formatNumber(
                                            stats?.total_positions
                                        )}
                                </td>

                                <td>
                                    <span className="dashboard-badge dashboard-badge-info">
                                        ثبت‌شده
                                    </span>
                                </td>
                            </tr>

                            <tr>
                                <td>
                                    پست‌های دارای مسئول
                                </td>

                                <td className="dashboard-number-cell">
                                    {loading
                                        ? "..."
                                        : formatNumber(
                                            stats?.filled_positions
                                        )}
                                </td>

                                <td>
                                    <span className="dashboard-badge dashboard-badge-success">
                                        تکمیل‌شده
                                    </span>
                                </td>
                            </tr>

                            <tr>
                                <td>
                                    پست‌های خالی
                                </td>

                                <td className="dashboard-number-cell">
                                    {loading
                                        ? "..."
                                        : formatNumber(
                                            stats?.empty_positions
                                        )}
                                </td>

                                <td>
                                    <span className="dashboard-badge dashboard-badge-danger">
                                        نیازمند تعیین مسئول
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>

            {/* =====================================================
                POSITION STATUS
               ===================================================== */}

            <section className="dashboard-grid dashboard-secondary-grid">
                <div className="dashboard-box dashboard-section-panel">
                    <div className="dashboard-section-header">
                        <div>
                            <span className="dashboard-section-kicker">
                                POSITION
                            </span>

                            <h2>
                                وضعیت پست‌های سازمانی
                            </h2>
                        </div>
                    </div>

                    <div className="dashboard-progress-card">
                        <div className="dashboard-progress-header">
                            <span>
                                درصد پست‌های تکمیل‌شده
                            </span>

                            <strong>
                                {loading
                                    ? "..."
                                    : `${filledPercent}%`}
                            </strong>
                        </div>

                        <div className="dashboard-progress">
                            <div
                                className="dashboard-progress-bar"
                                style={{
                                    width: `${Math.min(
                                        100,
                                        Math.max(
                                            0,
                                            filledPercent
                                        )
                                    )}%`,
                                }}
                            />
                        </div>

                        <div className="dashboard-progress-footer">
                            <span>
                                دارای مسئول:
                                {" "}
                                {loading
                                    ? "..."
                                    : formatNumber(
                                        filledPositions
                                    )}
                            </span>

                            <span>
                                خالی:
                                {" "}
                                {loading
                                    ? "..."
                                    : formatNumber(
                                        emptyPositions
                                    )}
                            </span>
                        </div>
                    </div>
                </div>

                <div className="dashboard-box dashboard-section-panel">
                    <div className="dashboard-section-header">
                        <div>
                            <span className="dashboard-section-kicker">
                                GIS
                            </span>

                            <h2>
                                وضعیت اطلاعات مکانی
                            </h2>
                        </div>
                    </div>

                    <div className="dashboard-gis-summary">
                        <strong>
                            {loading
                                ? "..."
                                : formatNumber(
                                    gisPoints.length
                                )}
                        </strong>

                        <span>
                            مرکز دارای مختصات مکانی
                        </span>

                        <small>
                            مراکز فعال:
                            {" "}
                            {loading
                                ? "..."
                                : formatNumber(
                                    activeGISCount
                                )}
                        </small>
                    </div>
                </div>
            </section>

            {/* =====================================================
                GIS CENTERS
               ===================================================== */}

            <section className="dashboard-box dashboard-section-panel">
                <div className="dashboard-section-header">
                    <div>
                        <span className="dashboard-section-kicker">
                            GEOGRAPHIC INFORMATION SYSTEM
                        </span>

                        <h2>
                            مراکز ثبت‌شده در GIS
                        </h2>
                    </div>

                    <span className="dashboard-section-badge">
                        {loading
                            ? "..."
                            : `${formatNumber(
                                gisPoints.length
                            )} مرکز`}
                    </span>
                </div>

                <div className="dashboard-table-wrapper">
                    <table className="dashboard-table dashboard-gis-table">
                        <thead>
                            <tr>
                                <th>
                                    نام مرکز
                                </th>

                                <th>
                                    شهرستان
                                </th>

                                <th>
                                    نوع مرکز
                                </th>

                                <th>
                                    استان
                                </th>

                                <th>
                                    وضعیت
                                </th>
                            </tr>
                        </thead>

                        <tbody>
                            {gisPoints.length === 0 ? (
                                <tr>
                                    <td
                                        colSpan={5}
                                        className="dashboard-empty-cell"
                                    >
                                        {loading
                                            ? "در حال دریافت اطلاعات مکانی..."
                                            : "اطلاعات مکانی ثبت نشده است"}
                                    </td>
                                </tr>
                            ) : (
                                gisPoints
                                    .slice(0, 10)
                                    .map(
                                        (
                                            point,
                                            index
                                        ) => (
                                            <tr
                                                key={`${displayValue(
                                                    point.title,
                                                    "point"
                                                )}-${index}`}
                                            >
                                                <td>
                                                    <strong>
                                                        {displayValue(
                                                            point.title
                                                        )}
                                                    </strong>
                                                </td>

                                                <td>
                                                    {displayValue(
                                                        point.county
                                                    )}
                                                </td>

                                                <td>
                                                    {displayValue(
                                                        point.unit_type
                                                    )}
                                                </td>

                                                <td>
                                                    {displayValue(
                                                        point.province
                                                    )}
                                                </td>

                                                <td>
                                                    <span
                                                        className={
                                                            point.is_active
                                                                ? "dashboard-badge dashboard-badge-success"
                                                                : "dashboard-badge dashboard-badge-danger"
                                                        }
                                                    >
                                                        {statusText(
                                                            point.is_active
                                                        )}
                                                    </span>
                                                </td>
                                            </tr>
                                        )
                                    )
                            )}
                        </tbody>
                    </table>
                </div>

                {gisPoints.length > 10 && (
                    <div className="dashboard-table-footer">
                        نمایش ۱۰ مرکز اول از مجموع{" "}
                        <strong>
                            {formatNumber(
                                gisPoints.length
                            )}
                        </strong>{" "}
                        مرکز ثبت‌شده
                    </div>
                )}
            </section>

            {/* =====================================================
                GIS STATUS
               ===================================================== */}

            <section className="dashboard-box dashboard-section-panel">
                <div className="dashboard-section-header">
                    <div>
                        <span className="dashboard-section-kicker">
                            GIS STATUS
                        </span>

                        <h2>
                            وضعیت GIS
                        </h2>
                    </div>
                </div>

                <div className="dashboard-gis-status">
                    <div className="dashboard-gis-status-icon">
                        GIS
                    </div>

                    <div className="dashboard-gis-status-content">
                        <strong>
                            {loading
                                ? "..."
                                : formatNumber(
                                    gisPoints.length
                                )}
                        </strong>

                        <p>
                            مرکز دارای مختصات مکانی
                            در سامانه GIS
                        </p>
                    </div>

                    <div className="dashboard-gis-status-state">
                        <span className="dashboard-status-dot" />

                        <span>
                            {gisPoints.length > 0
                                ? "اطلاعات مکانی موجود است"
                                : "اطلاعات مکانی ثبت نشده است"}
                        </span>
                    </div>
                </div>
            </section>
        </div>
    );
}