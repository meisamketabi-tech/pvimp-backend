import axios from "axios";

const API = "http://localhost:8000/inspections";

export interface Inspection {
    id: number;
    inspection_number?: string;
    inspection_date?: string;
    status?: string;
    result?: string;
}

export const getInspections = () =>
    axios.get<Inspection[]>(API);

export const getOfficerInspections = (id: number) =>
    axios.get<Inspection[]>(`${API}/officer/${id}`);

export const createInspection = (data: any) =>
    axios.post(API, data);
