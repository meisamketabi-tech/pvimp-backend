import React, {useState} from "react";
import {useParams} from "react-router-dom";
import {getCountyName} from "../utils/counties";
import "./SupervisionForm.css";
import VoiceRecorder from "../components/VoiceRecorder";

export default function SupervisionForm(){

const {id}=useParams();

const county=getCountyName(id);

const today=new Intl.DateTimeFormat(
"fa-IR-u-ca-persian",
{
year:"numeric",
month:"2-digit",
day:"2-digit"
}
).format(new Date());


const currentTime =
new Date().toLocaleTimeString("fa-IR",
{
hour:"2-digit",
minute:"2-digit"
});


const [form,setForm]=useState({

epidemiologyCode:"",
unitName:"",
activityGroup:"",
activityType:"",
managerName:"",
technicalManager:"",
inspectorName:"",
inspectorRole:"",
visitDate:today,
startTime:currentTime,
visitReason:"",
inspectionType:"",
finalStatus:"",
description:""

});

const [healthItems,setHealthItems]=useState<any[]>([

{
title:"وضعیت ساختمان و محوطه",
status:"",
description:""
},

{
title:"بهداشت محیط و شرایط نگهداری",
status:"",
description:""
},

{
title:"نظافت و شستشو",
status:"",
description:""
},

{
title:"ضدعفونی و کنترل آلودگی",
status:"",
description:""
},

{
title:"کنترل حشرات و جوندگان",
status:"",
description:""
},

{
title:"بهداشت فردی کارکنان",
status:"",
description:""
},

{
title:"کارت بهداشت کارکنان",
status:"",
description:""
},

{
title:"لباس کار و تجهیزات حفاظت فردی",
status:"",
description:""
},

{
title:"آب مصرفی",
status:"",
description:""
},

{
title:"مدیریت فاضلاب",
status:"",
description:""
},

{
title:"مدیریت پسماند",
status:"",
description:""
},

{
title:"زنجیره سرد",
status:"",
description:""
},

{
title:"کنترل دمای نگهداری",
status:"",
description:""
},

{
title:"ثبت سوابق بهداشتی",
status:"",
description:""
}

]);


const [violations,setViolations]=useState<any[]>([]);
const [samples,setSamples]=useState<any[]>([]);
const [checklist,setChecklist]=useState<string[]>([]);


const toggleChecklist=(item:string)=>{

if(checklist.includes(item)){

setChecklist(
checklist.filter(x=>x!==item)
);

}
else{

setChecklist([
...checklist,
item
]);

}

};


const updateField=(e:any)=>{

setForm({

...form,

[e.target.name]:e.target.value

});

};


const updateHealth=(index:number,key:string,value:string)=>{

const copy=[...healthItems];

copy[index][key]=value;

setHealthItems(copy);

};
const activityGroups = [

"کشتارگاه",
"کارگاه قطعه‌بندی و بسته‌بندی",
"مراکز عرضه فرآورده‌های خام دامی",
"کارخانجات لبنیات",
"سردخانه",
"کارخانجات خوراک دام، طیور و آبزیان"

];


const activityTypes:any={

"کشتارگاه":[
"کشتارگاه دام",
"کشتارگاه طیور"
],

"کارگاه قطعه‌بندی و بسته‌بندی":[
"مستقل",
"وابسته به کشتارگاه",
"وابسته به مرکز عرضه"
],

"مراکز عرضه فرآورده‌های خام دامی":[
"مرکز عرضه",
"قصابی",
"فروشگاه زنجیره‌ای"
],

"کارخانجات لبنیات":[
"کارخانه لبنیات"
],

"سردخانه":[
"سردخانه نگهداری"
],

"کارخانجات خوراک دام، طیور و آبزیان":[
"کارخانه خوراک دام",
"کارخانه خوراک طیور",
"کارخانه خوراک آبزیان"
]

};


const countyUnits:any={

"زنجان":{

"کشتارگاه طیور":[

{
name:"کشتارگاه صنعتی طیور زنجان",
code:"Z-P-001",
manager:"مدیرعامل کشتارگاه صنعتی طیور زنجان",
technical:"مسئول فنی کشتارگاه صنعتی طیور زنجان"
},

{
name:"کشتارگاه صنعتی صباغ مرغ",
code:"Z-P-002",
manager:"مدیرعامل صباغ مرغ",
technical:"مسئول فنی صباغ مرغ"
}

]

},


"سلطانیه":{

"کشتارگاه طیور":[

{
name:"کشتارگاه صنعتی آندیا",
code:"S-P-001",
manager:"مدیرعامل آندیا",
technical:"مسئول فنی آندیا"
}

]

},


"خرمدره":{

"کشتارگاه طیور":[

{
name:"کشتارگاه صنعتی طیور زرین طیور",
code:"K-P-001",
manager:"مدیرعامل زرین طیور",
technical:"مسئول فنی زرین طیور"
},

{
name:"کشتارگاه صنعتی طیور پرطلایی هیدج",
code:"K-P-002",
manager:"مدیرعامل پرطلایی هیدج",
technical:"مسئول فنی پرطلایی هیدج"
}

]

}

};


const addViolation=()=>{

setViolations([

...violations,

{
type:"",
severity:"",
deadline:"",
action:""
}

]);

};


const addSample=()=>{

setSamples([

...samples,

{
type:"",
result:"در انتظار نتیجه"
}

]);

};


const specificChecklists:any={

"کشتارگاه دام":[
"مجوز بهره‌برداری معتبر است",
"بازرسی قبل از کشتار انجام می‌شود",
"بازرسی لاشه انجام می‌شود",
"شرایط سالن کشتار مناسب است",
"زنجیره سرد رعایت می‌شود"
],

"کشتارگاه طیور":[
"مجوز بهره‌برداری معتبر است",
"کنترل بهداشتی خط کشتار انجام می‌شود",
"دمای سردخانه کنترل می‌شود",
"ضدعفونی تجهیزات انجام می‌شود"
],

"کارخانه لبنیات":[
"کنترل مواد اولیه انجام می‌شود",
"آزمایش کنترل کیفیت انجام می‌شود",
"خط تولید بهداشتی است",
"شرایط CIP رعایت می‌شود",
"نمونه‌برداری انجام می‌شود"
],

"مرکز عرضه":[
"پروانه کسب معتبر است",
"دمای یخچال کنترل می‌شود",
"فرآورده دارای مشخصات است",
"نظافت محل مناسب است"
],

"سردخانه نگهداری":[
"دمای سردخانه ثبت می‌شود",
"چیدمان محصولات مناسب است",
"سوابق ورود و خروج ثبت می‌شود"
]

};


const availableGroups = activityGroups.filter(group=>{

if(group==="کشتارگاه"){

const countyData=countyUnits[county];

return countyData &&
countyData["کشتارگاه طیور"] &&
countyData["کشتارگاه طیور"].length>0;

}

return true;

});


return(
<div

className="dashboard-container"

dir="rtl"

>


<div className="expert-header">

<h1>

فرم ثبت بازدید نظارت بهداشتی

</h1>


<p>

اداره دامپزشکی شهرستان {county}

</p>


</div>



<form

className="dashboard-box"

onSubmit={(e)=>{

e.preventDefault();

console.log({

form,

healthItems,

violations,

samples,

checklist

});

alert("بازدید ثبت شد");

}}

>


<div className="form-section">

<h2>

اطلاعات مرکز

</h2>


<div className="form-grid">


<div>

<label>
نام بازرس
</label>

<input

name="inspectorName"

value={form.inspectorName}

onChange={updateField}

/>

</div>



<div>

<label>
سمت بازرس
</label>

<select

name="inspectorRole"

value={form.inspectorRole}

onChange={updateField}

>

<option value="">
انتخاب کنید
</option>

<option>
کارشناس بهداشت عمومی
</option>

<option>
رئیس اداره شهرستان
</option>

<option>
معاون سلامت
</option>

</select>

</div>



<div>

<label>
ساعت شروع بازدید
</label>

<input

type="time"

name="startTime"

value={form.startTime}

onChange={updateField}

/>

</div>


</div>


<div className="form-grid">


<div>

<label>
کد اپیدمیولوژیک واحد
</label>

<input

value={form.epidemiologyCode}

readOnly

/>

</div>



<div>

<label>
گروه فعالیت
</label>

<select

name="activityGroup"

value={form.activityGroup}

onChange={updateField}

>

<option value="">
انتخاب کنید
</option>


{

availableGroups.map(x=>(

<option key={x}>

{x}

</option>

))

}

</select>

</div>



<div>

<label>
نوع مرکز
</label>

<select

name="activityType"

value={form.activityType}

onChange={updateField}

>

<option value="">
انتخاب کنید
</option>


{

(form.activityGroup ?

activityTypes[form.activityGroup] || []

:[]

).map((x:string)=>(

<option key={x}>

{x}

</option>

))

}

</select>


</div>



<div>

<label>
نام مرکز
</label>


<select

name="unitName"

value={form.unitName}

onChange={(e)=>{

const unit =
countyUnits[county]
?.[form.activityType]
?.find(
(x:any)=>x.name===e.target.value
);


setForm({

...form,

unitName:e.target.value,

epidemiologyCode:unit?.code || "",

managerName:unit?.manager || "",

technicalManager:unit?.technical || ""

});

}}

>


<option value="">
انتخاب مرکز
</option>


{

countyUnits[county]
?.[form.activityType]
?.map((u:any)=>(

<option

key={u.code}

value={u.name}

>

{u.name}

</option>

))

}


</select>

</div>



<div>

<label>
نام مدیرعامل
</label>

<input

value={form.managerName}

readOnly

/>

</div>



<div>

<label>
مسئول فنی
</label>

<input

value={form.technicalManager}

readOnly

/>

</div>


</div>


</div>
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
علت بازدید
</label>

<select

name="visitReason"

value={form.visitReason || ""}

onChange={updateField}

>

<option value="">
انتخاب کنید
</option>

<option>
دوره‌ای
</option>

<option>
شکایت
</option>

<option>
پیگیری تخلف
</option>

<option>
بازدید موردی
</option>

</select>

</div>



<div>

<label>
نوع بازرسی
</label>


<select

name="inspectionType"

value={form.inspectionType || ""}

onChange={updateField}

>

<option value="">
انتخاب کنید
</option>

<option>
بازرسی مستقل
</option>

<option>
بازرسی مشترک
</option>

</select>


</div>


</div>


</div>



<div className="form-section">

<h2>
ارزیابی شرایط بهداشتی عمومی
</h2>


<div style={{overflowX:"auto"}}>


<table

style={{
width:"100%",
borderCollapse:"collapse"
}}

>


<thead>

<tr>

<th style={{border:"1px solid #ddd",padding:"10px"}}>
مورد ارزیابی
</th>


<th style={{border:"1px solid #ddd",padding:"10px"}}>
وضعیت
</th>


<th style={{border:"1px solid #ddd",padding:"10px"}}>
توضیحات
</th>


</tr>

</thead>


<tbody>


{

healthItems.map((item,index)=>(

<tr key={item.title}>


<td style={{border:"1px solid #ddd",padding:"10px"}}>

{item.title}

</td>



<td style={{border:"1px solid #ddd",padding:"10px"}}>


<select

value={item.status}

onChange={(e)=>
updateHealth(
index,
"status",
e.target.value
)
}

>

<option value="">
انتخاب کنید
</option>

<option value="مطلوب">
مطلوب
</option>

<option value="نامطلوب">
نامطلوب
</option>

<option value="نیاز به اصلاح">
نیاز به اصلاح
</option>


</select>


</td>




<td

style={{
border:"1px solid #ddd",
padding:"10px"
}}

>


<textarea

value={item.description}

onChange={(e)=>
updateHealth(
index,
"description",
e.target.value
)
}

placeholder="توضیحات بازرس"

rows={3}

style={{
width:"100%",
resize:"vertical"
}}

/>



<VoiceRecorder

onTextGenerated={(text)=>{

updateHealth(

index,

"description",

item.description

?

item.description+" "+text

:

text

)

}}

/>



</td>


</tr>


))

}


</tbody>


</table>


</div>


</div>
<div className="form-section">

<div

style={{
display:"flex",
justifyContent:"space-between",
alignItems:"center",
gap:"10px",
flexWrap:"wrap"
}}

>

<h2>
تخلفات و عدم انطباق‌ها
</h2>


<button

type="button"

className="upload-btn"

onClick={addViolation}

>

+ افزودن تخلف

</button>


</div>



<div

style={{
display:"grid",
gap:"12px",
marginTop:"15px"
}}

>


{

violations.map((v,index)=>(


<div

key={index}

style={{

border:"1px solid #ddd",

borderRadius:"10px",

padding:"12px",

background:"#fff"

}}

>


<div className="form-grid">


<div>

<label>
عنوان تخلف
</label>

<input

value={v.type}

onChange={(e)=>{

const copy=[...violations];

copy[index].type=e.target.value;

setViolations(copy);

}}

/>

</div>



<div>

<label>
شدت
</label>


<select

value={v.severity}

onChange={(e)=>{

const copy=[...violations];

copy[index].severity=e.target.value;

setViolations(copy);

}}

>


<option value="">
انتخاب کنید
</option>

<option value="خفیف">
خفیف
</option>

<option value="متوسط">
متوسط
</option>

<option value="شدید">
شدید
</option>


</select>


</div>



<div>

<label>
مهلت اصلاح
</label>

<input

value={v.deadline}

onChange={(e)=>{

const copy=[...violations];

copy[index].deadline=e.target.value;

setViolations(copy);

}}

/>

</div>



<div>

<label>
اقدام انجام شده
</label>


<input

value={v.action}

onChange={(e)=>{

const copy=[...violations];

copy[index].action=e.target.value;

setViolations(copy);

}}

/>

</div>



</div>


</div>


))

}


</div>


</div>





<div className="form-section">


<div

style={{
display:"flex",
justifyContent:"space-between",
alignItems:"center",
gap:"10px",
flexWrap:"wrap"
}}

>


<h2>
نمونه‌برداری
</h2>


<button

type="button"

className="upload-btn"

onClick={addSample}

>

+ افزودن نمونه

</button>


</div>
<div

style={{
display:"grid",
gap:"12px",
marginTop:"15px"
}}

>


{

samples.map((s,index)=>(


<div

key={index}

style={{

border:"1px solid #ddd",

borderRadius:"10px",

padding:"12px",

background:"#fff"

}}

>


<div className="form-grid">


<div>

<label>
نوع نمونه
</label>


<select

value={s.type}

onChange={(e)=>{

const copy=[...samples];

copy[index].type=e.target.value;

setSamples(copy);

}}

>


<option value="">
انتخاب کنید
</option>

<option value="گوشت">
گوشت
</option>

<option value="شیر">
شیر
</option>

<option value="آب">
آب
</option>

<option value="خوراک">
خوراک
</option>

<option value="سطح">
سطح
</option>


</select>


</div>



<div>

<label>
نتیجه آزمایش
</label>


<select

value={s.result}

onChange={(e)=>{

const copy=[...samples];

copy[index].result=e.target.value;

setSamples(copy);

}}

>


<option value="در انتظار نتیجه">
در انتظار نتیجه
</option>

<option value="مطلوب">
مطلوب
</option>

<option value="نامطلوب">
نامطلوب
</option>


</select>


</div>


</div>


</div>


))


}


</div>


</div>





<div className="form-section">


<h2>
چک‌لیست اختصاصی واحد
</h2>




{

specificChecklists[form.activityType]


?


<div

style={{

display:"flex",

flexDirection:"column",

gap:"15px"

}}

>


{

specificChecklists[form.activityType].map(

(item:string)=>(


<div

key={item}

style={{

border:"1px solid #ddd",

borderRadius:"12px",

padding:"18px",

background:"#fff",

display:"flex",

alignItems:"center",

gap:"12px"

}}

>


<input

type="checkbox"

checked={checklist.includes(item)}

onChange={()=>toggleChecklist(item)}

/>


<span>

{item}

</span>


</div>


)


)


}


</div>


:


<p>

ابتدا نوع مرکز را انتخاب کنید.

</p>


}


</div>
<div className="form-section">


<h2>
جمع‌بندی بازدید
</h2>



<div className="form-grid">



<div>

<label>
وضعیت نهایی بازدید
</label>


<select

name="finalStatus"

value={form.finalStatus || ""}

onChange={updateField}

>


<option value="">
انتخاب کنید
</option>


<option>
مطلوب
</option>


<option>
نیازمند اصلاح
</option>


<option>
دارای تخلف
</option>


</select>


</div>



<div>

<label>
توضیحات بازرس
</label>


<textarea

name="description"

value={form.description || ""}

onChange={updateField}

rows={4}

/>


</div>


</div>


</div>





<div

style={{

display:"flex",

justifyContent:"center",

marginTop:"25px"

}}

>


<button

className="upload-btn"

type="submit"

>

ثبت بازدید

</button>


</div>



</form>


</div>


)

}