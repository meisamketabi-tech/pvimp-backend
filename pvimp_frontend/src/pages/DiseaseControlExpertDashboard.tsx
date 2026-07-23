import React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getCountyName } from "../utils/counties";
import "./Dashboard.css";

import {
    ResponsiveContainer,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid
} from "recharts";


export default function DiseaseControlExpertDashboard(){

    const navigate = useNavigate();

    const { id } = useParams();

    const county = getCountyName(id);



    const diseaseData = [
        {name:"تب برفکی",value:85},
        {name:"شاربن",value:45},
        {name:"بروسلوز",value:30},
        {name:"لمپی اسکین",value:70}
    ];



    return (

    <div className="dashboard-container" dir="rtl">


        <div className="expert-header">

            <h1>
                داشبورد کارشناس بهداشت و مدیریت بیماری‌های دامی
            </h1>

            <p>
                شهرستان {county} | آخرین بروزرسانی: امروز
            </p>

        </div>




        <div className="cards">


            <div className="card county-card">

                <h3>
                    شهرستان
                </h3>

                <strong>
                    {county}
                </strong>

            </div>




            <div className="card">

                <h3>
                    برنامه مراقبت ماه جاری
                </h3>

                <strong>
                    120
                </strong>

                <p>
                    هدف
                </p>

            </div>




            <div className="card">

                <h3>
                    مراقبت انجام شده
                </h3>

                <strong>
                    86
                </strong>

                <p>
                    ثبت شده
                </p>

            </div>




            <div className="card">

                <h3>
                    درصد تحقق
                </h3>

                <strong>
                    72%
                </strong>

                <p>
                    وضعیت برنامه
                </p>

            </div>




            <div className="card">

                <h3>
                    واحدهای پرخطر
                </h3>

                <strong>
                    18
                </strong>

                <p>
                    نیازمند اقدام
                </p>

            </div>


        </div>






        <div className="dashboard-grid">





            <div className="panel">

                <h2>
                    عملکرد مراقبت ماهانه
                </h2>


                <div className="performance-box">


                    <div className="progress-circle">
                        72%
                    </div>



                    <div>

                        <h3>
                            وضعیت عملکرد
                        </h3>


                        <p>
                            34 مورد مراقبت تا تکمیل برنامه باقی مانده است.
                        </p>


                        <p className="warning">
                            نیاز به افزایش بازدید واحدهای عقب مانده
                        </p>


                    </div>


                </div>


            </div>






            <div className="panel action-panel">

                <h2>
                    اقدامات مورد نیاز امروز
                </h2>


                <ul className="action-list">


                    <li>
                        بازدید 5 واحد پرخطر شهرستان {county}
                    </li>


                    <li>
                        پیگیری کانون سابقه‌دار شاربن
                    </li>


                    <li>
                        تکمیل ثبت مراقبت 12 واحد
                    </li>


                </ul>


            </div>








            <div className="panel chart-panel">


                <h2>
                    وضعیت بیماری‌های تحت مراقبت
                </h2>



                <ResponsiveContainer width="100%" height={250}>


                    <BarChart data={diseaseData}>


                        <CartesianGrid strokeDasharray="3 3"/>


                        <XAxis dataKey="name"/>


                        <YAxis/>


                        <Tooltip/>


                        <Bar
                            dataKey="value"
                            fill="#008577"
                        />


                    </BarChart>


                </ResponsiveContainer>



            </div>








            <div className="panel ai-panel">


                <h2>
                    تحلیل هوشمند AI
                </h2>



                <p>
                    کاهش پوشش مراقبت در برخی مناطق شهرستان {county} شناسایی شد.
                </p>


                <p>
                    احتمال افزایش ریسک بیماری در واحدهای بدون بازدید وجود دارد.
                </p>


                <p>
                    وضعیت بیماری‌های گروه یک کنترل شده است.
                </p>


            </div>









            <div className="panel upload-panel">


                <h2>
                    ورود اطلاعات مراقبت
                </h2>



                <p>
                    ثبت فایل Excel دریافت شده از سامانه GIS
                </p>




                <button

                    className="upload-btn"

                    onClick={()=>navigate(
                        `/county/${id}/expert/disease/import`
                    )}

                >

                    ورود اطلاعات مراقبت

                </button>



            </div>





        </div>




    </div>

    )

}