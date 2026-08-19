import api from "./api";
import type { LoginRequest, LoginResponse, User } from "../types/auth";


export async function login(data: LoginRequest) {

    const formData = new URLSearchParams();

    formData.append(
        "username",
        data.username
    );

    formData.append(
        "password",
        data.password
    );


    const response =
        await api.post<LoginResponse>(
            "/api/v1/auth/login",
            formData,
            {
                headers: {
                    "Content-Type":
                        "application/x-www-form-urlencoded"
                }
            }
        );


    return response.data;

}


export async function getCurrentUser() {

    const response =
        await api.get<User>(
            "/api/v1/auth/me"
        );

    return response.data;

}