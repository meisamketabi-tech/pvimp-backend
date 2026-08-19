import React from "react";

type AlertLevel = "danger" | "warning" | "success";

type AlertItem = {
    level: AlertLevel;
    text: string;
};

type AlertPanelProps = {
    alerts?: AlertItem[];
};

const defaultAlerts: AlertItem[] = [
    {
        level: "danger",
        text: "نیاز به بررسی فوری برخی موارد ثبت‌شده وجود دارد."
    },
    {
        level: "warning",
        text: "برخی موارد نیازمند پیگیری کارشناسی هستند."
    },
    {
        level: "success",
        text: "آخرین پایش PPR با موفقیت ثبت شده است."
    }
];

const icons: Record<AlertLevel, string> = {
    danger: "!",
    warning: "⚠",
    success: "✓"
};

export default function AlertPanel({
    alerts = defaultAlerts
}: AlertPanelProps) {
    return (
        <section
            className="pv-alert-panel"
            dir="rtl"
            aria-label="هشدارها"
        >
            {alerts.map((alert, index) => (
                <div
                    key={`${alert.level}-${index}`}
                    className={`pv-alert-item pv-alert-item-${alert.level}`}
                >
                    <span
                        className="pv-alert-item-icon"
                        aria-hidden="true"
                    >
                        {icons[alert.level]}
                    </span>

                    <span className="pv-alert-item-text">
                        {alert.text}
                    </span>
                </div>
            ))}
        </section>
    );
}