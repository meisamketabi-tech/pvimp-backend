
import axios from "axios";


const API="http://localhost:8000/notifications";



export const getNotifications=(id:number)=>
axios.get(
`${API}/${id}`
);



export const markNotificationRead=(id:number)=>
axios.put(
`${API}/${id}/read`
);

