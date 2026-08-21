
import axios from "axios";


const API="http://localhost:8000/reminders";



export const getReminders=()=>
axios.get(API);



export const completeReminder=(id:number)=>
axios.put(
`${API}/${id}/complete`
);

