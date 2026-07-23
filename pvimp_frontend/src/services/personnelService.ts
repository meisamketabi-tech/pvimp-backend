
import axios from "axios";


const API="http://localhost:8000/personnel";



export const getPersonnel=()=>
axios.get(API);



export const createPersonnel=(data:any)=>
axios.post(
API,
data
);

