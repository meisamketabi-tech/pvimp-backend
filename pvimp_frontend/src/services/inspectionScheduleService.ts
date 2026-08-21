
import axios from "axios";


const API="http://localhost:8000/inspection-schedules";



export const getInspectionSchedule=(officer:number)=>
axios.get(
`${API}/${officer}`
);



export const completeInspectionSchedule=(id:number)=>
axios.put(
`${API}/${id}/complete`
);

