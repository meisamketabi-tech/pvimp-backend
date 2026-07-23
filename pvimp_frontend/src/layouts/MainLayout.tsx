import React from "react";
import { Outlet } from "react-router-dom";
import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";
import "./MainLayout.css";


export default function MainLayout(){

return (

<div className="main-layout">

<Sidebar />


<div className="main-content">

<Header />

<main className="page-content">

<Outlet />

</main>

</div>


</div>

);

}
