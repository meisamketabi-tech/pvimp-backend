import { Navigate } from "react-router-dom";
import { useAuthStore } from "../store/auth.store";
import type { ReactNode } from "react";

export default function ProtectedRoute(
{
 children
}:{
 children:ReactNode
}){

 const token = useAuthStore(
   state=>state.token
 );

 if(!token){
   return <Navigate to="/login"/>;
 }

 return children;
}