import { create } from "zustand";
import type { User } from "../types/auth";
import { removeToken, setToken } from "../utils/token";

interface AuthState {
  user: User | null;
  token:string | null;
  login:(token:string)=>void;
  logout:()=>void;
}

export const useAuthStore = create<AuthState>((set)=>({

  user:null,
  token:null,

  login:(token)=>{
    setToken(token);
    set({
      token
    });
  },

  logout:()=>{
    removeToken();
    set({
      user:null,
      token:null
    });
  }

}));