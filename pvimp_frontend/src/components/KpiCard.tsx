import React from "react";

type KpiCardProps = {
    title: string;
    value: string | number;
    icon?: React.ReactNode;
    status?: string;
    onClick?: () => void;
};

export default function KpiCard({
    title,
    value,
    icon,
    status,
    onClick
}: KpiCardProps) {
    return (
        <section
            className={[
                "pv-kpi-card",
                onClick ? "pv-kpi-card-clickable" : ""
            ]
                .filter(Boolean)
                .join(" ")}
            onClick={onClick}
            onKeyDown={(event) => {
                if (
                    onClick &&
                    (event.key === "Enter" || event.key === " ")
                ) {
                    event.preventDefault();
                    onClick();
                }
            }}
            role={onClick ? "button" : undefined}
            tabIndex={onClick ? 0 : undefined}
            dir="rtl"
        >
            <div className="pv-kpi-card-header">
                <span className="pv-kpi-card-title">
                    {title}
                </span>

                {icon && (
                    <span
                        className="pv-kpi-card-icon"
                        aria-hidden="true"
                    >
                        {icon}
                    </span>
                )}
            </div>

            <div className="pv-kpi-card-value">
                {value}
            </div>

            {status && (
                <div className="pv-kpi-card-status">
                    {status}
                </div>
            )}
        </section>
    );
}