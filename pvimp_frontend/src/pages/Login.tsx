import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/auth.service";
import { useAuthStore } from "../store/auth.store";
import logo from "../assets/logo.png";


export default function Login(){

const navigate = useNavigate();

const authLogin = useAuthStore(
    state => state.login
);


const [username,setUsername] = useState("");
const [password,setPassword] = useState("");
const [error,setError] = useState("");


async function submit(e:React.FormEvent){

e.preventDefault();

setError("");

try{

const result = await login({
    username,
    password
});


console.log("LOGIN SUCCESS", result);


authLogin(
    result.access_token
);


navigate("/");


}catch(error:any){


console.error(
    "LOGIN ERROR",
    error
);


setError(
    error.response?.data?.detail ||
    "خطای ارتباط با سرور"
);


}

}



return (

<div dir="rtl" className="login-page">

<div className="login-container">


<div className="login-brand">


<img
src={logo}
className="login-logo"
/>


<h2>
سامانه مدیریت دامپزشکی
</h2>


<p>
سیستم هوشمند مدیریت و نظارت دامپزشکی استان زنجان
</p>


</div>



<div className="login-form">


<h1 className="login-title">
ورود به سامانه
</h1>


<p className="login-subtitle">
لطفا اطلاعات خود را وارد کنید
</p>



<form onSubmit={submit}>


<input

className="login-input"

placeholder="نام کاربری"

value={username}

onChange={
e=>setUsername(e.target.value)
}

/>



<input

type="password"

className="login-input"

placeholder="رمز عبور"

value={password}

onChange={
e=>setPassword(e.target.value)
}

/>



<button 
className="login-button"
type="submit"
>

ورود

</button>


</form>



{
error &&

<div
style={{
color:"red",
marginTop:"20px",
textAlign:"center"
}}
>

{error}

</div>

}


</div>


</div>


</div>

);

}

