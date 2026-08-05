import React from "react";
import "./Textarea.css";

type TextareaProps = {
    label?: string;
    name?: string;
    value?: string;
    placeholder?: string;
    rows?: number;
    disabled?: boolean;
    required?: boolean;
    readOnly?: boolean;
    error?: string;
    hint?: string;
    className?: string;
    onChange?: (event: React.ChangeEvent<HTMLTextAreaElement>) => void;
};

export default function Textarea({
    label,
    name,
    value,
    placeholder,
    rows = 4,
    disabled = false,
    required = false,
    readOnly = false,
    error,
    hint,
    className = "",
    onChange
}: TextareaProps) {

    return (
        <div className={`pv-textarea-group ${className}`}>

            {label && (
                <label
                    className="pv-textarea-label"
                    htmlFor={name}
                >
                    {label}

                    {required && (
                        <span className="pv-textarea-required">
                            *
                        </span>
                    )}
                </label>
            )}

            <textarea
                id={name}
                name={name}
                value={value}
                placeholder={placeholder}
                rows={rows}
                disabled={disabled}
                required={required}
                readOnly={readOnly}
                className={[
                    "pv-textarea",
                    error ? "pv-textarea-error" : ""
                ].join(" ")}
                onChange={onChange}
            />

            {error && (
                <div className="pv-textarea-message pv-textarea-error-text">
                    {error}
                </div>
            )}

            {!error && hint && (
                <div className="pv-textarea-message pv-textarea-hint">
                    {hint}
                </div>
            )}

        </div>
    );
}
