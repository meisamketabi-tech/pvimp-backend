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
    title: string;
    province?: string;
    county?: string;
    latitude?: number;
    longitude?: number;
    unit_type?: string;
    is_active?: boolean;
}

export default function Dashboard() {
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [gisPoints, setGisPoints] = useState<GISPoint[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadDashboard = async () => {
            try {
                const [statsResponse, gisResponse] = await Promise.all([
                    api.get<DashboardStats>("/organization/dashboard"),
                    api.get<GISPoint[]>("/gis-dashboard/map-points"),
                ]);

                setStats(statsResponse.data);
                setGisPoints(gisResponse.data);
            } catch (error) {
                console.error("Dashboard loading error:", error);
            } finally {
                setLoading(false);
            }
        };

        loadDashboard();
    }, []);

    const cards = [
        {
            title: "واحدهای سازمانی فعال",
            value: stats?.total_units ?? 0,
            desc: "واحدهای فعال در ساختار سازمانی",
        },
        {
            title: "کاربران فعال",
            value: stats?.total_users ?? 0,
            desc: "کاربران دارای انتساب فعال",
        },
        {
            title: "پست‌های سازمانی",
            value: stats?.total_positions ?? 0,
            desc: "مجموع پست‌های فعال سازمان",
        },
        {
            title: "پست‌های خالی",
            value: stats?.empty_positions ?? 0,
            desc: "پست‌های فعال بدون انتساب",
        },
    ];

    return (
        <div className="dashboard-page" dir="rtl">

            <div className="dashboard-header">
                <h1>
                    داشبورد مدیریتی سامانه دامپزشکی
                </h1>

                <p>
                    نمای کلی وضعیت ساختار سازمانی، عملکرد و اطلاعات مکانی
                </p>
            </div>

            <div className="dashboard-grid">

                {cards.map((item, index) => (
                    <div
                        className="dashboard-box"
                        key={index}
                    >
                        <h3>
                            {item.title}
                        </h3>

                        <strong>
                            {loading ? "..." : item.value}
                        </strong>

                        <p>
                            {item.desc}
                        </p>
                    </div>
                ))}

            </div>

            <div className="dashboard-box">

                <h2>
                    وضعیت ساختار سازمانی
                </h2>

                <table>

                    <thead>
                        <tr>
                            <th>شاخص</th>
                            <th>تعداد</th>
                            <th>وضعیت</th>
                        </tr>
                    </thead>

                    <tbody>

                        <tr>
                            <td>واحدهای سازمانی فعال</td>
                            <td>{stats?.total_units ?? 0}</td>
                            <td>فعال</td>
                        </tr>

                        <tr>
                            <td>کاربران فعال</td>
                            <td>{stats?.total_users ?? 0}</td>
                            <td>فعال</td>
                        </tr>

                        <tr>
                            <td>پست‌های سازمانی</td>
                            <td>{stats?.total_positions ?? 0}</td>
                            <td>ثبت‌شده</td>
                        </tr>

                        <tr>
                            <td>پست‌های دارای مسئول</td>
                            <td>{stats?.filled_positions ?? 0}</td>
                            <td>تکمیل‌شده</td>
                        </tr>

                        <tr>
                            <td>پست‌های خالی</td>
                            <td>{stats?.empty_positions ?? 0}</td>
                            <td>نیازمند تعیین مسئول</td>
                        </tr>

                    </tbody>

                </table>

            </div>

            <div className="dashboard-box">

                <h2>
                    مراکز ثبت‌شده در GIS
                </h2>

                <table>

                    <thead>
                        <tr>
                            <th>نام مرکز</th>
                            <th>شهرستان</th>
                            <th>نوع مرکز</th>
                            <th>استان</th>
                            <th>وضعیت</th>
                        </tr>
                    </thead>

                    <tbody>

                        {gisPoints.length === 0 ? (

                            <tr>
                                <td colSpan={5}>
                                    {loading
                                        ? "در حال دریافت اطلاعات..."
                                        : "اطلاعات مکانی ثبت نشده است"}
                                </td>
                            </tr>

                        ) : (

                            gisPoints.slice(0, 10).map((point, index) => (

                                <tr key={index}>

                                    <td>{point.title || "-"}</td>

                                    <td>{point.county || "-"}</td>

                                    <td>{point.unit_type || "-"}</td>

                                    <td>{point.province || "-"}</td>

                                    <td>
                                        {point.is_active
                                            ? "فعال"
                                            : "غیرفعال"}
                                    </td>

                                </tr>

                            ))

                        )}

                    </tbody>

                </table>

            </div>

            <div className="dashboard-box">

                <h2>
                    وضعیت GIS
                </h2>

                <div className="chart-placeholder">

                    <div>

                        <strong>
                            {gisPoints.length}
                        </strong>

                        <p>
                            مرکز دارای مختصات مکانی در سامانه GIS
                        </p>

                    </div>

                </div>

            </div>

        </div>
    );
}