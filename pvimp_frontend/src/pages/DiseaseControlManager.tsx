import React from "react";
import "./Dashboard.css";


const kpis=[
{
title:"واحدهای اپیدمیولوژیک تحت پوشش",
value:"14968",
desc:"بر اساس خروجی GIS"
},
{
title:"مراقبت فعال ماه جاری",
value:"86",
desc:"از برنامه مصوب"
},
{
title:"درصد تحقق مراقبت",
value:"71%",
desc:"وضعیت برنامه مراقبت"
},
{
title:"موارد مثبت بیماری",
value:"0",
desc:"در نمونه‌های ثبت شده"
},
{
title:"نمونه‌های بررسی شده",
value:"960",
desc:"دام بررسی شده"
}
];


const monitoring=[

{
unit:"گاو گل",
city:"ماهنشان",
type:"روستا",
disease:"مراقبت فعال مبتنی بر خطر تب برفکی",
animal:"گوسفند",
date:"1405/04/22",
result:"منفی"
},

{
unit:"گاو گل",
city:"ماهنشان",
type:"روستا",
disease:"مراقبت فعال مبتنی بر خطر تب برفکی",
animal:"بز",
date:"1405/04/22",
result:"منفی"
},

{
unit:"حلب علیا جدید",
city:"ماهنشان",
type:"روستا",
disease:"مراقبت شاربن",
animal:"گوسفند",
date:"1405/04/07",
result:"منفی"
}

];


const alerts=[

"⚠️ پوشش مراقبت تب برفکی در برخی شهرستان‌ها کمتر از برنامه هدف است.",

"⚠️ نیاز به پایش بیشتر واحدهای پرخطر وجود دارد.",

"✅ تاکنون مورد مثبت بیماری گروه یک در مراقبت‌های ثبت شده مشاهده نشده است."

];


const cities=[

["زنجان","82%","مطلوب"],

["ابهر","76%","نیازمند توجه"],

["خدابنده","91%","مطلوب"],

["ماهنشان","68%","نیازمند پیگیری"],

["طارم","85%","مطلوب"]

];


export default function DiseaseControlManager(){


return(

<div className="dashboard-page" dir="rtl">


<header className="dashboard-header">

<h1>
داشبورد اداره بهداشت و مدیریت بیماری‌های دامی
</h1>

<p>
نمایش وضعیت مراقبت بیماری‌های دامی بر اساس داده‌های GIS
</p>

</header>



<div className="dashboard-grid">

{
kpis.map((k,i)=>(

<div className="dashboard-box" key={i}>

<h3>{k.title}</h3>

<strong>{k.value}</strong>

<p>{k.desc}</p>

</div>

))
}

</div>




<section className="dashboard-box">

<h2>
آخرین مراقبت‌های ثبت شده
</h2>


<table>

<thead>

<tr>

<th>واحد</th>
<th>شهرستان</th>
<th>نوع واحد</th>
<th>نوع مراقبت</th>
<th>دام</th>
<th>تاریخ</th>
<th>نتیجه</th>

</tr>

</thead>


<tbody>

{
monitoring.map((m,i)=>(

<tr key={i}>

<td>{m.unit}</td>
<td>{m.city}</td>
<td>{m.type}</td>
<td>{m.disease}</td>
<td>{m.animal}</td>
<td>{m.date}</td>
<td>{m.result}</td>

</tr>

))
}

</tbody>


</table>


</section>




<section className="dashboard-box">

<h2>
وضعیت شهرستان‌ها
</h2>


<table>

<thead>

<tr>

<th>شهرستان</th>
<th>تحقق برنامه</th>
<th>وضعیت</th>

</tr>

</thead>


<tbody>

{
cities.map((c,i)=>(

<tr key={i}>

<td>{c[0]}</td>
<td>{c[1]}</td>
<td>{c[2]}</td>

</tr>

))
}

</tbody>


</table>


</section>





<section className="dashboard-box">


<h2>
هشدارهای مدیریتی AI
</h2>


{
alerts.map((a,i)=>(

<p key={i}>
{a}
</p>

))
}


</section>



</div>

)

}
