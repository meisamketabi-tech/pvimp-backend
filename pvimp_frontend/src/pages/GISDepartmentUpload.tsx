import React, { useEffect, useState } from "react";
import api from "../services/api";

const forms = [
    {
        title: "سابقه عملیات در واحد دامی",
        code: "operation_history",
    },
    {
        title: "مبارزه با انگل ها",
        code: "spraying",
    },
    {
        title: "کشتار و معدوم سازی",
        code: "slaughter_disposal",
    },
    {
        title: "ثبت جواب آزمایشگاه",
        code: "laboratory_result",
    },
    {
        title: "ارسال نمونه",
        code: "send_sample_detail",
    },
    {
        title: "بروز بیماری",
        code: "disease_occurrence",
    },
    {
        title: "پایش و مراقبت",
        code: "surveillance",
    },
    {
        title: "گزارش بیماری",
        code: "disease_report",
    },
    {
        title: "واحدهای اپیدمیولوژیک دامی",
        code: "epidemiology_units",
    },
    {
        title: "عملکرد واکسیناسیون دام",
        code: "vaccination_performance",
    },
    {
        title: "توزیع واکسن",
        code: "vaccine_distribution",
    },
    {
        title: "معدوم سازی واکسن دام",
        code: "vaccine_disposal",
    },
    {
        title: "وضعیت موجودی واکسن",
        code: "vaccine_inventory",
    },
];

type ImportResult = {
    inserted?: number;
    skipped?: number;
    failed?: number;
    missing_units?: any[];
    warnings?: string[];
};

type ImportResponse = {
    status?: string;
    message?: string;
    form?: string;
    file?: string;
    result?: ImportResult;
};

type PopupData = {
    type: "success" | "warning" | "error";
    title: string;
    message: string;
    file?: string;
    result?: ImportResult;
};

