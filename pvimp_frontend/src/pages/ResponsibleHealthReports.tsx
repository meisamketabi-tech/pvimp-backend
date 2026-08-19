
import React,{useEffect,useState} from "react";
import {
getInspections,
getNonConformities,
getSamples,
getColdChain
}
from "../services/responsibleHealthService";

import "./Dashboard.css";


export default function ResponsibleHealthReports(){


const [data,setData]=useState<any>({
inspections:[],
violations:[],
samples:[],
cold:[]
});



useEffect(()=>{


Promise.all([

getInspections(),

getNonConformities(),

getSamples(),

getColdChain()

])
.then(res=>{


setData({

inspections:res[0].data,

violations:res[1].data,

samples:res[2].data,

cold:res[3].data

});


});


},[]);



return (

<div className="dashboard-container" dir="rtl">


<h1>
گزارش‌های مسئول بهداشتی
</h1>


<div className="dashboard-grid">


<div className="dashboard-card">

<h3>
بازدیدها
</h3>

<h2>
{data.inspections.length}
</h2>

</div>



<div className="dashboard-card">

<h3>
عدم انطباق‌ها
</h3>

<h2>
{data.violations.length}
</h2>

</div>



<div className="dashboard-card">

<h3>
نمونه‌برداری‌ها
</h3>

<h2>
{data.samples.length}
</h2>

</div>



<div className="dashboard-card">

<h3>
کنترل زنجیره سرد
</h3>

<h2>
{data.cold.length}
</h2>

</div>


</div>



</div>

)

}

