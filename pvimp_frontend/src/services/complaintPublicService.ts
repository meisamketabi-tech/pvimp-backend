
import axios from "axios";


const API="http://localhost:8000/complaints";



export const submitComplaint=(data:any)=>
axios.post(
API,
data
);

