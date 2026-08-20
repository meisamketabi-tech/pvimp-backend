import React, { useEffect, useMemo, useState } from "react";
import { getCurrentUser } from "../../services/auth.service";
import { getNotifications, markRead } from "../../services/notificationService";
import "./NotificationBell.css";

type NotificationItem = { id: number; title: string; message: string; is_read: boolean; level?: string };

export default function NotificationBell() {
  const [items, setItems] = useState<NotificationItem[]>([]);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let mounted = true;
    async function load() {
      try {
        setLoading(true);
        const user = await getCurrentUser();
        const response = await getNotifications(user.id);
        if (mounted) setItems(Array.isArray(response.data) ? response.data : []);
      } catch {
        if (mounted) setItems([]);
      } finally {
        if (mounted) setLoading(false);
      }
    }
    load();
    const timer = window.setInterval(load, 60000);
    return () => { mounted = false; window.clearInterval(timer); };
  }, []);

  const unread = useMemo(() => items.filter((x) => !x.is_read), [items]);

  async function readOne(item: NotificationItem) {
    if (item.is_read) return;
    try { await markRead(item.id); } catch { /* UI still updates optimistically */ }
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
          <div className="notification-head">
            <div><b>آلارم‌های مدیریتی</b><small>{unread.length ? `${unread.length} پیام خوانده‌نشده` : "پیام خوانده‌نشده‌ای نیست"}</small></div>
            {unread.length > 0 && <span className="notification-head-badge">{Math.min(unread.length, 10)} جدید</span>}
          </div>
          <div className="notification-list">
            {loading && <div className="notification-empty">در حال دریافت اعلان‌ها...</div>}
            {!loading && !items.length && <div className="notification-empty">فعلاً اعلان مدیریتی ثبت نشده است.</div>}
            {items.slice(0, 10).map((item) => (
              <button key={item.id} className={`notification-item ${item.is_read ? "" : "unread"}`} onClick={() => readOne(item)}>
                <span className={`notification-dot ${item.level === "CRITICAL" ? "critical" : "warning"}`} />
                <span className="notification-copy"><b>{item.level === "CRITICAL" ? "بحرانی" : "هشدار مدیریتی"}</b><span>{item.title}</span><small>{item.message}</small></span>
                {!item.is_read && <i>جدید</i>}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
