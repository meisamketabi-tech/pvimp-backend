import React from "react";
import "./Button.css";

type ButtonVariant =
    | "primary"
    | "secondary"
    | "danger"
    | "success"
    | "warning"
    | "ghost";

type ButtonSize = "sm" | "md" | "lg";

type ButtonProps = {
    children: React.ReactNode;
    type?: "button" | "submit" | "reset";
    variant?: ButtonVariant;
    size?: ButtonSize;
    disabled?: boolean;
    loading?: boolean;
    fullWidth?: boolean;
    icon?: React.ReactNode;
    className?: string;
    onClick?: (
        event: React.MouseEvent<HTMLButtonElement>
    ) => void;
};

export default function Button({
    children,
    type = "button",
    variant = "primary",
    size = "md",
    disabled = false,
    loading = false,
    fullWidth = false,
    icon,
    className = "",
    onClick
}: ButtonProps) {
    const classes = [
        "pv-button",
        `pv-button-${variant}`,
        `pv-button-${size}`,
        fullWidth ? "pv-button-full" : "",
        loading ? "pv-button-loading" : "",
        className
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <button
            type={type}
            disabled={disabled || loading}
            className={classes}
            onClick={onClick}
        >
            {loading ? (
                <span className="pv-button-spinner" aria-hidden="true" />
            ) : icon ? (
                <span className="pv-button-icon" aria-hidden="true">
                    {icon}
                </span>
            ) : null}

            <span className="pv-button-content">
                {loading ? "در حال پردازش..." : children}
            </span>
        </button>
    );
}