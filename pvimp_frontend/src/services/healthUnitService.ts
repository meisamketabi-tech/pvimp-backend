
import axios from "axios";


const API="http://localhost:8000/health-units";



export const getHealthUnits=()=>
axios.get(API);



export const createHealthUnit=(data:any)=>
axios.post(
API,
data
);

