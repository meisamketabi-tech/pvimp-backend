import React,{useEffect,useState} from "react";
import {useParams} from "react-router-dom";

import {
ResponsiveContainer,
BarChart,
Bar,
XAxis,
YAxis,
Tooltip,
Legend,
PieChart,
Pie,
Cell
} from "recharts";

import "./Dashboard.css";


const API="http://localhost:8000";


function normalize(value:any){

return String(value || "")
.replace(/[\u200b-\u200f\u202a-\u202e]/g,"")
.replace(/\s+/g,"")
.replace(/ي/g,"ی")
.replace(/ك/g,"ک")
.trim();

}



export default function CountyDashboard(){


const {id}=useParams();

const county=normalize(id);



const [unit,setUnit]=useState<any>({
total_units:0,
active_units:0
});


const [animal,setAnimal]=useState<any>({
sheep:0,
cattle:0,
goat:0,
horse:0,
dog:0
});


const [diseases,setDiseases]=useState<any[]>([]);




useEffect(()=>{


Promise.all([

fetch(`${API}/gis-county-analysis/units`).then(r=>r.json()),

fetch(`${API}/gis-county-analysis/animals`).then(r=>r.json()),

fetch(`${API}/gis-county-analysis/diseases`).then(r=>r.json())

])


.then(([units,animals,disease])=>{


const u=units.find(
(x:any)=>
normalize(x.county).includes(county)
);


const a=animals.find(
(x:any)=>
normalize(x.county).includes(county)
);


const d=disease.filter(
(x:any)=>
normalize(x.county).includes(county)
);



setUnit(u || {
total_units:0,
active_units:0
});


setAnimal(a || {
sheep:0,
cattle:0,
goat:0,
horse:0,
dog:0
});


setDiseases(d);



});


},[county]);





const totalAnimals =

Number(animal.sheep||0)+
Number(animal.cattle||0)+
Number(animal.goat||0)+
Number(animal.horse||0)+
Number(animal.dog||0);




const activity=

unit.total_units
?
Math.round(
(unit.active_units/unit.total_units)*100
)
:
0;




const unitChart=[

{
name:"واحدها",
کل:unit.total_units,
فعال:unit.active_units
}

];




const animalChart=[

{
name:"گوسفند",
value:Number(animal.sheep||0)
},

{
name:"گاو",
value:Number(animal.cattle||0)
},

{
name:"بز",
value:Number(animal.goat||0)
},

{
name:"اسب",
value:Number(animal.horse||0)
},

{
name:"سگ",
value:Number(animal.dog||0)
}

];



const COLORS=[

"#006064",
"#008577",
"#43a047",
"#ff9800",
"#8e24aa"

];





return(

<div className="dashboard-page">



<div className="dashboard-header">

<h1>
داشبورد مدیریتی شهرستان {id}
</h1>

<p>
تحلیل هوشمند وضعیت واحدها، جمعیت دامی و بیماری‌ها
</p>

</div>






<div className="dashboard-grid">



<div className="dashboard-box kpi-card">

<h3>
کل واحدها
</h3>

<strong>
{unit.total_units}
</strong>

<span>
واحد ثبت شده
</span>

</div>




<div className="dashboard-box kpi-card">

<h3>
واحد فعال
</h3>

<strong>
{unit.active_units}
</strong>

<span>
واحد فعال شهرستان
</span>

</div>





<div className="dashboard-box kpi-card">

<h3>
نرخ فعالیت
</h3>

<strong>
{activity}%
</strong>

<span>
شاخص فعالیت
</span>

</div>





<div className="dashboard-box kpi-card">

<h3>
جمعیت دامی
</h3>

<strong>
{totalAnimals.toLocaleString()}
</strong>

<span>
رأس دام
</span>

</div>



</div>








<section className="dashboard-box">


<h2>
وضعیت واحدهای شهرستان
</h2>



<ResponsiveContainer width="100%" height={350}>


<BarChart data={unitChart}>


<XAxis dataKey="name"/>

<YAxis/>

<Tooltip/>

<Legend/>


<Bar
dataKey="کل"
radius={[10,10,0,0]}
fill="#006064"
/>


<Bar
dataKey="فعال"
radius={[10,10,0,0]}
fill="#43a047"
/>


</BarChart>


</ResponsiveContainer>


</section>










<section className="dashboard-box">


<h2>
ترکیب جمعیت دامی
</h2>


<ResponsiveContainer width="100%" height={380}>


<PieChart>


<Pie

data={animalChart}

dataKey="value"

nameKey="name"

cx="50%"

cy="50%"

innerRadius={80}

outerRadius={130}

label

>


{

animalChart.map(
(_,index)=>(

<Cell

key={index}

fill={COLORS[index]}

/>

)

)

}



</Pie>


<Tooltip/>

<Legend/>


</PieChart>


</ResponsiveContainer>


</section>









<section className="dashboard-box">


<h2>
کانون‌های بیماری شهرستان
</h2>



{
diseases.length===0

?

<div className="success-box">

بدون گزارش بیماری

</div>

:

<div className="danger-box">

تعداد کانون بیماری:
<b>
{diseases.length}
</b>


<table>

<thead>

<tr>

<th>
بیماری
</th>

<th>
کانون
</th>

<th>
تلفات
</th>

</tr>

</thead>


<tbody>


{
diseases.map(
(d,i)=>(

<tr key={i}>

<td>
{d.disease}
</td>

<td>
{d.outbreaks}
</td>

<td>
{d.dead}
</td>


</tr>

)

)
}


</tbody>


</table>

</div>

}



</section>









<section className="dashboard-box">


<h2>
تحلیل مدیریتی
</h2>



<div className="analysis-card">

وضعیت فعالیت واحدها

<strong>
{activity}%
</strong>

</div>



<div className="analysis-card">

وضعیت بیماری

<strong>

{
diseases.length
?
"دارای کانون بیماری"
:
"پاک"

}

</strong>

</div>



</section>







</div>

)


}