
import axios from "axios";


const API="http://localhost:8000/inspections";



export const getInspections=()=>
axios.get(API);



export const getOfficerInspections=(id:number)=>
axios.get(
`${API}/officer/${id}`
);



export const createInspection=(data:any)=>
axios.post(
API,
data
);

