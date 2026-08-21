import React from "react";
import "./Spinner.css";

type SpinnerSize = "sm" | "md" | "lg";

type SpinnerProps = {
    size?: SpinnerSize;
    label?: string;
    overlay?: boolean;
    className?: string;
};

export default function Spinner({
    size = "md",
    label,
    overlay = false,
    className = ""
}: SpinnerProps) {
    const spinner = (
        <div
            className={`pv-spinner pv-spinner-${size} ${className}`}
            role="status"
            aria-label={label || "در حال بارگذاری"}
        >
            <span className="pv-spinner-circle" />

            {label && (
                <span className="pv-spinner-label">
                    {label}
                </span>
            )}
        </div>
    );

    if (overlay) {
        return (
            <div className="pv-spinner-overlay">
                {spinner}
            </div>
        );
    }

    return spinner;
}