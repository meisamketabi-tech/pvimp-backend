export interface User {
  id: number;
  username: string;
  full_name?: string | null;
  email?: string | null;
  mobile?: string | null;
  is_active: boolean;
  role?: string | null;
  roles?: string[];
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in?: number;
}
