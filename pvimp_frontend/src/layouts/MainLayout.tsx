import React, { useState } from "react";
import { Outlet } from "react-router-dom";
import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";
import "./MainLayout.css";

export default function MainLayout() {
    const [sidebarOpen, setSidebarOpen] = useState(false);

    return (
        <div className="main-layout">

            <button
                className="mobile-menu-button"
                onClick={() => setSidebarOpen(true)}
                aria-label="??? ???? ???"
            >
                ?
            </button>

            {sidebarOpen && (
                <div
                    className="mobile-sidebar-overlay"
                    onClick={() => setSidebarOpen(false)}
                />
            )}

            <Sidebar
                mobileOpen={sidebarOpen}
                onMobileClose={() => setSidebarOpen(false)}
            />

            <div className="main-content">
                <Header />

                <main className="page-content">
                    <Outlet />
                </main>
            </div>

        </div>
    );
}
