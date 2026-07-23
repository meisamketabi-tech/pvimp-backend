import {create} from "zustand";
import type {User} from "../types/auth";
import {getToken,setToken,removeToken} from "../utils/token";


interface AuthState{

 user:User|null;

 token:string|null;

 login:(token:string)=>void;

 setUser:(user:User)=>void;

 logout:()=>void;

}


export const useAuthStore=create<AuthState>((set)=>({

 user:null,

 token:getToken(),

 login:(token)=>{

  setToken(token);

  set({
   token
  });

 },

 setUser:(user)=>{

  set({
   user
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