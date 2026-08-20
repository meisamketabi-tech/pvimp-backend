import React, { useEffect, useMemo, useState } from "react";
import { getNotifications, markRead } from "../../services/notificationService";
import { useAuthStore } from "../../store/auth.store";
import { getToken } from "../../utils/token";
import "./NotificationBell.css";

const API = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";
type NotificationItem = { id: number; title: string; message: string; is_read: boolean; level?: string };

export default function NotificationBell() {
  const user = useAuthStore((state) => state.user);
  const [items, setItems] = useState<NotificationItem[]>([]);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [fallbackRead, setFallbackRead] = useState<number[]>(() => {
    try {
      return JSON.parse(localStorage.getItem("pvimp_fallback_read_notifications") || "[]");
    } catch {
      return [];
    }
  });

  useEffect(() => {
    let mounted = true;

    async function loadLiveAlarms() {
      const token = getToken();
      if (!token) return;

      try {
        const response = await fetch(
          `${API}/gis/disease-control-dashboard/summary`,
          {
            headers: {
              Accept: "application/json",
              Authorization: `Bearer ${token}`,
            },
          },
        );

        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();
        const alerts = Array.isArray(data?.management_alerts)
          ? data.management_alerts.slice(0, 10)
          : [];

        if (!mounted) return;

        setItems(
          alerts.map((alert: any, index: number) => ({
            id: 900000 + index,
            title: alert.title || "هشدار مدیریتی",
            message:
              alert.value != null
                ? `مقدار شاخص: ${Number(alert.value).toLocaleString("fa-IR")}`
                : "نیازمند بررسی مدیریتی",
            is_read: fallbackRead.includes(900000 + index),
            level: alert.level,
          })),
        );
      } catch {
        if (mounted) setItems([]);
      }
    }

    async function load() {
      if (!getToken()) {
        if (mounted) setItems([]);
        return;
      }

      try {
        setLoading(true);

        if (user?.id) {
          const response = await getNotifications(user.id);
          const serverItems = Array.isArray(response.data) ? response.data : [];

          if (mounted && serverItems.length) {
            setItems(serverItems);
            return;
          }
        }

        await loadLiveAlarms();
      } catch {
        await loadLiveAlarms();
      } finally {
        if (mounted) setLoading(false);
      }
    }

    load();
    const timer = window.setInterval(load, 60000);

    return () => {
      mounted = false;
      window.clearInterval(timer);
    };
  }, [user?.id, fallbackRead]);

  const unread = useMemo(() => items.filter((item) => !item.is_read), [items]);

  async function readOne(item: NotificationItem) {
    if (item.is_read) return;

    if (item.id < 900000) {
      try {
        await markRead(item.id);
      } catch {
        // Keep the UI optimistic if the notification API is temporarily unavailable.
      }
    } else {
      const next = Array.from(new Set([...fallbackRead, item.id]));
      setFallbackRead(next);
      localStorage.setItem(
        "pvimp_fallback_read_notifications",
        JSON.stringify(next),
      );
    }

    setItems((previous) =>
      previous.map((notification) =>
        notification.id === item.id
          ? { ...notification, is_read: true }
          : notification,
      ),
    );
  }

  return (
    <div className="notification-wrap" dir="rtl">
      <button
        type="button"
        className={`notification-button ${unread.length ? "has-unread" : ""}`}
        onClick={() => setOpen((value) => !value)}
        aria-label="اعلان‌ها"
        aria-expanded={open}
      >
        <span className="notification-icon">🔔</span>
        {unread.length > 0 && (
          <span className="notification-count">
            {Math.min(unread.length, 10)}
          </span>
        )}
      </button>

      {open && (
        <div className="notification-panel">
          <div className="notification-head">
            <div>
              <b>آلارم‌های مدیریتی</b>
              <small>
                {unread.length
                  ? `${unread.length} پیام خوانده‌نشده`
                  : "پیام خوانده‌نشده‌ای نیست"}
              </small>
            </div>
            {unread.length > 0 && (
              <span className="notification-head-badge">
                {Math.min(unread.length, 10)} جدید
              </span>
            )}
          </div>

          <div className="notification-list">
            {loading && (
              <div className="notification-empty">در حال دریافت اعلان‌ها...</div>
            )}
            {!loading && !items.length && (
              <div className="notification-empty">
                فعلاً اعلان مدیریتی ثبت نشده است.
              </div>
            )}
            {items.slice(0, 10).map((item) => (
              <button
                type="button"
                key={item.id}
                className={`notification-item ${item.is_read ? "" : "unread"}`}
                onClick={() => readOne(item)}
              >
                <span
                  className={`notification-dot ${item.level === "CRITICAL" ? "critical" : "warning"}`}
                />
                <span className="notification-copy">
                  <b>{item.level === "CRITICAL" ? "بحرانی" : "هشدار مدیریتی"}</b>
                  <span>{item.title}</span>
                  <small>{item.message}</small>
                </span>
                {!item.is_read && <i>جدید</i>}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
