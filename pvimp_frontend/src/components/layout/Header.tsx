import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "../../store/auth.store";
import "./Header.css";

export default function Header() {
    const navigate = useNavigate();
    const user = useAuthStore((state) => state.user);
    const token = useAuthStore((state) => state.token);
    const logout = useAuthStore((state) => state.logout);

    const displayName = user?.full_name || user?.username || "کاربر سامانه";
    const role = user?.role || "کاربر احراز هویت‌شده";
    const initial = displayName.trim().charAt(0) || "ک";

    function handleLogout() {
        logout();
        navigate("/login", { replace: true });
    }

    return (
        <header className="app-header" dir="rtl">
            <div className="app-header__right">
                <div className="app-header__icon">دام</div>
                <div className="app-header__titles">
                    <h1>سامانه مدیریت یکپارچه دامپزشکی</h1>
                    <span>اداره کل دامپزشکی استان زنجان</span>
                </div>
            </div>

            <div className="app-header__left">
                <div className={`app-header__status ${token ? "is-authenticated" : "is-guest"}`}>
                    <span className="app-header__status-dot" />
                    {token ? "وضعیت: آنلاین و واردشده" : "وضعیت: وارد نشده"}
                </div>

                <div className="app-header__user">
                    <div className="app-header__avatar">{initial}</div>
                    <div className="app-header__user-info">
                        <strong>{displayName}</strong>
                        <span>{role}</span>
                    </div>
                    <button
                        type="button"
                        className="app-header__logout"
                        onClick={handleLogout}
                        title="خروج از حساب کاربری"
                        aria-label="خروج از حساب کاربری"
                    >
                        خروج
                    </button>
                </div>
            </div>
        </header>
    );
}
