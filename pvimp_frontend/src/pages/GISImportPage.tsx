import React, { useRef, useState } from "react";
import "./SupervisionForm.css";

export default function GISImportPage() {

    const fileInput = useRef<HTMLInputElement>(null);

    const [fileName, setFileName] = useState("");
    const [fileSize, setFileSize] = useState("");
    const [status, setStatus] = useState("فایلی انتخاب نشده است.");

    const selectFile = () => {
        fileInput.current?.click();
    };

    const onFileChanged = (e: React.ChangeEvent<HTMLInputElement>) => {

        const file = e.target.files?.[0];

        if (!file) return;

        setFileName(file.name);

        setFileSize(
            (file.size / 1024 / 1024).toFixed(2) + " MB"
        );

        setStatus("فایل آماده بارگذاری است.");
    };

    const uploadFile = () => {

        if (!fileInput.current?.files?.length) {

            alert("ابتدا فایل اکسل را انتخاب کنید.");

            return;

        }

        alert("در مرحله بعد فایل به سرور ارسال خواهد شد.");
    };

    return (

        <div
            className="dashboard-container"
            dir="rtl"
        >

            <div className="expert-header">

                <h1>
                    بارگذاری خروجی سامانه GIS
                </h1>

                <p>
                    ورود اطلاعات خروجی سامانه GIS دامپزشکی
                </p>

            </div>

            <div className="dashboard-box">

                <div className="form-section">

                    <h2>
                        انتخاب فایل
                    </h2>

                    <input
                        ref={fileInput}
                        type="file"
                        accept=".xlsx,.xls"
                        style={{ display: "none" }}
                        onChange={onFileChanged}
                    />

                    <button
                        className="upload-btn"
                        type="button"
                        onClick={selectFile}
                    >
                        انتخاب فایل Excel
                    </button>

                </div>

                <div className="form-section">

                    <h2>
                        اطلاعات فایل
                    </h2>

                    <div className="form-grid">

                        <div>

                            <label>
                                نام فایل
                            </label>

                            <input
                                value={fileName}
                                readOnly
                            />

                        </div>

                        <div>

                            <label>
                                حجم فایل
                            </label>

                            <input
                                value={fileSize}
                                readOnly
                            />

                        </div>

                    </div>

                </div>

                <div className="form-section">

                    <h2>
                        وضعیت
                    </h2>

                    <textarea
                        value={status}
                        rows={4}
                        readOnly
                    />

                </div>

                <div
                    style={{
                        display: "flex",
                        justifyContent: "center",
                        marginTop: "20px"
                    }}
                >

                    <button
                        className="upload-btn"
                        type="button"
                        onClick={uploadFile}
                    >
                        بارگذاری فایل
                    </button>

                </div>

            </div>

        </div>

    );

}