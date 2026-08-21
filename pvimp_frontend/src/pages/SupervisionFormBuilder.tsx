import React, { useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import { getCountyName } from "../utils/counties";
import "./SupervisionForm.css";

export default function SupervisionForm() {

    const { id } = useParams();

    const county = getCountyName(id);

    const today = new Intl.DateTimeFormat(
        "fa-IR-u-ca-persian",
        {
            year: "numeric",
            month: "2-digit",
            day: "2-digit"
        }
    ).format(new Date());


    const activityGroups = [

        "بازدید و نظارت",

        "کشتارگاه و مراکز وابسته",

        "مراکز عرضه فرآورده های خام دامی",

        "واحدهای تولیدی و پرورش دام و طیور",

        "قرنطینه دامی",

        "نمونه برداری",

        "آزمایشگاه",

        "کنترل بیماری های واگیر دام",

        "واحدهای خدمات دامپزشکی"

    ];


    const activityTypes: any = {


        "بازدید و نظارت": [

            "بازدید دوره ای",

            "بازدید موردی"

        ],


        "کشتارگاه و مراکز وابسته": [

            "کشتارگاه",

            "مرکز بسته بندی",

            "مرکز عرضه گوشت"

        ],


        "مراکز عرضه فرآورده های خام دامی": [

            "قصابی",

            "مرغ فروشی",

            "فروشگاه فرآورده های دامی",

            "سردخانه"

        ],


        "واحدهای تولیدی و پرورش دام و طیور": [

            "دامداری",

            "مرغداری",

            "پرورش آبزیان"

        ],


        "قرنطینه دامی": [

            "بازرسی قرنطینه"

        ],


        "نمونه برداری": [

            "نمونه برداری رسمی"

        ],


        "آزمایشگاه": [

            "ارسال نمونه"

        ],


        "کنترل بیماری های واگیر دام": [

            "مراقبت بیماری",

            "واکسیناسیون"

        ],


        "واحدهای خدمات دامپزشکی": [

            "داروخانه دامپزشکی",

            "درمانگاه دامپزشکی",

            "مرکز مایه کوبی"

        ]


    };



    const organizationsList = [

        "اداره کل دامپزشکی",

        "شبکه دامپزشکی شهرستان",

        "مرکز بهداشت",

        "آزمایشگاه",

        "دانشگاه",

        "بخش خصوصی",

        "شهرداری",

        "فرمانداری",

        "سایر"

    ];



    const generalChecklist = [

        "رعایت الزامات بهداشتی",

        "بررسی مجوز و پروانه فعالیت",

        "کنترل شرایط نگهداری",

        "بررسی تجهیزات و امکانات",

        "کنترل سوابق فعالیت",

        "بررسی شرایط قرنطینه",

        "کنترل مستندات",

        "بررسی وضعیت کارکنان",

        "ثبت گزارش بازدید",

        "بررسی نواقص مشاهده شده",

        "ارائه توصیه های اصلاحی",

        "ثبت اقدامات انجام شده",

        "بررسی وضعیت ایمنی",

        "کنترل شرایط محیطی",

        "بررسی تجهیزات حفاظتی",

        "کنترل فرآیند کاری",

        "بررسی برنامه های آموزشی",

        "ثبت تخلفات احتمالی",

        "ارزیابی عملکرد",

        "تکمیل فرم نظارت"

    ];



    const specificChecklists: any = {


        "بازدید دوره ای": [

            "کنترل وضعیت عمومی واحد",

            "بررسی تجهیزات موجود",

            "کنترل بهداشت محیط",

            "بررسی شرایط نگهداری دام",

            "بررسی سوابق واکسیناسیون",

            "کنترل بیماری های مشاهده شده",

            "بررسی اقدامات اصلاحی",

            "کنترل کارکنان",

            "بررسی ایمنی محیط",

            "ثبت گزارش نهایی"

        ],



        "بازدید موردی": [

            "بررسی علت بازدید",

            "کنترل وضعیت اضطراری",

            "ثبت موارد مشاهده شده",

            "بررسی اقدامات انجام شده",

            "ارائه گزارش تخصصی",

            "ثبت نتیجه بازدید"

        ],



        "مرغداری": [

            "بررسی تراکم سالن",

            "کنترل تهویه",

            "بررسی برنامه واکسیناسیون",

            "کنترل خوراک و آب",

            "بررسی تلفات",

            "کنترل امنیت زیستی"

        ],



        "دامداری": [

            "کنترل وضعیت دام",

            "بررسی جایگاه دام",

            "کنترل تغذیه",

            "بررسی بیماری ها",

            "کنترل سوابق درمانی"

        ],



        "کشتارگاه": [

            "بررسی خط کشتار",

            "کنترل شرایط بهداشتی",

            "بررسی CIP",

            "کنترل تجهیزات",

            "بررسی کارکنان"

        ]


    };


    const [organizations, setOrganizations] = useState<string[]>([]);

    const [checklist, setChecklist] = useState<string[]>([]);


    const [form, setForm] = useState({

        epiCode: "",

        unitName: "",

        activityGroup: "",

        activityType: "",

        parentType: "",

        parentUnit: "",

        owner: "",

        technicalManager: "",

        visitDate: today,

        visitType: "",

        inspectionType: ""

    });


    const availableActivityTypes = useMemo(() => {

        return activityTypes[form.activityGroup] || [];

    }, [form.activityGroup]);


    const hasTechnicalManager = useMemo(() => {

        return [

            "بازدید دوره ای",

            "بازدید موردی",

            "دامداری",

            "مرغداری",

            "کشتارگاه",

            "واکسیناسیون"

        ].includes(form.activityType);


    }, [form.activityType]);
    const handleChange = (e: any) => {

        const { name, value } = e.target;

        setForm(prev => ({

            ...prev,

            [name]: value,

            ...(name === "activityGroup"
                ?
                {
                    activityType: "",
                    parentType: "",
                    parentUnit: ""
                }
                :
                {})

        }));

    };



    const toggleOrganization = (item: string) => {

        if (organizations.includes(item)) {

            setOrganizations(
                organizations.filter(x => x !== item)
            );

        }
        else {

            setOrganizations([
                ...organizations,
                item
            ]);

        }

    };



    const toggleChecklist = (item: string) => {

        if (checklist.includes(item)) {

            setChecklist(
                checklist.filter(x => x !== item)
            );

        }
        else {

            setChecklist([
                ...checklist,
                item
            ]);

        }

    };



    const submit = (e: any) => {

        e.preventDefault();


        console.log({

            ...form,

            organizations,

            checklist

        });


        alert("فرم با موفقیت ثبت شد");

    };



    return (

        <div
            className="dashboard-container"
            dir="rtl"
        >


            <div className="expert-header">


                <h1>

                    فرم بازدید و نظارت دامپزشکی

                </h1>


                <p>

                    ثبت اطلاعات واحد تحت پوشش شهرستان {county}

                </p>


            </div>



            <form

                className="dashboard-box"

                onSubmit={submit}

            >



                <div className="form-section">


                    <h2>

                        اطلاعات پایه فرم

                    </h2>



                    <div className="form-grid">



                        <div>

                            <label>

                                کد اپیدمیولوژیک

                            </label>


                            <input

                                name="epiCode"

                                value={form.epiCode}

                                onChange={handleChange}

                            />

                        </div>




                        <div>

                            <label>

                                گروه فعالیت

                            </label>


                            <select

                                name="activityGroup"

                                value={form.activityGroup}

                                onChange={handleChange}

                            >


                                <option value="">

                                    انتخاب کنید

                                </option>


                                {

                                    activityGroups.map(x =>

                                        <option

                                            key={x}

                                            value={x}

                                        >

                                            {x}

                                        </option>

                                    )

                                }


                            </select>


                        </div>





                        <div>


                            <label>

                                نوع فعالیت

                            </label>



                            <select

                                name="activityType"

                                value={form.activityType}

                                onChange={handleChange}

                            >


                                <option value="">

                                    انتخاب کنید

                                </option>



                                {

                                    availableActivityTypes.map((x: string) =>

                                        <option

                                            key={x}

                                            value={x}

                                        >

                                            {x}

                                        </option>

                                    )

                                }


                            </select>


                        </div>






                        {

                            form.activityGroup !== "" &&


                            <div>


                                <label>

                                    نام واحد

                                </label>



                                <select

                                    name="unitName"

                                    value={form.unitName}

                                    onChange={handleChange}

                                >


                                    <option>

                                        واحد شهرستان {county}

                                    </option>


                                </select>


                            </div>


                        }






                        <div>


                            <label>

                                مسئول واحد

                            </label>


                            <input

                                name="owner"

                                value={form.owner}

                                onChange={handleChange}

                            />


                        </div>





                        {

                            hasTechnicalManager &&


                            <div>


                                <label>

                                    مسئول فنی

                                </label>


                                <input

                                    name="technicalManager"

                                    value={form.technicalManager}

                                    onChange={handleChange}

                                />


                            </div>


                        }



                    </div>


                </div>
                {


                    form.activityGroup === "کشتارگاه و مراکز وابسته" &&


                    <div className="form-section">


                        <h2>

                            اطلاعات مرکز مادر

                        </h2>




                        <select

                            name="parentType"

                            value={form.parentType}

                            onChange={handleChange}

                        >


                            <option value="">

                                انتخاب کنید

                            </option>


                            <option>

                                کشتارگاه

                            </option>


                            <option>

                                مرکز بسته بندی

                            </option>


                            <option>

                                مرکز عرضه

                            </option>


                        </select>





                        {

                            form.parentType === "مرکز بسته بندی" &&


                            <select

                                name="parentUnit"

                                value={form.parentUnit}

                                onChange={handleChange}

                            >


                                <option>

                                    مرکز بسته بندی شهرستان {county}

                                </option>


                            </select>


                        }







                        {

                            form.parentType === "مرکز عرضه" &&


                            <select

                                name="parentUnit"

                                value={form.parentUnit}

                                onChange={handleChange}

                            >


                                <option>

                                    مرکز عرضه شهرستان {county}

                                </option>


                            </select>


                        }



                    </div>


                }






                <div className="form-section">


                    <h2>

                        اطلاعات بازدید

                    </h2>



                    <div className="form-grid">



                        <div>


                            <label>

                                تاریخ بازدید

                            </label>


                            <input

                                value={form.visitDate}

                                readOnly

                            />


                        </div>







                        <div>


                            <label>

                                نوع بازدید

                            </label>



                            <select

                                name="visitType"

                                value={form.visitType}

                                onChange={handleChange}

                            >


                                <option value="">

                                    انتخاب کنید

                                </option>


                                <option>

                                    دوره ای

                                </option>


                                <option>

                                    موردی

                                </option>


                                <option>

                                    پیگیری

                                </option>


                                <option>

                                    اضطراری

                                </option>


                                <option>

                                    کنترلی

                                </option>


                            </select>


                        </div>







                        <div>


                            <label>

                                نوع بازرسی

                            </label>


                            <select

                                name="inspectionType"

                                value={form.inspectionType}

                                onChange={handleChange}

                            >


                                <option value="">

                                    انتخاب کنید

                                </option>


                                <option>

                                    بازرسی مشترک

                                </option>


                                <option>

                                    بازرسی تخصصی

                                </option>


                            </select>


                        </div>



                    </div>


                </div>






                {

                    form.inspectionType === "بازرسی مشترک" &&


                    <div className="form-section">


                        <h2>

                            سازمان های همکار

                        </h2>




                        <div

                            style={{

                                display: "grid",

                                gridTemplateColumns: "repeat(auto-fill,minmax(220px,1fr))",

                                gap: "10px"

                            }}

                        >


                            {

                                organizationsList.map(item =>

                                    <label

                                        key={item}

                                        style={{

                                            border: "1px solid #ddd",

                                            padding: "12px",

                                            borderRadius: "8px",

                                            background: "#fff"

                                        }}

                                    >


                                        <input

                                            type="checkbox"

                                            checked={organizations.includes(item)}

                                            onChange={() => toggleOrganization(item)}

                                            style={{ marginLeft: "8px" }}

                                        />


                                        {item}


                                    </label>


                                )


                            }



                        </div>


                    </div>


                }
                <div className="form-section">


                    <h2>

                        چک لیست عمومی بازدید

                    </h2>



                    <div

                        style={{

                            display: "grid",

                            gridTemplateColumns: "repeat(auto-fill,minmax(260px,1fr))",

                            gap: "10px"

                        }}

                    >


                        {

                            generalChecklist.map(item =>



                                <label

                                    key={item}

                                    style={{

                                        border: "1px solid #ddd",

                                        padding: "12px",

                                        borderRadius: "8px",

                                        background: "#fff"

                                    }}

                                >


                                    <input

                                        type="checkbox"

                                        checked={checklist.includes(item)}

                                        onChange={() => toggleChecklist(item)}

                                    />


                                    <span style={{ marginRight: "8px" }}>

                                        {item}

                                    </span>



                                </label>



                            )


                        }



                    </div>


                </div>






                <div className="form-section">


                    <h2>

                        چک لیست تخصصی فعالیت

                    </h2>




                    {

                        specificChecklists[form.activityType] ? (


                            <div

                                style={{

                                    display: "grid",

                                    gridTemplateColumns: "repeat(auto-fill,minmax(260px,1fr))",

                                    gap: "10px"

                                }}

                            >


                                {

                                    specificChecklists[form.activityType].map((item: string) => (


                                        <label

                                            key={item}

                                            style={{

                                                border: "1px solid #ddd",

                                                padding: "12px",

                                                borderRadius: "8px",

                                                background: "#fff",

                                                display: "flex",

                                                alignItems: "center",

                                                cursor: "pointer"

                                            }}

                                        >


                                            <input

                                                type="checkbox"

                                                checked={checklist.includes(item)}

                                                onChange={() => toggleChecklist(item)}

                                            />



                                            <span style={{ marginRight: "8px" }}>

                                                {item}

                                            </span>



                                        </label>


                                    ))


                                }



                            </div>


                        )

                            :


                            (


                                <p>

                                    برای این نوع فعالیت چک لیست تخصصی تعریف نشده است.

                                </p>


                            )


                    }



                </div>







                <button

                    className="upload-btn"

                    type="submit"

                >


                    ثبت فرم بازدید


                </button>





            </form>





        </div>


    )

}

