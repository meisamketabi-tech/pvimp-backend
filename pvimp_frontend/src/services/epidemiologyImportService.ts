import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/v1";

export async function importEpidemiologyUnits(file: File) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await axios.post(
    `${API_URL}/gis/import/disease-control/epidemiology-units/import`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
}