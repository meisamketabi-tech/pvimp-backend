import api from "./api";


export interface GISUnit {

    id: number;

    unit_name: string;

    unit_code: string;

    unit_type_id: number;

    province_id: number | null;

    county_id: number | null;

    latitude: number | null;

    longitude: number | null;

    cattle_count: number;

    sheep_count: number;

    goat_count: number;

    horse_count: number;

    dog_count: number;

    camel_count: number;

    buffalo_count: number;

    is_active: boolean;

}



export const gisService = {


    getUnits() {

        return api.get<GISUnit[]>(
            "/gis/epidemiology-units/"
        );

    },



    createUnit(data: any) {

        return api.post(
            "/gis/epidemiology-units/",
            data
        );

    },



    updateUnit(
        id: number,
        data: any
    ) {

        return api.put(
            `/gis/epidemiology-units/${id}`,
            data
        );

    },



    deleteUnit(
        id: number
    ) {

        return api.delete(
            `/gis/epidemiology-units/${id}`
        );

    },



    getUploadedFiles() {

        return api.get(
            "/gis/import/disease-control/files"
        );

    }


};