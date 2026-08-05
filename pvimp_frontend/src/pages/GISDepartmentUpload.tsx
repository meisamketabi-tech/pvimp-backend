import React, { useEffect, useState } from "react";
import api from "../services/api";

const forms = [
    {
        title: "سابقه عملیات در واحد دامی",
        code: "operation_history"
    },
    {
        title: "مبارزه با انگل‌ها",
        code: "spraying"
    },
    {
        title: "کشتار و معدوم سازی",
        code: "slaughter_disposal"
    },
    {
        title: "ثبت جواب آزمایش",
        code: "laboratory_result"
    },
    {
        title: "ارسال نمونه",
        code: "send_sample_detail"
    },
    {
        title: "بروز بیماری",
        code: "disease_occurrence"
    },
    {
        title: "پایش و مراقبت",
        code: "surveillance"
    },
    {
        title: "گزارش بیماری",
        code: "disease_report"
    },
    {
        title: "اپیدمیولوژیک دام",
        code: "epidemiology_units"
    },
    {
        title: "عملکرد واکسیناسیون دام",
        code: "vaccination_performance"
    },
    {
        title: "توزیع واکسن",
        code: "vaccine_distribution"
    },
    {
        title: "معدوم سازی واکسن دام",
        code: "vaccine_disposal"
    },
    {
        title: "وضعیت موجودی واکسن دام",
        code: "vaccine_inventory"
    }
];

export default function GISDepartmentUpload() {

    const [files, setFiles] = useState<any>({});

    const [lastFiles, setLastFiles] = useState<any>({});

    const [message, setMessage] = useState("");
    useEffect(() => {
        loadFiles();
    }, []);

    async function loadFiles() {

        try {

            const res = await api.get(
                "/gis/import/disease-control/files"
            );

            const mapped: any = {};

            res.data.forEach((item: any) => {

                mapped[item.form] = item.filename;

            });

            setLastFiles(mapped);

        } catch (e) {

            console.log(e);

        }

    }

    function selectFile(
        code: string,
        e: any
    ) {

        setFiles({

            ...files,

            [code]:
                e.target.files?.[0]

        });

    }

    async function upload(code: string) {

        const file = files[code];

        if (!file) {
            alert("ابتدا فایل را انتخاب کنید");
            return;
        }

        const formData = new FormData();

        formData.append("file", file);

        try {

            // مرحله اول : Upload

            formData.append(
                "code",
                code
            );

            await api.post(
                "/gis/import/disease-control/upload",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }
            );

            // مرحله دوم : فقط اگر فایل اپیدمیولوژی بود Import کن

            if (code === "epidemiology_units") {

                await api.post(
                    "/gis/import/disease-control/epidemiology-units/import"
                );

            }

            setMessage("فایل با موفقیت ارسال شد");

            await loadFiles();

        }
        catch (e: any) {

            console.log(e);

            setMessage(
                JSON.stringify(
                    e.response?.data || e.message
                )
            );

        }

    }

    function getSelectedFile(
        code: string
    ) {

        if (!files[code]) {
            return "No file chosen";
        }

        return files[code].name;

    }
    return (

        <div
            dir="rtl"
            style={{
                padding: "30px"
            }}
        >

            <h2>
                اداره مبارزه با بیماری‌های دامی
            </h2>

            <h3>
                ورود اطلاعات GIS
            </h3>

            <table
                border={1}
                width="100%"
                cellPadding={8}
            >

                <thead>

                    <tr>

                        <th>فرم</th>

                        <th>فایل انتخابی</th>

                        <th>آپلود</th>

                        <th>آخرین فایل</th>

                    </tr>

                </thead>

                <tbody>

                    {

                        forms.map(item => (

                            <tr key={item.code}>

                                <td>

                                    {item.title}

                                </td>

                                <td>

                                    <input

                                        type="file"

                                        accept=".xlsx,.xls"

                                        onChange={

                                            e =>
                                                selectFile(
                                                    item.code,
                                                    e
                                                )

                                        }

                                    />

                                    <br />

                                    <span>

                                        {
                                            getSelectedFile(
                                                item.code
                                            )
                                        }

                                    </span>

                                </td>

                                <td>

                                    <button

                                        onClick={
                                            () =>
                                                upload(
                                                    item.code
                                                )
                                        }

                                    >

                                        آپلود

                                    </button>

                                </td>

                                <td>

                                    {

                                        lastFiles[item.code] ??

                                        ""

                                    }

                                </td>

                            </tr>

                        ))

                    }

                </tbody>

            </table>
            {

                message &&

                <h3>

                    {message}

                </h3>

            }

        </div>

    );

}