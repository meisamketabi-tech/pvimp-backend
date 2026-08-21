
import React from "react";
import {useNavigate} from "react-router-dom";


export default function SupervisionDashboardMenu(){

const nav=useNavigate();


return(

<div className="dashboard-container" dir="rtl">

<div className="expert-header">

<h1>
???? ????? ?????
</h1>

</div>


<div className="dashboard-cards">


<button onClick={()=>nav("/supervision/create")}>
??? </button>


<button onClick={()=>nav("/supervision/list")}>
???? ??
</button>


<button onClick={()=>nav("/supervision/reports")}>
????? ??
</button>


<button onClick={()=>nav("/supervision/gis")}>
GIS
</button>


<button onClick={()=>nav("/supervision/violations")}>
</button>


<button onClick={()=>nav("/supervision/samples")}>
????? </button>


<button onClick={()=>nav("/supervision/legal")}>
????? ?????
</button>


</div>

</div>

)

}



