import React, { useEffect, useMemo, useState } from "react";
import { getCurrentUser } from "../../services/auth.service";
import { getNotifications, markRead } from "../../services/notificationService";
import { getToken } from "../../utils/token";
import "./NotificationBell.css";

const API = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";
type NotificationItem = { id: number; title: string; message: string; is_read: boolean; level?: string };

export default function NotificationBell() {
  const [items, setItems] = useState<NotificationItem[]>([]);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [fallbackRead, setFallbackRead] = useState<number[]>(() => {
    try { return JSON.parse(localStorage.getItem("pvimp_fallback_read_notifications") || "[]"); } catch { return []; }
  });

  useEffect(() => {
    let mounted = true;
    async function load() {
      try {
        setLoading(true);
        const user = await getCurrentUser();
        const response = await getNotifications(user.id);
        const serverItems = Array.isArray(response.data) ? response.data : [];
        if (mounted && serverItems.length) setItems(serverItems);
        else if (mounted) await loadLiveAlarms();
      } catch {
        if (mounted) await loadLiveAlarms();
      } finally {
        if (mounted) setLoading(false);
      }
    }
    async function loadLiveAlarms() {
      try {
        const r = await fetch(`${API}/gis/disease-control-dashboard/summary`, { headers: { Accept: "application/json", Authorization: `Bearer ${getToken()}` } });
        const data = await r.json();
        const alerts = Array.isArray(data?.management_alerts) ? data.management_alerts.slice(0, 10) : [];
        setItems(alerts.map((a: any, i: number) => ({ id: 900000 + i, title: a.title, message: a.value != null ? `مقدار شاخص: ${Number(a.value).toLocaleString("fa-IR")}` : "نیازمند بررسی مدیریتی", is_read: fallbackRead.includes(900000 + i), level: a.level })));
      } catch { setItems([]); }
    }
    load();
    const timer = window.setInterval(load, 60000);
    return () => { mounted = false; window.clearInterval(timer); };
  }, [fallbackRead]);

  const unread = useMemo(() => items.filter((x) => !x.is_read), [items]);

  async function readOne(item: NotificationItem) {
    if (item.is_read) return;
    if (item.id < 900000) { try { await markRead(item.id); } catch { /* optimistic update */ } }
    else {
      const next = Array.from(new Set([...fallbackRead, item.id]));
      setFallbackRead(next);
      localStorage.setItem("pvimp_fallback_read_notifications", JSON.stringify(next));
    }
    setItems((prev) => prev.map((x) => x.id === item.id ? { ...x, is_read: true } : x));
  }

  return (
    <div className="notification-wrap" dir="rtl">
      <button className={`notification-button ${unread.length ? "has-unread" : ""}`} onClick={() => setOpen((v) => !v)} aria-label="اعلان‌ها">
        <span className="notification-icon">🔔</span>
        {unread.length > 0 && <span className="notification-count">{Math.min(unread.length, 10)}</span>}
      </button>
      {open && (
        <div className="notification-panel">
          <div className="notification-head"><div><b>آلارم‌های مدیریتی</b><small>{unread.length ? `${unread.length} پیام خوانده‌نشده` : "پیام خوانده‌نشده‌ای نیست"}</small></div>{unread.length > 0 && <span className="notification-head-badge">{Math.min(unread.length, 10)} جدید</span>}</div>
          <div className="notification-list">
            {loading && <div className="notification-empty">در حال دریافت اعلان‌ها...</div>}
            {!loading && !items.length && <div className="notification-empty">فعلاً اعلان مدیریتی ثبت نشده است.</div>}
            {items.slice(0, 10).map((item) => <button key={item.id} className={`notification-item ${item.is_read ? "" : "unread"}`} onClick={() => readOne(item)}><span className={`notification-dot ${item.level === "CRITICAL" ? "critical" : "warning"}`} /><span className="notification-copy"><b>{item.level === "CRITICAL" ? "بحرانی" : "هشدار مدیریتی"}</b><span>{item.title}</span><small>{item.message}</small></span>{!item.is_read && <i>جدید</i>}</button>)}
          </div>
        </div>
      )}
    </div>
  );
}
