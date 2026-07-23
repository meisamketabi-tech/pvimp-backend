import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Sidebar.css";


const experts = [

{
title:"کارشناس بهداشت و مدیریت بیماری‌های دامی",
route:"disease"
},

{
title:"کارشناس قرنطینه و امنیت زیستی",
route:"quarantine"
},

{
title:"کارشناس نظارت بر بهداشت عمومی و مواد غذایی",
route:"supervision",
children:[
{
title:"ثبت بازرسی جدید",
path:"/create"
},
{
title:"بارگذاری فایل GIS",
path:"/import"
}
]
},

{
title:"کارشناس طیور و آبزیان",
route:"poultry"
},

{
title:"کارشناس تشخیص و درمان",
route:"diagnosis"
},

{
title:"کارشناس آزمایشگاه",
route:"laboratory"
}

];



const menu = [

{
title:"حوزه مدیرکل",
items:[

["دفتر مدیرکل","/"],
["نماینده ولی فقیه","/"],
["حراست","/"],
["امور حقوقی","/"],
["روابط عمومی","/"],
["پدافند غیرعامل و مدیریت بحران","/"]

]

},



{
title:"معاونت سلامت",
items:[

["معاون سلامت","/health-deputy"],
["اداره بهداشت و مدیریت بیماری‌های دامی","/disease-control"],
["واحد قرنطینه و امنیت زیستی","/quarantine"],
["اداره طیور، زنبور عسل، کرم ابریشم و آبزیان","/poultry"],
["اداره نظارت بر بهداشت عمومی و مواد غذایی","/supervision"],
["اداره تشخیص و درمان","/diagnosis"]

]

},



{
title:"معاونت توسعه و مدیریت منابع",
items:[

["معاون توسعه و مدیریت منابع","/"],
["اداره امور پشتیبانی و رفاه","/"],
["اداره امور مالی","/"],
["اداره فناوری اطلاعات، ارتباطات و تحول اداری","/"],
["اداره طرح، برنامه و بودجه","/"]

]

},



{
title:"ادارات شهرستان",

counties:[

["اداره دامپزشکی شهرستان ابهر","/county/0"],
["اداره دامپزشکی شهرستان ایجرود","/county/1"],
["اداره دامپزشکی شهرستان طارم","/county/2"],
["اداره دامپزشکی شهرستان زنجان","/county/3"],
["اداره دامپزشکی شهرستان خرمدره","/county/4"],
["اداره دامپزشکی شهرستان خدابنده","/county/5"],
["اداره دامپزشکی شهرستان سلطانیه","/county/6"],
["اداره دامپزشکی شهرستان ماهنشان","/county/7"]

]

}

];




export default function Sidebar(){


const navigate = useNavigate();


const [openMain,setOpenMain] = useState<number|null>(null);

const [openCounty,setOpenCounty] = useState<string|null>(null);

const [openExpert,setOpenExpert] = useState<string|null>(null);



return (

<aside className="sidebar" dir="rtl">


<div className="sidebar-header">

<h2>
سامانه مدیریت یکپارچه دامپزشکی
</h2>

<p>
استان زنجان
</p>

</div>




<div className="tree-menu">


{

menu.map((group,index)=>(


<div key={index}>


<div

className="tree-title"

onClick={()=>setOpenMain(
openMain===index ? null : index
)}

>

<span>
{
openMain===index ? "−" : "+"
}
</span>

{group.title}

</div>





{

openMain===index &&

<div>



{
group.items &&
group.items.map((item,i)=>(

<div

key={i}

className="tree-child"

onClick={()=>navigate(item[1])}

>

{item[0]}

</div>

))

}





{
group.counties &&
group.counties.map((county,i)=>{


const countyPath = county[1];


return (

<div key={i}>


<div

className="tree-title county-menu"

onClick={()=>setOpenCounty(
openCounty===countyPath
?
null
:
countyPath
)}

>

<span>

{
openCounty===countyPath
?
"−"
:
"+"
}

</span>

{county[0]}

</div>





{

openCounty===countyPath &&

<div>



<div

className="tree-child"

onClick={()=>navigate(
countyPath+"/manager"
)}

>

رئیس اداره

</div>





<div

className="tree-child"

onClick={()=>navigate(
countyPath+"/deputy"
)}

>

معاون اداره

</div>






{

experts.map((expert,e)=>{


const expertKey =
countyPath+"/"+expert.route;



return (

<div key={e}>


<div

className="tree-child"

onClick={()=>{


if(expert.children){

setOpenExpert(
openExpert===expertKey
?
null
:
expertKey
);

}

else{

navigate(
countyPath+
"/expert/"+
expert.route
);

}


}}

>


{
expert.children &&
(
openExpert===expertKey
?
"− "
:
"+ "
)
}


{expert.title}


</div>






{

expert.children &&
openExpert===expertKey &&

expert.children.map((child,c)=>(


<div

key={c}

className="tree-child"

style={{
paddingRight:"45px"
}}

onClick={()=>navigate(

countyPath+
"/expert/"+
expert.route+
child.path

)}

>

{child.title}

</div>


))

}



</div>

)

})

}



</div>

}


</div>

)


})

}



</div>

}



</div>


))

}



</div>


</aside>

)

}