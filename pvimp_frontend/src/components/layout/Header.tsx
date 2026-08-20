import React, { useEffect } from "react";
import { getCurrentUser } from "../../services/auth.service";
import { useAuthStore } from "../../store/auth.store";
import NotificationBell from "./NotificationBell";
import "./Header.css";

export default function Header() {
  const user = useAuthStore((state) => state.user);
  const setUser = useAuthStore((state) => state.setUser);

  useEffect(() => {
    if (user) return;
    getCurrentUser().then(setUser).catch(() => undefined);
  }, [user, setUser]);

  const displayName = user?.full_name || user?.username || "کاربر سامانه";
  const role = user?.role || "مدیریت استان";

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
        <NotificationBell />
        <div className="app-header__status"><span className="app-header__status-dot" />سامانه فعال</div>
        <div className="app-header__user">
          <div className="app-header__avatar">{displayName.trim().charAt(0) || "ک"}</div>
          <div className="app-header__user-info"><strong>{displayName}</strong><span>{role}</span></div>
        </div>
      </div>
    </header>
  );
}
