import React, { useEffect, useState } from "react";
import { Outlet } from "react-router-dom";
import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";
import "./MainLayout.css";

export default function MainLayout() {
    const [sidebarOpen, setSidebarOpen] = useState(false);

    function closeSidebar() {
        setSidebarOpen(false);
    }

    useEffect(() => {
        function handleResize() {
            if (window.innerWidth > 900) {
                setSidebarOpen(false);
            }
        }

        function handleEscape(event: KeyboardEvent) {
            if (event.key === "Escape") {
                setSidebarOpen(false);
            }
        }

        window.addEventListener("resize", handleResize);
        window.addEventListener("keydown", handleEscape);

        return () => {
            window.removeEventListener("resize", handleResize);
            window.removeEventListener("keydown", handleEscape);
        };
    }, []);

    useEffect(() => {
        document.body.style.overflow =
            sidebarOpen && window.innerWidth <= 900
                ? "hidden"
                : "";

        return () => {
            document.body.style.overflow = "";
        };
    }, [sidebarOpen]);

    return (
        <div className="main-layout" dir="rtl">
            <button
                type="button"
                className="mobile-menu-button"
                onClick={() => setSidebarOpen(true)}
                aria-label="باز کردن منوی اصلی"
                aria-controls="main-sidebar"
                aria-expanded={sidebarOpen}
            >
                <span />
                <span />
                <span />
            </button>

            {sidebarOpen && (
                <button
                    type="button"
                    className="mobile-sidebar-overlay"
                    onClick={closeSidebar}
                    aria-label="بستن منو"
                />
            )}

            <div id="main-sidebar">
                <Sidebar
                    mobileOpen={sidebarOpen}
                    onMobileClose={closeSidebar}
                />
            </div>

            <div className="main-layout__content">
                <Header />

                <main className="main-layout__page">
                    <Outlet />
                </main>
            </div>
        </div>
    );
}
