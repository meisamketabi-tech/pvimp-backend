
import axios from "axios";


const API="http://localhost:8000/violation-followups";



export const getViolationFollowups=(id:number)=>
axios.get(
`${API}/${id}`
);



export const createViolationFollowup=(data:any)=>
axios.post(
API,
data
);

