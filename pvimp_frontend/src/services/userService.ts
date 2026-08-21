import api from "./api";


export interface UserAssignment {
    id: number;

    organization_unit?: {
        id: number;
        name: string;
        code: string;
    } | null;

    position?: {
        id: number;
    } | null;

    role?: {
        id: number;
        name: string;
    } | null;

    is_primary: boolean;
    is_active: boolean;
    start_date: string;
    end_date?: string | null;
}


export interface UserDetails {

    id: number;
    username: string;
    full_name: string;
    email: string | null;
    mobile: string | null;
    is_active: boolean;

    assignments: UserAssignment[];
}



export async function getUserDetails(
    userId: number
): Promise<UserDetails>{

    const response = await api.get(
        `/users/${userId}/details`
    );

    return response.data;
}