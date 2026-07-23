import React from "react";
import {useParams} from "react-router-dom";
import "./Dashboard.css";


const countyNames=[

"ابهر",
"ایجرود",
"طارم",
"زنجان",
"خرمدره",
"خدابنده",
"سلطانیه",
"ماهنشان"

];


const experts=[

["کارشناس بهداشت و مدیریت بیماری‌های دامی","42","مطلوب"],
["کارشناس قرنطینه و امنیت زیستی","31","مطلوب"],
["کارشناس نظارت بهداشت عمومی و مواد غذایی","28","نیازمند پیگیری"],
["کارشناس طیور و آبزیان","24","مطلوب"],
["کارشناس تشخیص و درمان","18","مطلوب"],
["کارشناس آزمایشگاه","15","مطلوب"]

];


export default function CountyDashboard(){


const {id}=useParams();


const county =
countyNames[Number(id)||0] || "نامشخص";



return(

<div className="dashboard-page" dir="rtl">


<div className="dashboard-header">

<h1>
داشبورد رئیس اداره دامپزشکی شهرستان {county}
</h1>

<p>
مدیریت عملکرد، پایش فعالیت‌ها و وضعیت بهداشتی شهرستان
</p>

</div>



<div className="dashboard-grid">



<div className="dashboard-box">

<h3>
واحدهای تحت پوشش
</h3>

<strong>
1250
</strong>

<p>
واحد اپیدمیولوژیک ثبت شده
</p>

</div>



<div className="dashboard-box">

<h3>
مراقبت فعال ماه جاری
</h3>

<strong>
86
</strong>

<p>
مورد انجام شده
</p>

</div>



<div className="dashboard-box">

<h3>
درصد تحقق برنامه
</h3>

<strong>
78%
</strong>

<p>
وضعیت برنامه شهرستان
</p>

</div>



<div className="dashboard-box">

<h3>
موارد مثبت بیماری
</h3>

<strong>
0
</strong>

<p>
در مراقبت‌های ثبت شده
</p>

</div>



</div>




<section className="dashboard-box">


<h2>
عملکرد کارشناسان شهرستان
</h2>


<table>


<thead>

<tr>

<th>
واحد تخصصی
</th>

<th>
بازدید انجام شده
</th>

<th>
وضعیت
</th>

</tr>

</thead>


<tbody>


{

experts.map((e,i)=>(

<tr key={i}>

<td>{e[0]}</td>

<td>{e[1]}</td>

<td>{e[2]}</td>

</tr>

))

}


</tbody>


</table>


</section>





<section className="dashboard-box">


<h2>
ساختار مدیریتی اداره
</h2>


<p>
+
رئیس اداره دامپزشکی شهرستان {county}
</p>


<p>
+
کارشناسان اداره
</p>


<ul>

<li>کارشناس بهداشت و مدیریت بیماری‌های دامی</li>

<li>کارشناس قرنطینه و امنیت زیستی</li>

<li>کارشناس نظارت بهداشت عمومی و مواد غذایی</li>

<li>کارشناس طیور و آبزیان</li>

<li>کارشناس تشخیص و درمان</li>

<li>کارشناس آزمایشگاه</li>

</ul>


</section>




<section className="dashboard-box">


<h2>
هشدارهای مدیریتی AI
</h2>


<p>
⚠️ نیاز به افزایش پوشش مراقبت در واحدهای پرخطر
</p>


<p>
⚠️ پایش عملکرد کارشناسان شهرستان به صورت مستمر انجام شود
</p>


<p>
✅ تاکنون مورد مثبت بیماری گروه یک ثبت نشده است
</p>


</section>



</div>

)

}
