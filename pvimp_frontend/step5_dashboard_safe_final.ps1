$ErrorActionPreference = "Stop"
Set-Location "D:\pvimp_backend\pvimp_frontend"
$tsx = ".\src\pages\Dashboard.tsx"
if (-not (Test-Path $tsx)) { throw "Dashboard.tsx پیدا نشد" }
$backup = ".\src\pages\Dashboard.tsx.step5.safe.bak"
Copy-Item $tsx $backup -Force
Write-Host "===== STEP 5 : SAFE TSX REPLACEMENT =====" -ForegroundColor Cyan
Write-Host "Backup: $backup"

@'
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

function displayValue(value: unknown, fallback = "-"): string {
    if (value === null || value === undefined) return fallback;
    if (typeof value === "string") {
        const text = value.trim();
        return text === "" ? fallback : text;
    }
    if (typeof value === "number" || typeof value === "boolean") return String(value);
    if (typeof value === "object") {
        try { return JSON.stringify(value); } catch { return fallback; }
    }
    return String(value);
}

function displayNumber(value: unknown, fallback = 0): number {
    if (typeof value === "number" && Number.isFinite(value)) return value;
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : fallback;
}

export default function Dashboard() {
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [gisPoints, setGisPoints] = useState<GISPoint[]>([]);
    const [loading, setLoading] = useState(true);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);

    useEffect(() => {
        let mounted = true;

        const loadDashboard = async () => {
            try {
                setLoading(true);
                setErrorMessage(null);

                const [statsResponse, gisResponse] = await Promise.all([
                    api.get<DashboardStats>("/organization/dashboard"),
                    api.get<GISPoint[]>("/gis-dashboard/map-points"),
                ]);

                if (!mounted) return;

                setStats(statsResponse.data ?? null);
                setGisPoints(Array.isArray(gisResponse.data) ? gisResponse.data : []);
            } catch (error: unknown) {
                console.error("Dashboard loading error:", error);
                if (!mounted) return;

                setErrorMessage("دریافت اطلاعات داشبورد با خطا مواجه شد.");
                setStats(null);
                setGisPoints([]);
            } finally {
                if (mounted) setLoading(false);
            }
        };

        loadDashboard();
        return () => { mounted = false; };
    }, []);

    const cards = [
        { title: "واحدهای سازمانی فعال", value: displayNumber(stats?.total_units), desc: "واحدهای فعال در ساختار سازمانی" },
        { title: "کاربران فعال", value: displayNumber(stats?.total_users), desc: "کاربران دارای انتساب فعال" },
        { title: "پست‌های سازمانی", value: displayNumber(stats?.total_positions), desc: "مجموع پست‌های فعال سازمان" },
        { title: "پست‌های خالی", value: displayNumber(stats?.empty_positions), desc: "پست‌های فعال بدون انتساب" },
    ];

    return (
        <div className="dashboard-page dashboard-command-center" dir="rtl">
            <div className="dashboard-header dashboard-command-header">
                <h1>داشبورد مدیریتی سامانه دامپزشکی</h1>
                <p>نمای کلی وضعیت ساختار سازمانی، عملکرد و اطلاعات مکانی</p>
            </div>

            {errorMessage && (
                <div className="dashboard-box dashboard-alert-panel">
                    <div className="dashboard-alert">{errorMessage}</div>
                </div>
            )}

            <div className="dashboard-grid dashboard-kpi-grid">
                {cards.map((item, index) => (
                    <div className="dashboard-box dashboard-stat-card" key={index}>
                        <h3>{item.title}</h3>
                        <strong>{loading ? "..." : item.value}</strong>
                        <p>{item.desc}</p>
                    </div>
                ))}
            </div>

            <div className="dashboard-box dashboard-section-panel">
                <div className="dashboard-section-header">
                    <div>
                        <h2>وضعیت ساختار سازمانی</h2>
                        <p>نمای کلی وضعیت واحدها، کاربران و پست‌های سازمانی</p>
                    </div>
                </div>

                <div className="dashboard-table-wrapper">
                    <table className="dashboard-table">
                        <thead>
                            <tr><th>شاخص</th><th>تعداد</th><th>وضعیت</th></tr>
                        </thead>
                        <tbody>
                            <tr><td>واحدهای سازمانی فعال</td><td>{loading ? "..." : displayNumber(stats?.total_units)}</td><td>فعال</td></tr>
                            <tr><td>کاربران فعال</td><td>{loading ? "..." : displayNumber(stats?.total_users)}</td><td>فعال</td></tr>
                            <tr><td>پست‌های سازمانی</td><td>{loading ? "..." : displayNumber(stats?.total_positions)}</td><td>ثبت‌شده</td></tr>
                            <tr><td>پست‌های دارای مسئول</td><td>{loading ? "..." : displayNumber(stats?.filled_positions)}</td><td>تکمیل‌شده</td></tr>
                            <tr><td>پست‌های خالی</td><td>{loading ? "..." : displayNumber(stats?.empty_positions)}</td><td>نیازمند تعیین مسئول</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div className="dashboard-box dashboard-section-panel">
                <div className="dashboard-section-header">
                    <div>
                        <h2>مراکز ثبت‌شده در GIS</h2>
                        <p>آخرین مراکز دارای اطلاعات مکانی در سامانه</p>
                    </div>
                    <span className="dashboard-section-count">{loading ? "..." : gisPoints.length}</span>
                </div>

                <div className="dashboard-table-wrapper">
                    <table className="dashboard-table">
                        <thead>
                            <tr><th>نام مرکز</th><th>شهرستان</th><th>نوع مرکز</th><th>استان</th><th>وضعیت</th></tr>
                        </thead>
                        <tbody>
                            {gisPoints.length === 0 ? (
                                <tr><td colSpan={5}>{loading ? "در حال دریافت اطلاعات..." : "اطلاعات مکانی ثبت نشده است"}</td></tr>
                            ) : (
                                gisPoints.slice(0, 10).map((point, index) => (
                                    <tr key={`${displayValue(point.title, "point")}-${index}`}>
                                        <td>{displayValue(point.title)}</td>
                                        <td>{displayValue(point.county)}</td>
                                        <td>{displayValue(point.unit_type)}</td>
                                        <td>{displayValue(point.province)}</td>
                                        <td>
                                            <span className={point.is_active ? "dashboard-status dashboard-status-success" : "dashboard-status dashboard-status-danger"}>
                                                {point.is_active ? "فعال" : "غیرفعال"}
                                            </span>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>

                {gisPoints.length > 10 && (
                    <div className="dashboard-table-footer">
                        نمایش ۱۰ مرکز از مجموع {gisPoints.length} مرکز
                    </div>
                )}
            </div>

            <div className="dashboard-box dashboard-section-panel">
                <div className="dashboard-section-header">
                    <div>
                        <h2>وضعیت GIS</h2>
                        <p>تعداد مراکز دارای مختصات مکانی ثبت‌شده</p>
                    </div>
                </div>

                <div className="chart-placeholder dashboard-gis-status">
                    <div className="dashboard-gis-status-value">
                        <strong>{loading ? "..." : gisPoints.length}</strong>
                        <p>مرکز دارای مختصات مکانی در سامانه GIS</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
'@ | Set-Content $tsx -Encoding UTF8

Write-Host "Dashboard.tsx written." -ForegroundColor Green
Write-Host "===== TYPESCRIPT CHECK =====" -ForegroundColor Yellow
npx tsc -b
if ($LASTEXITCODE -ne 0) {
    Copy-Item $backup $tsx -Force
    throw "Step 5 TypeScript check failed. Original Dashboard.tsx restored."
}
Write-Host "TypeScript: PASS" -ForegroundColor Green

Write-Host "===== BUILD =====" -ForegroundColor Cyan
npm run build
if ($LASTEXITCODE -ne 0) {
    Copy-Item $backup $tsx -Force
    throw "Step 5 build failed. Original Dashboard.tsx restored."
}

Write-Host "===== STEP 5 DONE =====" -ForegroundColor Green
Write-Host "Dashboard.tsx updated successfully."
Write-Host "Backup: $backup"
Write-Host "Build: SUCCESS"
