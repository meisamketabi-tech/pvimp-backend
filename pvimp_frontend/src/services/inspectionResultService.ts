
import axios from "axios";


const API="http://localhost:8000/inspection-results";



export const getInspectionResults=(id:number)=>
axios.get(
`${API}/${id}`
);



export const createInspectionResult=(data:any)=>
axios.post(
API,
data
);

