import React from "react";
import "./Card.css";

type CardProps = {
    children: React.ReactNode;
    title?: string;
    subtitle?: string;
    icon?: React.ReactNode;
    actions?: React.ReactNode;
    variant?: "default" | "accent" | "success" | "warning";
    className?: string;
    onClick?: () => void;
};

export default function Card({
    children,
    title,
    subtitle,
    icon,
    actions,
    variant = "default",
    className = "",
    onClick
}: CardProps) {

    const clickable = Boolean(onClick);

    return (
        <section
            className={[
                "pv-card",
                `pv-card-${variant}`,
                clickable ? "pv-card-clickable" : "",
                className
            ].join(" ")}
            onClick={onClick}
            role={clickable ? "button" : undefined}
            tabIndex={clickable ? 0 : undefined}
            onKeyDown={(event) => {

                if (
                    clickable &&
                    (event.key === "Enter" || event.key === " ")
                ) {

                    event.preventDefault();
                    onClick?.();

                }

            }}
        >

            {(title || subtitle || icon || actions) && (
                <header className="pv-card-header">

                    <div className="pv-card-heading">

                        {icon && (
                            <div className="pv-card-icon">
                                {icon}
                            </div>
                        )}

                        {(title || subtitle) && (
                            <div className="pv-card-title-area">

                                {title && (
                                    <h3 className="pv-card-title">
                                        {title}
                                    </h3>
                                )}

                                {subtitle && (
                                    <p className="pv-card-subtitle">
                                        {subtitle}
                                    </p>
                                )}

                            </div>
                        )}

                    </div>

                    {actions && (
                        <div className="pv-card-actions">
                            {actions}
                        </div>
                    )}

                </header>
            )}

            <div className="pv-card-body">
                {children}
            </div>

        </section>
    );
}
