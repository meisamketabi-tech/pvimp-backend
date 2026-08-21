import React, { useState } from "react";

import {
    uploadAttachment
} from "../services/attachmentService";

type FileUploaderProps = {
    entity: string;
    entityId: number;
};

export default function FileUploader({
    entity,
    entityId
}: FileUploaderProps) {
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState("");

    async function upload() {
        if (!file || uploading) {
            return;
        }

        setUploading(true);
        setMessage("");

        try {
            await uploadAttachment(
                entity,
                entityId,
                file
            );

            setMessage("فایل با موفقیت بارگذاری شد.");
        } catch {
            setMessage(
                "بارگذاری فایل با خطا مواجه شد."
            );
        } finally {
            setUploading(false);
        }
    }

    return (
        <div
            className="pv-file-uploader"
            dir="rtl"
        >
            <input
                type="file"
                disabled={uploading}
                onChange={(event) => {
                    setFile(
                        event.target.files?.[0] || null
                    );
                    setMessage("");
                }}
            />

            <button
                type="button"
                disabled={!file || uploading}
                onClick={upload}
            >
                {uploading
                    ? "در حال بارگذاری..."
                    : "بارگذاری فایل"}
            </button>

            {file && (
                <small>
                    فایل انتخاب‌شده: {file.name}
                </small>
            )}

            {message && (
                <small>
                    {message}
                </small>
            )}
        </div>
    );
}