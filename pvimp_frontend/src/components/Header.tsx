import React from "react";

type HeaderProps = {
    title?: string;
    subtitle?: string;
    children?: React.ReactNode;
};

export default function Header({
    title = "سامانه مدیریت یکپارچه دامپزشکی",
    subtitle = "استان زنجان",
    children
}: HeaderProps) {
    return (
        <header
            className="pv-header"
            dir="rtl"
        >
            <div className="pv-header-content">
                <h1>{title}</h1>

                {subtitle && (
                    <span>{subtitle}</span>
                )}
            </div>

            {children && (
                <div className="pv-header-actions">
                    {children}
                </div>
            )}
        </header>
    );
}