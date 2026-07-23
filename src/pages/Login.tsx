import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/auth.service";
import { useAuthStore } from "../store/auth.store";

export default function Login(){

  const navigate = useNavigate();
  const authLogin = useAuthStore(
    state=>state.login
  );

  const [username,setUsername]=useState("");
  const [password,setPassword]=useState("");
  const [error,setError]=useState("");

  async function submit(e:React.FormEvent){

    e.preventDefault();

    try{

      const result = await login({
        username,
        password
      });

      authLogin(result.access_token);

      navigate("/");

    }catch{

      setError("??? ?????? ?? ??? ???? ???? ????");

    }
  }


  return (

    <div className="min-h-screen flex items-center justify-center bg-gray-100">

      <form
        onSubmit={submit}
        className="bg-white p-8 rounded-xl shadow w-96"
      >

        <h1 className="text-2xl font-bold mb-6 text-center">
          ???? ?? ?????? PVIMP
        </h1>


        <input
          className="border w-full p-3 mb-3 rounded"
          placeholder="??? ??????"
          value={username}
          onChange={e=>setUsername(e.target.value)}
        />


        <input
          className="border w-full p-3 mb-3 rounded"
          type="password"
          placeholder="??? ????"
          value={password}
          onChange={e=>setPassword(e.target.value)}
        />


        {
          error &&
          <div className="text-red-600 mb-3">
            {error}
          </div>
        }


        <button
          className="w-full bg-blue-600 text-white p-3 rounded"
        >
          ????
        </button>

      </form>

    </div>

  );
}