export interface User {
  id:number;
  username:string;
  full_name:string;
  role:string;
}

export interface LoginRequest {
  username:string;
  password:string;
}

export interface LoginResponse {
  access_token:string;
  token_type:string;
}