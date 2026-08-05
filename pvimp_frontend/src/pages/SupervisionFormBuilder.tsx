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
year:"numeric",
month:"2-digit",
day:"2-digit"
}
).format(new Date());



const activityGroups = [

"کشتارگاه",

"کارگاه قطعه‌بندی و بسته‌بندی",

"مراکز عرضه فرآورده‌های خام دامی",

"مراکز تولید، فرآوری و بسته‌بندی فرآورده‌های خام دامی",

"کارخانجات لبنیات",

"مراکز جمع‌آوری شیر",

"سردخانه",

"ناوگان حمل فرآورده‌های خام دامی",

"کارخانجات خوراک دام، طیور و آبزیان"

];



const activityTypes:any = {


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

"قصابی",

"مرکز عرضه",

"فروشگاه زنجیره‌ای",

"هایپرمارکت"

],


"مراکز تولید، فرآوری و بسته‌بندی فرآورده‌های خام دامی":[

"فرآوری گوشت",

"بسته‌بندی گوشت",

"فرآوری آبزیان"

],


"کارخانجات لبنیات":[

"کارخانه لبنیات"

],


"مراکز جمع‌آوری شیر":[

"مرکز جمع‌آوری شیر"

],


"سردخانه":[

"سردخانه نگهداری"

],


"ناوگان حمل فرآورده‌های خام دامی":[

"خودروی یخچالدار",

"کانتینر یخچالدار"

],


"کارخانجات خوراک دام، طیور و آبزیان":[

"خوراک دام",

"خوراک طیور",

"خوراک آبزیان"

]


};



const organizationsList=[

"دانشگاه علوم پزشکی",

"اداره استاندارد",

"تعزیرات حکومتی",

"فرمانداری",

"محیط زیست",

"نیروی انتظامی",

"جهاد کشاورزی",

"صمت",

"سایر"

];



const generalChecklist=[

"بهداشت محیط واحد مناسب است",

"نظافت و شستشو انجام می‌شود",

"ضدعفونی طبق برنامه انجام می‌شود",

"کنترل حشرات و جوندگان انجام شده است",

"لباس کار کارکنان مناسب است",

"کارت بهداشت کارکنان معتبر است",

"بهداشت فردی رعایت می‌شود",

"امکانات شستشوی دست وجود دارد",

"آب مصرفی شرایط مناسب دارد",

"فاضلاب مدیریت می‌شود",

"زباله‌ها به شکل صحیح دفع می‌شوند",

"زنجیره سرد رعایت می‌شود",

"دمای نگهداری کنترل می‌شود",

"تجهیزات سالم هستند",

"سوابق بهداشتی ثبت می‌شود",

"آموزش کارکنان انجام شده است",

"مواد اولیه دارای مجوز هستند",

"برچسب گذاری صحیح است",

"تاریخ تولید و انقضا کنترل می‌شود",

"شرایط حمل مناسب است"

];
const specificChecklists:any={


"کشتارگاه دام":[

"مجوز بهره‌برداری معتبر است",

"وضعیت سالن کشتار مناسب است",

"محل نگهداری دام قبل از کشتار مناسب است",

"بازرسی قبل از کشتار انجام می‌شود",

"بازرسی لاشه انجام می‌شود",

"لاشه‌های ضبطی تفکیک شده‌اند",

"زنجیره سرد لاشه رعایت می‌شود",

"ابزار و تجهیزات کشتار بهداشتی هستند",

"آب گرم و سرد کافی وجود دارد",

"پساب کشتارگاه مدیریت می‌شود"

],



"کشتارگاه طیور":[

"مجوز بهره‌برداری معتبر است",

"شرایط دریافت طیور مناسب است",

"بازرسی قبل از کشتار انجام می‌شود",

"خط کشتار بهداشتی است",

"کنترل آلودگی لاشه انجام می‌شود",

"دمای سردخانه مناسب است",

"بسته‌بندی محصولات صحیح است",

"ضدعفونی تجهیزات انجام می‌شود"

],



"مرکز عرضه":[

"محل عرضه دارای پروانه است",

"ویترین و تجهیزات سردکن مناسب است",

"دمای یخچال کنترل می‌شود",

"فرآورده بدون مشخصات عرضه نمی‌شود",

"تفکیک فرآورده‌ها رعایت شده است",

"نظافت محل مناسب است"

],



"سردخانه نگهداری":[

"دمای سردخانه ثبت می‌شود",

"سیستم پایش دما فعال است",

"چیدمان فرآورده‌ها مناسب است",

"تفکیک محصولات انجام شده است",

"سوابق ورود و خروج ثبت می‌شود"

],



"کارخانه لبنیات":[

"کنترل مواد اولیه انجام می‌شود",

"آزمایش‌های کنترل کیفیت انجام می‌شود",

"خط تولید بهداشتی است",

"شرایط CIP رعایت می‌شود",

"نمونه‌برداری انجام می‌شود"

]


};


const [organizations,setOrganizations]=useState<string[]>([]);


