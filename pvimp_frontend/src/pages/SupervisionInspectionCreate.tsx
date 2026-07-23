import React,{useState} from "react";
import {useNavigate,useParams} from "react-router-dom";

import {
createSupervisionInspection
} from "../services/supervisionService";

import {
emptyInspection,
SupervisionInspection
} from "../types/SupervisionInspection";

import {
getCountyName
} from "../utils/counties";

import {
slaughterhouses
} from "../data/slaughterhouses";

import "./Dashboard.css";


const partnerOptions=[

"صمت",
"تعزیرات حکومتی",
"جهاد کشاورزی",
"راه و شهرسازی",
"شبکه بهداشت",
"محیط زیست",
"نیروی انتظامی",
"سایر"

];



const centerOptions=[

"کشتارگاه",
"فروشگاه عرضه فرآورده‌های خام دامی",
"مراکز طبخ و رستوران",
"هتل",
"کارخانه فرآوری",
"مرکز بسته بندی",
"سردخانه",
"خودرو حمل",
"انبار",
"سایر"

];



const salesUnits=[

"قصابی",
"مرغ فروشی",
"ماهی فروشی",
"فروشگاه بزرگ",
"کارگاه قطعه بندی مستقل",
"کارگاه قطعه بندی وابسته به کشتارگاه",
"کارگاه قطعه بندی وابسته به مراکز عرضه"

];



const cookingUnits=[

"رستوران",
"فست فود",
"مرکز طبخ"

];



export default function SupervisionInspectionCreate(){


const navigate=useNavigate();

const {id}=useParams();


const county=getCountyName(id);



const today=new Intl.DateTimeFormat(
"fa-IR",
{
dateStyle:"short"
}
).format(new Date());



const [form,setForm]=useState<SupervisionInspection>({

...emptyInspection,

inspectionDate:today,

city:county

});





function change(
e:React.ChangeEvent<HTMLInputElement|HTMLSelectElement>
){


const {name,value}=e.target;


setForm({

...form,

[name]:value

});


}




function togglePartner(value:string){


if(form.partners.includes(value)){


setForm({

...form,

partners:
form.partners.filter(x=>x!==value)

});


}

else{


setForm({

...form,

partners:[
...form.partners,
value
]

});


}

}




function selectSlaughterType(value:string){


const list=
slaughterhouses[county]
?.filter(
(x:any)=>x.type===value
)
||[];


setForm({

...form,

slaughterType:[
value
],

unitName:"",

ownerName:"",

phone:""

});


}





function selectSlaughter(name:string){


const item=
slaughterhouses[county]
?.find(
(x:any)=>x.name===name
);



setForm({

...form,

unitName:name,

ownerName:item?.owner || "",

phone:item?.phone || ""

});


}





async function save(){


await createSupervisionInspection(form);


navigate(
`/county/${id}/expert/supervision`
);


}





const slaughterList=
slaughterhouses[county] || [];




return (

<div className="dashboard-container" dir="rtl">


<div className="expert-header">

<h1>
ثبت بازرسی جدید
</h1>

<p>
استان زنجان - شهرستان {county}
</p>

</div>





<div className="inspection-form-card">


<div className="form-grid">





<div className="form-group">

<label>
تاریخ بازرسی
</label>

<input

value={form.inspectionDate}

readOnly

/>

</div>







<div className="form-group">

<label>
نوع بازرسی
</label>


<select

name="inspectionType"

value={form.inspectionType}

onChange={change}

>

<option value="">
انتخاب
</option>


<option>
بازدید مستقل
</option>


<option>
بازدید مشترک
</option>


</select>


</div>







{

form.inspectionType==="بازدید مشترک" &&


<div className="form-group full">

<label>
دستگاه مشترک
</label>


{

partnerOptions.map(x=>(


<label key={x}>


<input

type="checkbox"

checked={
form.partners.includes(x)
}

onChange={()=>togglePartner(x)}

/>


{x}


</label>


))


}


</div>


}







<div className="form-group">


<label>
نوع مرکز
</label>


<select

name="centerType"

value={form.centerType}

onChange={change}

>


<option value="">
انتخاب نوع مرکز
</option>


{

centerOptions.map(x=>(

<option key={x}>
{x}
</option>

))

}


</select>


</div>







{

form.centerType==="کشتارگاه" &&


<div className="form-group">


<label>
نوع کشتارگاه
</label>



<label>

<input

type="radio"

name="slaughterType"

value="کشتارگاه دام"

checked={
form.slaughterType.includes("کشتارگاه دام")
}

onChange={
()=>selectSlaughterType("کشتارگاه دام")
}

/>

کشتارگاه دام

</label>



<label>

<input

type="radio"

name="slaughterType"

value="کشتارگاه طیور"

checked={
form.slaughterType.includes("کشتارگاه طیور")
}

onChange={
()=>selectSlaughterType("کشتارگاه طیور")
}

/>

کشتارگاه طیور

</label>


</div>


}







{

form.centerType==="کشتارگاه" &&
form.slaughterType.length>0 &&


<div className="form-group">


<label>
نام واحد
</label>


<select

value={form.unitName}

onChange={
e=>selectSlaughter(e.target.value)
}

>


<option value="">
انتخاب کشتارگاه
</option>



{

slaughterList

.filter(
(x:any)=>
x.type===form.slaughterType[0]
)

.map(
(x:any)=>(

<option

key={x.name}

value={x.name}

>

{x.name}

</option>

)

)


}


</select>


</div>


}









{

form.centerType==="فروشگاه عرضه فرآورده‌های خام دامی" &&


<div className="form-group">

<label>
نوع واحد عرضه
</label>


<select

name="unitType"

value={form.unitType}

onChange={change}

>


<option value="">
انتخاب
</option>


{

salesUnits.map(x=>(

<option key={x}>
{x}
</option>

))

}


</select>


</div>


}








{

form.centerType==="مراکز طبخ و رستوران" &&


<div className="form-group">


<label>
نوع مرکز طبخ
</label>


<select

name="unitType"

value={form.unitType}

onChange={change}

>


<option value="">
انتخاب
</option>


{

cookingUnits.map(x=>(

<option key={x}>
{x}
</option>

))

}


</select>


</div>


}







<div className="form-group">

<label>
نام واحد
</label>


<input

name="unitName"

value={form.unitName}

onChange={change}

disabled={
form.centerType==="کشتارگاه"
}

/>


</div>







<div className="form-group">

<label>
نام مالک
</label>


<input

name="ownerName"

value={form.ownerName}

onChange={change}

/>


</div>







<div className="form-group">

<label>
تلفن
</label>


<input

name="phone"

value={form.phone}

onChange={change}

/>


</div>







<div className="form-group">

<label>
آدرس
</label>


<input

name="address"

value={form.address}

onChange={change}

/>


</div>







<div className="form-group">

<label>
نام بازرس
</label>


<input

name="inspectorName"

value={form.inspectorName}

onChange={change}

/>


</div>





</div>





<button

className="primary-button"

onClick={save}

>

ثبت بازرسی

</button>



</div>


</div>


);


}