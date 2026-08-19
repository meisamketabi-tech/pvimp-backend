import React, { useEffect, useState } from "react";

import {
    getNotifications,
    markRead
} from "../services/notificationService";

type NotificationItem = {
    id: number;
    is_read: boolean;
    title?: string;
    message?: string;
};

export default function NotificationBell() {
    const [items, setItems] = useState<NotificationItem[]>([]);
    const [open, setOpen] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        let mounted = true;

        setLoading(true);

        getNotifications(1)
            .then((response) => {
                if (mounted) {
                    setItems(response.data ?? []);
                }
            })
            .catch(() => {
                if (mounted) {
                    setItems([]);
                }
            })
            .finally(() => {
                if (mounted) {
                    setLoading(false);
                }
            });

        return () => {
            mounted = false;
        };
    }, []);

    const unreadCount = items.filter(
        (item) => !item.is_read
    ).length;

    async function handleNotificationClick(
        item: NotificationItem
    ) {
        if (!item.is_read) {
            try {
                await markRead(item.id);

                setItems((current) =>
                    current.map((notification) =>
                        notification.id === item.id
                            ? {
                                ...notification,
                                is_read: true
                            }
                            : notification
                    )
                );
            } catch {
                // Keep the notification state unchanged if the API fails.
            }
        }
    }

    return (
        <div
            className="pv-notification"
            dir="rtl"
        >
            <button
                type="button"
                className="pv-notification-button"
                onClick={() => setOpen((value) => !value)}
                aria-label={`اعلان‌ها${unreadCount ? `، ${unreadCount} خوانده نشده` : ""}`}
                aria-expanded={open}
            >
                <span aria-hidden="true">
                    🔔
                </span>

                {unreadCount > 0 && (
                    <span className="pv-notification-count">
                        {unreadCount}
                    </span>
                )}
            </button>

            {open && (
                <div className="pv-notification-menu">
                    {loading ? (
                        <div className="pv-notification-empty">
                            در حال بارگذاری...
                        </div>
                    ) : items.length === 0 ? (
                        <div className="pv-notification-empty">
                            اعلانی وجود ندارد.
                        </div>
                    ) : (
                        items.map((item) => (
                            <button
                                type="button"
                                key={item.id}
                                className={[
                                    "pv-notification-item",
                                    !item.is_read
                                        ? "pv-notification-item-unread"
                                        : ""
                                ]
                                    .filter(Boolean)
                                    .join(" ")}
                                onClick={() =>
                                    handleNotificationClick(item)
                                }
                            >
                                <strong>
                                    {item.title || "اعلان"}
                                </strong>

                                {item.message && (
                                    <span>
                                        {item.message}
                                    </span>
                                )}
                            </button>
                        ))
                    )}
                </div>
            )}
        </div>
    );
}