import React from "react";

const alerts = [
    {
        level: "danger",
        text: "واحدهای دارای پوشش واکسیناسیون پایین نیازمند بررسی فوری هستند",
    },
    {
        level: "warning",
        text: "تعداد ثبت عملیات در برخی واحدها کمتر از حد انتظار است",
    },
    {
        level: "success",
        text: "وضعیت کنترل بیماری PPR در محدوده مطلوب قرار دارد",
    },
];

export default function AlertPanel() {
    return (
        <div className="dashboard-box">
            <h2>
                هشدارهای مدیریتی
            </h2>

            {alerts.map((a, i) => (
                <div
                    className={`alert ${a.level}`}
                    key={i}
                >
                    {a.level === "danger"
                        ? "⚠️"
                        : a.level === "warning"
                            ? "🔔"
                            : "✅"}

                    &nbsp;

                    {a.text}
                </div>
            ))}
        </div>
    );
}