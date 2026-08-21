import React, { useEffect, useState } from "react";
import { Outlet } from "react-router-dom";

import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";

import "./MainLayout.css";

export default function MainLayout() {

    const [sidebarOpen, setSidebarOpen] = useState(false);

    useEffect(() => {

        function handleResize() {

            if (window.innerWidth > 900) {
                setSidebarOpen(false);
            }
        }

        window.addEventListener("resize", handleResize);

        return () => {
            window.removeEventListener("resize", handleResize);
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
                aria-expanded={sidebarOpen}
            >
                <span />
                <span />
                <span />
            </button>

            <Sidebar
                mobileOpen={sidebarOpen}
                onMobileClose={() => setSidebarOpen(false)}
            />

            <div className="main-layout__content">

                <Header />

                <main className="main-layout__page">
                    <Outlet />
                </main>

            </div>

        </div>
    );
}
