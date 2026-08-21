import React, { useEffect, useState } from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { getCurrentUser } from "../../services/auth.service";
import { useAuthStore } from "../../store/auth.store";
import { removeToken } from "../../utils/token";

export default function AuthGuard() {
    const location = useLocation();
    const token = useAuthStore((state) => state.token);
    const user = useAuthStore((state) => state.user);
    const setUser = useAuthStore((state) => state.setUser);
    const logout = useAuthStore((state) => state.logout);
    const [checking, setChecking] = useState(Boolean(token) && !user);

    useEffect(() => {
        let active = true;

        async function hydrateUser() {
            if (!token) {
                if (active) setChecking(false);
                return;
            }

            if (user) {
                if (active) setChecking(false);
                return;
            }

            try {
                const currentUser = await getCurrentUser();
                if (active) setUser(currentUser);
            } catch (error) {
                console.warn("AUTH SESSION INVALID", error);
                removeToken();
                logout();
            } finally {
                if (active) setChecking(false);
            }
        }

        void hydrateUser();

        return () => {
            active = false;
        };
    }, [token, user, setUser, logout]);

    if (!token) {
        return <Navigate to="/login" replace state={{ from: location.pathname }} />;
    }

    if (checking) {
        return (
            <div className="auth-loading" dir="rtl">
                <div className="auth-loading__spinner" />
                <strong>در حال بررسی نشست کاربر...</strong>
                <span>لطفاً چند لحظه صبر کنید</span>
            </div>
        );
    }

    return <Outlet />;
}
