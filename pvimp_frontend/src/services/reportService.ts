
import axios from "axios";


const API="http://localhost:8000/reports";



export const getReports=()=>
axios.get(API);



export const createReport=(data:any)=>
axios.post(
`${API}/create`,
data
);