const [checklist,setChecklist]=useState<string[]>([]);



const [form,setForm]=useState({

epiCode:"",

unitName:"",

activityGroup:"",

activityType:"",

parentType:"",

parentUnit:"",

owner:"",

technicalManager:"",

visitDate:today,

visitType:"",

inspectionType:""

});



const availableActivityTypes = useMemo(()=>{

return activityTypes[form.activityGroup] || [];

},[form.activityGroup]);



const hasTechnicalManager = useMemo(()=>{


return [

"کشتارگاه دام",

"کشتارگاه طیور",

"کارخانه لبنیات",

"فرآوری گوشت",

"بسته‌بندی گوشت",

"فرآوری آبزیان"

].includes(form.activityType);


},[form.activityType]);



const handleChange=(e:any)=>{


const {name,value}=e.target;


setForm(prev=>({

...prev,

[name]:value,


...(name==="activityGroup"
?
{
activityType:"",
parentType:"",
parentUnit:""
}
:
{})

}));



};



const toggleOrganization=(item:string)=>{


if(organizations.includes(item)){


setOrganizations(

organizations.filter(x=>x!==item)

);


}

else{


setOrganizations([

...organizations,

item

]);


}


};



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



const submit=(e:any)=>{


e.preventDefault();


console.log({

...form,

organizations,

checklist

});


alert("بازدید ثبت شد");


};
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

onSubmit={submit}

>



<div className="form-section">


<h2>

مشخصات واحد تحت نظارت

</h2>



<div className="form-grid">



<div>

<label>

کد اپیدمیولوژیک واحد

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

activityGroups.map(x=>

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

availableActivityTypes.map((x:string)=>

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

form.activityGroup!=="" &&


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

واحدهای شهرستان {county}

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

form.activityGroup==="کارگاه قطعه‌بندی و بسته‌بندی" &&



<div className="form-section">


<h2>

نحوه فعالیت کارگاه

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

مستقل

</option>


<option>

وابسته به کشتارگاه

</option>


<option>

وابسته به مرکز عرضه

</option>


</select>





{

form.parentType==="وابسته به کشتارگاه" &&


<select

name="parentUnit"

value={form.parentUnit}

onChange={handleChange}

>


<option>

کشتارگاه‌های شهرستان {county}

</option>


</select>


}





{

form.parentType==="وابسته به مرکز عرضه" &&


<select

name="parentUnit"

value={form.parentUnit}

onChange={handleChange}

>


<option>

مراکز عرضه شهرستان {county}

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

علت بازدید

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

دوره‌ای

</option>


<option>

شکایت

</option>


<option>

پیگیری تخلف

</option>


<option>

نمونه‌برداری

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

value={form.inspectionType}

onChange={handleChange}

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
{
form.inspectionType==="بازرسی مشترک" &&


<div className="form-section">


<h2>

دستگاه‌های حاضر در بازدید مشترک

</h2>



<div

style={{

display:"grid",

gridTemplateColumns:"repeat(auto-fill,minmax(220px,1fr))",

gap:"10px"

}}

>


{

organizationsList.map(item=>

<label

key={item}

style={{

border:"1px solid #ddd",

padding:"12px",

borderRadius:"8px",

background:"#fff"

}}

>


<input

type="checkbox"

checked={organizations.includes(item)}

onChange={()=>toggleOrganization(item)}

style={{marginLeft:"8px"}}

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

چک‌لیست عمومی نظارت بهداشتی

</h2>



<div

style={{

display:"grid",

gridTemplateColumns:"repeat(auto-fill,minmax(260px,1fr))",

gap:"10px"

}}

>


{

generalChecklist.map(item=>



<label

key={item}

style={{

border:"1px solid #ddd",

padding:"12px",

borderRadius:"8px",

background:"#fff"

}}

>


<input

type="checkbox"

checked={checklist.includes(item)}

onChange={()=>toggleChecklist(item)}

/>


<span style={{marginRight:"8px"}}>

{item}

</span>



</label>



)


}



</div>


</div>



<div className="form-section">


<h2>

چک‌لیست اختصاصی واحد

</h2>



{
specificChecklists[form.activityType] ? (

<div
style={{
display:"grid",
gridTemplateColumns:"repeat(auto-fill,minmax(260px,1fr))",
gap:"10px"
}}
>
{
specificChecklists[form.activityType].map((item: string) => (
<label
key={item}
style={{
border:"1px solid #ddd",
padding:"12px",
borderRadius:"8px",
background:"#fff",
display:"flex",
alignItems:"center",
cursor:"pointer"
}}
>
<input
type="checkbox"
checked={checklist.includes(item)}
onChange={()=>toggleChecklist(item)}
/>

<span style={{marginRight:"8px"}}>
{item}
</span>

</label>
))
}
</div>

) : (

<p>
?? ?? ?????? ??? ????? ??????? ??????? ????? ???? ??????.
</p>

)
}

</div>

<button

className="upload-btn"

type="submit"

>


ثبت بازدید


</button>




</form>



</div>


)

}
