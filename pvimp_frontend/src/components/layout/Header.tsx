import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getCurrentUser } from "../../services/auth.service";
import { useAuthStore } from "../../store/auth.store";
import NotificationBell from "./NotificationBell";
import "./Header.css";

export default function Header() {
  const navigate = useNavigate();
  const user = useAuthStore((state) => state.user);
  const setUser = useAuthStore((state) => state.setUser);
  const logout = useAuthStore((state) => state.logout);
  const [authLoading, setAuthLoading] = useState(!user);

  useEffect(() => {
    let mounted = true;

    if (user) {
      setAuthLoading(false);
      return () => {
        mounted = false;
      };
    }

    setAuthLoading(true);
    getCurrentUser()
      .then((currentUser) => {
        if (mounted) setUser(currentUser);
      })
      .catch(() => {
        if (mounted) {
          logout();
          navigate("/login", { replace: true });
        }
      })
      .finally(() => {
        if (mounted) setAuthLoading(false);
      });

    return () => {
      mounted = false;
    };
  }, [user, setUser, logout, navigate]);

  const displayName = user?.full_name?.trim() || user?.username || "کاربر سامانه";
  const role = user?.role || user?.roles?.[0] || "کاربر سامانه";
  const isAuthenticated = Boolean(user);

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
        {isAuthenticated && <NotificationBell />}

        <div className={`app-header__status ${isAuthenticated ? "is-authenticated" : ""}`}>
          <span className="app-header__status-dot" />
          {authLoading ? "در حال بررسی ورود" : isAuthenticated ? "وارد شده" : "خارج از حساب"}
        </div>

        <div className="app-header__user">
          <div className="app-header__avatar">
            {displayName.charAt(0) || "ک"}
          </div>
          <div className="app-header__user-info">
            <strong>{displayName}</strong>
            <span>{role}</span>
          </div>
        </div>

        {isAuthenticated && (
          <button
            type="button"
            className="app-header__logout"
            onClick={handleLogout}
            title="خروج از حساب کاربری"
          >
            خروج
          </button>
        )}
      </div>
    </header>
  );
}
