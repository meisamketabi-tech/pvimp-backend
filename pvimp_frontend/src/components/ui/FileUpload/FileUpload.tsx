import React, { useRef } from "react";
import "./FileUpload.css";

type FileUploadProps = {
    label?: string;
    accept?: string;
    file?: File | null;
    disabled?: boolean;
    error?: string;
    hint?: string;
    multiple?: boolean;
    onChange?: (files: FileList | null) => void;
};

export default function FileUpload({
    label = "فایل",
    accept,
    file,
    disabled = false,
    error,
    hint,
    multiple = false,
    onChange
}: FileUploadProps) {

    const inputRef = useRef<HTMLInputElement>(null);

    function handleClick() {
        if (!disabled) {
            inputRef.current?.click();
        }
    }

    function handleChange(
        event: React.ChangeEvent<HTMLInputElement>
    ) {
        onChange?.(event.target.files);
    }

    return (
        <div className="pv-file-upload">

            {label && (
                <label className="pv-file-upload-label">
                    {label}
                </label>
            )}

            <input
                ref={inputRef}
                type="file"
                accept={accept}
                multiple={multiple}
                disabled={disabled}
                onChange={handleChange}
                className="pv-file-upload-input"
            />

            <button
                type="button"
                disabled={disabled}
                className={[
                    "pv-file-upload-zone",
                    error ? "pv-file-upload-error" : "",
                    file ? "pv-file-upload-selected" : ""
                ].join(" ")}
                onClick={handleClick}
            >

                <span className="pv-file-upload-icon">
                    {file ? "✓" : "📎"}
                </span>

                <span className="pv-file-upload-content">

                    <strong>
                        {file
                            ? file.name
                            : "انتخاب فایل"}
                    </strong>

                    <small>
                        {file
                            ? `${(file.size / 1024 / 1024).toFixed(2)} MB`
                            : "برای انتخاب فایل کلیک کنید"}
                    </small>

                </span>

            </button>

            {error && (
                <span className="pv-file-upload-message pv-file-upload-error-text">
                    {error}
                </span>
            )}

            {!error && hint && (
                <span className="pv-file-upload-message pv-file-upload-hint">
                    {hint}
                </span>
            )}

        </div>
    );
}