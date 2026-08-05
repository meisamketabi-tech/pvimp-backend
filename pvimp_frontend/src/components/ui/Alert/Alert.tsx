import React from "react";
import "./Alert.css";

type AlertVariant = "info" | "success" | "warning" | "error";

type AlertProps = {
    variant?: AlertVariant;
    title?: string;
    icon?: React.ReactNode;
    onClose?: () => void;
    className?: string;
    children: React.ReactNode;
};

const defaultIcons: Record<AlertVariant, React.ReactNode> = {
    info: "ℹ",
    success: "✓",
    warning: "⚠",
    error: "×"
};

export default function Alert({
    variant = "info",
    title,
    icon,
    onClose,
    className = "",
    children
}: AlertProps) {
    return (
        <div
            className={[
                "pv-alert",
                `pv-alert-${variant}`,
                className
            ]
                .filter(Boolean)
                .join(" ")}
            role="alert"
        >
            <div
                className="pv-alert-icon"
                aria-hidden="true"
            >
                {icon ?? defaultIcons[variant]}
            </div>

            <div className="pv-alert-content">
                {title && (
                    <div className="pv-alert-title">
                        {title}
                    </div>
                )}

                <div className="pv-alert-message">
                    {children}
                </div>
            </div>

            {onClose && (
                <button
                    type="button"
                    className="pv-alert-close"
                    onClick={onClose}
                    aria-label="بستن"
                >
                    ×
                </button>
            )}
        </div>
    );
}