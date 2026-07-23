
import axios from "axios";


const API="http://localhost:8000/schedule";



export const createSchedule=(data:any)=>
axios.post(
API,
data
);



export const getSchedule=(id:number)=>
axios.get(
`${API}/${id}`
);



export const completeSchedule=(id:number)=>
axios.put(
`${API}/${id}/complete`
);

