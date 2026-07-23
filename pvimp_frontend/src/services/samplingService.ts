
import axios from "axios";


const API="http://localhost:8000/sampling";



export const getSamples=()=>
axios.get(API);



export const createSample=(data:any)=>
axios.post(
API,
data
);

