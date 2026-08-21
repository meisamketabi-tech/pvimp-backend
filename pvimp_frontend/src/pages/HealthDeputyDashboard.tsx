
import React from "react";
import "./Dashboard.css";

const departments=[
["اداره بهداشت و مدیریت بیماری های دامی","92%","مطلوب"],
["اداره نظارت بر بهداشت عمومی و مواد غذایی","87%","مطلوب"],
["اداره طیور و زنبور عسل","89%","مطلوب"],
["قرنطینه و امنیت زیستی","91%","مطلوب"],
["آزمایشگاه","95%","مطلوب"]
];

export default function HealthDeputyDashboard(){

return(
<div className="dashboard-page" dir="rtl">

<h1>داشبورد معاونت سلامت</h1>

<div className="dashboard-box">

<table>

<thead>
<tr>
<th>اداره</th>
<th>شاخص</th>
<th>وضعیت</th>
</tr>
</thead>

<tbody>

{departments.map((d,i)=>
<tr key={i}>
<td>{d[0]}</td>
<td>{d[1]}</td>
<td>{d[2]}</td>
</tr>
)}

</tbody>

</table>

</div>

</div>
)

}

