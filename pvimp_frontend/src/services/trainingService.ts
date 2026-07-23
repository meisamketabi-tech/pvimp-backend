
import axios from "axios";

const API="http://localhost:8000/trainings";

export const getTrainings=()=>
axios.get(API);

export const createTraining=(data:any)=>
axios.post(
API,
data
);