export default function GISDepartmentUpload() {

    const [files, setFiles] = useState<
        Record<string, File | undefined>
    >({});

    const [lastFiles, setLastFiles] = useState<
        Record<string, string>
    >({});

    const [popup, setPopup] =
        useState<PopupData | null>(null);


    useEffect(() => {
        loadFiles();
    }, []);


    async function loadFiles() {

        try {

            const res = await api.get(
                "/api/v1/gis/import/disease-control/files"
            );


            const mapped: Record<string, string> = {};


            if (Array.isArray(res.data)) {

                res.data.forEach((item: any) => {

                    if (item?.code && item?.filename) {

                        mapped[item.code] =
                            item.filename;

                    }

                });

            }


            setLastFiles(mapped);


        } catch (error) {

            console.error(
                "Load files error:",
                error
            );

        }

    }



    function selectFile(
        code: string,
        event: React.ChangeEvent<HTMLInputElement>
    ) {

        const selectedFile =
            event.target.files?.[0];


        setFiles(previous => ({

            ...previous,

            [code]: selectedFile

        }));


        setPopup(null);

    }



    function normalizeImportResponse(
        response: any
    ): ImportResponse {


        const data =
            response?.data ??
            response ??
            {};


        const rawResult =
            data?.result &&
                typeof data.result === "object"
                ? data.result
                : data;



        return {

            status: data?.status,

            message: data?.message,

            form: data?.form,

            file: data?.file,


            result: {

                inserted: Number(
                    rawResult?.inserted ?? 0
                ),


                skipped: Number(
                    rawResult?.skipped ?? 0
                ),


                failed: Number(
                    rawResult?.failed ?? 0
                ),


                missing_units:

                    Array.isArray(
                        rawResult?.missing_units
                    )
                        ?
                        rawResult.missing_units
                        :
                        [],


                warnings:

                    Array.isArray(
                        rawResult?.warnings
                    )
                        ?
                        rawResult.warnings
                        :
                        []

            }

        };

    }



    function getMissingUnitCodes(
        missingUnits: any[]
    ): string[] {


        const codes: string[] = [];


        for (const item of missingUnits || []) {


            let code = "";


            if (typeof item === "string") {

                code = item;

            }
            else if (item?.unit_code) {

                code = String(item.unit_code);

            }
            else if (item?.code) {

                code = String(item.code);

            }
            else if (item?.unitCode) {

                code = String(item.unitCode);

            }


            code = code.trim();


            if (code && !codes.includes(code)) {

                codes.push(code);

            }

        }


        return codes;

    }
    function showImportPopup(
        responseData: ImportResponse
    ) {

        const result =
            responseData.result ?? {};


        const inserted =
            Number(result.inserted ?? 0);

        const skipped =
            Number(result.skipped ?? 0);

        const failed =
            Number(result.failed ?? 0);


        const missingUnits =
            Array.isArray(result.missing_units)
                ? result.missing_units
                : [];


        const warnings =
            Array.isArray(result.warnings)
                ? result.warnings
                : [];


        const missingCodes =
            getMissingUnitCodes(
                missingUnits
            );


        const normalizedResult: ImportResult =
        {
            ...result,

            inserted,

            skipped,

            failed,

            missing_units:
                missingUnits,

            warnings

        };



        if (missingCodes.length > 0) {

            setPopup({

                type: "warning",

                title:
                    "برخی واحدها در سامانه پیدا نشدند",

                message:
                    "برخی رکوردهای فایل به دلیل نبود کد واحد در سامانه ثبت نشدند.",

                file:
                    responseData.file,

                result:
                    normalizedResult

            });


            return;

        }



        if (failed > 0) {

            setPopup({

                type: "warning",

                title:
                    "ثبت برخی رکوردها ناموفق بود",

                message:
                    responseData.message ??
                    "برخی اطلاعات فایل وارد نشدند. جزئیات خطا را بررسی کنید.",

                file:
                    responseData.file,

                result:
                    normalizedResult

            });


            return;

        }



        if (
            inserted === 0 &&
            skipped > 0
        ) {

            setPopup({

                type: "warning",

                title:
                    "اطلاعات قبلاً ثبت شده است",

                message:
                    "تمام رکوردهای فایل تکراری تشخیص داده شدند و اطلاعات جدیدی ثبت نشد.",

                file:
                    responseData.file,

                result:
                    normalizedResult

            });


            return;

        }



        setPopup({

            type: "success",

            title:
                "عملیات وارد کردن فایل موفق بود",

            message:
                responseData.message ??
                "اطلاعات با موفقیت ثبت شد.",

            file:
                responseData.file,

            result:
                normalizedResult

        });


    }





    async function upload(
        code: string
    ) {

        const file =
            files[code];


        if (!file) {

            setPopup({

                type: "warning",

                title:
                    "فایل انتخاب نشده",

                message:
                    "لطفاً ابتدا فایل Excel مورد نظر را انتخاب کنید."

            });


            return;

        }



        const formData =
            new FormData();



        formData.append(
            "file",
            file
        );


        formData.append(
            "code",
            code
        );



        try {


            await api.post(

                "/api/v1/gis/import/disease-control/upload",

                formData,

                {

                    headers: {

                        "Content-Type":
                            "multipart/form-data"

                    }

                }

            );



            let importResponse: any;



            try {


                const importUrl =
                    "/api/v1/gis/import/disease-control/" +
                    String(code).trim() +
                    "/import";



                console.log(
                    "IMPORT URL:",
                    importUrl
                );



                importResponse =
                    await api.post(
                        importUrl
                    );



            }
            catch (error: any) {


                console.error(
                    "Import endpoint error:",
                    error
                );



                const detail =

                    error?.response?.data?.detail ??

                    error?.response?.data?.message ??

                    error?.message ??

                    "خطا در اجرای عملیات Import";



                setPopup({

                    type: "error",

                    title:
                        "خطا در مرحله Import",

                    message:
                        String(detail),

                    file:
                        file.name

                });



                return;

            }




            const responseData =

                normalizeImportResponse(
                    importResponse
                );



            console.log(
                "GIS IMPORT RESPONSE:",
                responseData
            );



            showImportPopup(
                responseData
            );



            await loadFiles();



        }
        catch (error: any) {


            console.error(
                "GIS upload/import error:",
                error
            );



            const detail =

                error?.response?.data?.detail ??

                error?.response?.data?.message ??

                error?.message ??

                "خطا در ارسال فایل";



            setPopup({

                type: "error",

                title:
                    "خطا در ارسال فایل",

                message:
                    String(detail),

                file:
                    file.name

            });


        }

    }
    function getSelectedFile(code: string) {

        if (!files[code]) {

            return "فایلی انتخاب نشده";

        }


        return files[code]?.name ?? "";

    }




    const missingCodes =

        getMissingUnitCodes(

            popup?.result?.missing_units ?? []

        );




    return (

        <div
            dir="rtl"
            style={{
                padding: "30px"
            }}
        >


            <h2>
                بارگذاری اطلاعات GIS
            </h2>


            <h3>
                مدیریت اطلاعات کنترل بیماری
            </h3>




            <table
                border={1}
                width="100%"
                cellPadding={8}
                style={{
                    borderCollapse: "collapse"
                }}
            >

                <thead>

                    <tr>

                        <th>
                            فرم
                        </th>


                        <th>
                            فایل
                        </th>


                        <th>
                            عملیات
                        </th>


                        <th>
                            آخرین فایل
                        </th>

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

                                        onChange={(event) =>
                                            selectFile(
                                                item.code,
                                                event
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

                                        onClick={() =>
                                            upload(
                                                item.code
                                            )
                                        }

                                    >

                                        بارگذاری و Import

                                    </button>


                                </td>



                                <td>

                                    {
                                        lastFiles[item.code] ?? ""
                                    }

                                </td>



                            </tr>

                        ))
                    }


                </tbody>


            </table>





            {
                popup && (

                    <div

                        style={{

                            position: "fixed",

                            inset: 0,

                            backgroundColor:
                                "rgba(0,0,0,0.45)",

                            display: "flex",

                            alignItems: "center",

                            justifyContent: "center",

                            zIndex: 9999,

                            padding: "20px"

                        }}

                    >


                        <div

                            style={{

                                background: "#fff",

                                width:
                                    "min(700px,100%)",

                                maxHeight: "85vh",

                                overflowY: "auto",

                                borderRadius: "12px",

                                padding: "25px"

                            }}

                        >



                            <div

                                style={{

                                    display: "flex",

                                    justifyContent:
                                        "space-between"

                                }}

                            >

                                <h2>

                                    {popup.title}

                                </h2>


                                <button

                                    onClick={() =>
                                        setPopup(null)
                                    }

                                >

                                    ×

                                </button>


                            </div>




                            <p>

                                {popup.message}

                            </p>





                            {
                                popup.file && (

                                    <p>

                                        <strong>
                                            فایل:
                                        </strong>

                                        {" "}

                                        {popup.file}

                                    </p>

                                )
                            }





                            {
                                popup.result && (

                                    <div

                                        style={{

                                            display: "grid",

                                            gridTemplateColumns:
                                                "repeat(3,1fr)",

                                            gap: "10px"

                                        }}

                                    >



                                        <div>

                                            <strong>
                                                ثبت شده
                                            </strong>

                                            <h2>

                                                {
                                                    popup.result.inserted ?? 0
                                                }

                                            </h2>

                                        </div>




                                        <div>

                                            <strong>
                                                تکراری
                                            </strong>

                                            <h2>

                                                {
                                                    popup.result.skipped ?? 0
                                                }

                                            </h2>

                                        </div>




                                        <div>

                                            <strong>
                                                خطا
                                            </strong>

                                            <h2>

                                                {
                                                    popup.result.failed ?? 0
                                                }

                                            </h2>

                                        </div>



                                    </div>

                                )
                            }





                            {
                                missingCodes.length > 0 && (

                                    <div>

                                        <h3>
                                            کد واحدهای پیدا نشده
                                        </h3>


                                        <ul>

                                            {
                                                missingCodes.map(code => (

                                                    <li key={code}>

                                                        {code}

                                                    </li>

                                                ))
                                            }

                                        </ul>


                                    </div>

                                )
                            }





                            {
                                popup.result?.warnings &&
                                popup.result.warnings.length > 0 && (

                                    <div>

                                        <h3>
                                            هشدارها
                                        </h3>


                                        <ul>

                                            {
                                                popup.result.warnings.map(
                                                    (warning, index) => (

                                                        <li key={index}>

                                                            {warning}

                                                        </li>

                                                    ))
                                            }

                                        </ul>


                                    </div>

                                )
                            }




                            <button

                                onClick={() =>
                                    setPopup(null)
                                }

                            >

                                بستن

                            </button>



                        </div>


                    </div>

                )
            }




        </div>

    );


}
