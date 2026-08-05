import React from "react";
import "./Select.css";

type SelectOption = {
    value: string | number;
    label: string;
};

type SelectProps = {
    label?: string;
    name?: string;
    value?: string | number;
    options: SelectOption[];
    placeholder?: string;
    disabled?: boolean;
    required?: boolean;
    error?: string;
    hint?: string;
    className?: string;
    onChange?: (event: React.ChangeEvent<HTMLSelectElement>) => void;
};

export default function Select({
    label,
    name,
    value,
    options,
    placeholder = "لطفاً انتخاب کنید",
    disabled = false,
    required = false,
    error,
    hint,
    className = "",
    onChange
}: SelectProps) {

    const selectProps = {
        id: name,
        name,
        disabled,
        required,
        className: "pv-select",
        onChange
    };

    return (
        <div className={`pv-select-group ${className}`}>

            {label && (
                <label
                    className="pv-select-label"
                    htmlFor={name}
                >
                    {label}

                    {required && (
                        <span className="pv-select-required">
                            *
                        </span>
                    )}
                </label>
            )}

            <div
                className={[
                    "pv-select-wrapper",
                    error ? "pv-select-wrapper-error" : "",
                    disabled ? "pv-select-wrapper-disabled" : ""
                ].join(" ")}
            >

                {value !== undefined ? (
                    <select
                        {...selectProps}
                        value={value}
                    >
                        <option value="" disabled>
                            {placeholder}
                        </option>

                        {options.map((option) => (
                            <option
                                key={String(option.value)}
                                value={option.value}
                            >
                                {option.label}
                            </option>
                        ))}
                    </select>
                ) : (
                    <select
                        {...selectProps}
                        defaultValue=""
                    >
                        <option value="" disabled>
                            {placeholder}
                        </option>

                        {options.map((option) => (
                            <option
                                key={String(option.value)}
                                value={option.value}
                            >
                                {option.label}
                            </option>
                        ))}
                    </select>
                )}

                <span
                    className="pv-select-arrow"
                    aria-hidden="true"
                >
                    ▼
                </span>

            </div>

            {error && (
                <div className="pv-select-message pv-select-error">
                    {error}
                </div>
            )}

            {!error && hint && (
                <div className="pv-select-message pv-select-hint">
                    {hint}
                </div>
            )}

        </div>
    );
}