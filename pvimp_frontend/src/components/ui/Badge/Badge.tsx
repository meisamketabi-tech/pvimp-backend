import React from "react";
import "./Badge.css";

type BadgeVariant =
    | "default"
    | "primary"
    | "success"
    | "warning"
    | "danger"
    | "info";

type BadgeProps = {
    children: React.ReactNode;
    variant?: BadgeVariant;
    dot?: boolean;
    className?: string;
};

export default function Badge({
    children,
    variant = "default",
    dot = false,
    className = ""
}: BadgeProps) {

    return (
        <span
            className={[
                "pv-badge",
                `pv-badge-${variant}`,
                className
            ].join(" ")}
        >

            {dot && (
                <span
                    className="pv-badge-dot"
                    aria-hidden="true"
                />
            )}

            <span className="pv-badge-content">
                {children}
            </span>

        </span>
    );
}
