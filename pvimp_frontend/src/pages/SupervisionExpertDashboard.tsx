import React from "react";
import {useNavigate,useParams} from "react-router-dom";
import {getCountyName} from "../utils/counties";
import "./Dashboard.css";


export default function SupervisionExpertDashboard(){


const navigate=useNavigate();

const {id}=useParams();

const county=getCountyName(id);



return(

<div className="dashboard-container" dir="rtl">


<div className="expert-header">

<h1>
داشبورد کارشناس اداره نظارت بر بهداشت عمومی و مواد غذایی
</h1>


<p>
اداره دامپزشکی شهرستان {county}
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
مراکز تحت پوشش
</h3>

<strong>
1250
</strong>

<p>
مرکز فعال
</p>

</div>



<div className="card">

<h3>
بازدید برنامه ماه جاری
</h3>

<strong>
240
</strong>

<p>
هدف
</p>

</div>



<div className="card">

<h3>
بازدید انجام شده
</h3>

<strong>
186
</strong>

<p>
ثبت شده
</p>

</div>



<div className="card">

<h3>
تخلفات باز
</h3>

<strong>
34
</strong>

<p>
نیازمند پیگیری
</p>

</div>


</div>





<div className="dashboard-grid">



<div className="panel">


<h2>
عملکرد نظارت ماهانه
</h2>


<div className="performance-box">


<div className="progress-circle">

77%

</div>


<div>

<h3>
وضعیت اجرای برنامه
</h3>

<p>
54 بازدید تا تکمیل برنامه باقی مانده است.
</p>

<p className="warning">
تمرکز بر مراکز دارای سابقه تخلف
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
🔴 پیگیری 8 تخلف بحرانی
</li>


<li>
🟠 بازدید مجدد 12 مرکز دارای عدم انطباق
</li>


<li>
🟡 تکمیل گزارش 15 بازدید انجام شده
</li>


<li>
🔴 بررسی 4 نمونه مشکوک آزمایشگاهی
</li>


</ul>


</div>






<div className="panel">


<h2>
وضعیت تخلفات بهداشتی
</h2>


<table>


<thead>

<tr>

<th>
نوع تخلف
</th>

<th>
تعداد
</th>

<th>
وضعیت
</th>

</tr>

</thead>



<tbody>


<tr>

<td>
عدم رعایت زنجیره سرد
</td>

<td>
12
</td>

<td className="warning">
نیازمند اصلاح
</td>

</tr>


<tr>

<td>
شرایط بهداشتی نامناسب
</td>

<td>
15
</td>

<td className="warning">
پیگیری
</td>

</tr>



<tr>

<td>
تخلف بحرانی
</td>

<td>
7
</td>

<td className="warning">
اقدام فوری
</td>

</tr>



</tbody>


</table>


</div>






<div className="panel gis-alert-panel">


<h2>
هشدارهای GIS
</h2>


<div className="risk-item">

<strong>
فروشگاه مواد غذایی منطقه مرکزی
</strong>

<span>
45 روز بدون بازدید
</span>

</div>



<div className="risk-item">

<strong>
مرکز عرضه فرآورده خام دامی
</strong>

<span>
سابقه تخلف تکراری
</span>

</div>



<div className="risk-item">

<strong>
کشتارگاه شهرستان
</strong>

<span>
نیازمند بررسی فوری
</span>

</div>



</div>







<div className="panel action-panel upload-panel">


<h2>
ورود اطلاعات نظارت
</h2>


<p>
بارگذاری فرم‌های بازدید، تخلفات و نتایج نمونه‌برداری
</p>


<button

className="upload-btn"

onClick={()=>navigate("/supervision-import")}

>

📂 ورود اطلاعات نظارت

</button>


</div>







<div className="panel">


<h2>
آخرین بازدیدهای ثبت شده
</h2>


<table>


<thead>

<tr>

<th>
مرکز
</th>


<th>
نوع مرکز
</th>


<th>
تاریخ
</th>


<th>
نتیجه
</th>


</tr>

</thead>



<tbody>


<tr>

<td>
فروشگاه الف
</td>


<td>
عرضه فرآورده خام دامی
</td>


<td>
1405/04/22
</td>


<td className="good">
مطلوب
</td>


</tr>



</tbody>


</table>


</div>







<div className="panel ai-panel">


<h2>
تحلیل هوشمند AI
</h2>


<p>
⚠️ افزایش تخلفات بهداشتی در منطقه شمالی شناسایی شد.
</p>


<p>
⚠️ 6 مرکز نیازمند بازدید فوری هستند.
</p>


<p>
✅ روند کاهش تخلفات کشتارگاه‌ها مشاهده شده است.
</p>


</div>




</div>



</div>


)

}


