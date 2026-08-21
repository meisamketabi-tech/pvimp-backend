import React from "react";
import "./Input.css";

type InputProps = {
    label?: string;
    name?: string;
    type?: React.HTMLInputTypeAttribute;
    value?: string | number;
    placeholder?: string;
    disabled?: boolean;
    required?: boolean;
    readOnly?: boolean;
    error?: string;
    hint?: string;
    prefix?: React.ReactNode;
    suffix?: React.ReactNode;
    className?: string;
    onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
};

export default function Input({
    label,
    name,
    type = "text",
    value,
    placeholder,
    disabled = false,
    required = false,
    readOnly = false,
    error,
    hint,
    prefix,
    suffix,
    className = "",
    onChange
}: InputProps) {

    return (
        <div className={`pv-input-group ${className}`}>

            {label && (
                <label
                    className="pv-input-label"
                    htmlFor={name}
                >
                    {label}

                    {required && (
                        <span className="pv-input-required">
                            *
                        </span>
                    )}
                </label>
            )}

            <div
                className={[
                    "pv-input-wrapper",
                    error ? "pv-input-wrapper-error" : "",
                    disabled ? "pv-input-wrapper-disabled" : ""
                ].join(" ")}
            >

                {prefix && (
                    <span className="pv-input-prefix">
                        {prefix}
                    </span>
                )}

                <input
                    id={name}
                    name={name}
                    type={type}
                    value={value}
                    placeholder={placeholder}
                    disabled={disabled}
                    required={required}
                    readOnly={readOnly}
                    className="pv-input"
                    onChange={onChange}
                />

                {suffix && (
                    <span className="pv-input-suffix">
                        {suffix}
                    </span>
                )}

            </div>

            {error && (
                <div className="pv-input-message pv-input-error">
                    {error}
                </div>
            )}

            {!error && hint && (
                <div className="pv-input-message pv-input-hint">
                    {hint}
                </div>
            )}

        </div>
    );
}
