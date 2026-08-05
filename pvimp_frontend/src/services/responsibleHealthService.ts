import axios from "axios";

const API = "http://localhost:8000/responsible-health";

export const getStatistics = () =>
    axios.get(`${API}/statistics`);

export const getComplianceScore = (id: number) =>
    axios.get(`${API}/compliance-score/${id}`);

export const getOfficerSummary = (id: number) =>
    axios.get(`${API}/officer/${id}/summary`);

export const getOfficerDashboard = (id: number) =>
    axios.get(`${API}/officer/${id}/dashboard`);

export const createOfficer = (data: any) =>
    axios.post(`${API}/officers`, data);

export const createInspection = (data: any) =>
    axios.post(`${API}/inspections`, data);

export const createNonConformity = (data: any) =>
    axios.post(`${API}/non-conformities`, data);

export const createSample = (data: any) =>
    axios.post(`${API}/samples`, data);

export const createColdChain = (data: any) =>
    axios.post(`${API}/cold-chain`, data);

export const getInspections = () =>
    axios.get(`${API}/inspections`);

export const getNonConformities = () =>
    axios.get(`${API}/non-conformities`);

export const getSamples = () =>
    axios.get(`${API}/samples`);

export const getColdChain = () =>
    axios.get(`${API}/cold-chain`);
