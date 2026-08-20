import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/auth.service";
import { useAuthStore } from "../store/auth.store";
import logo from "../assets/logo.png";
import "./Login.css";

export default function Login() {
  const navigate = useNavigate();
  const authLogin = useAuthStore((state) => state.login);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const result = await login({ username, password });
      authLogin(result.access_token);
      navigate("/", { replace: true });
    } catch (err: any) {
      console.error("LOGIN ERROR", err);
      setError(err.response?.data?.detail || "نام کاربری یا رمز عبور صحیح نیست یا ارتباط با سرور برقرار نشد.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div dir="rtl" className="login-page">
      <div className="login-shell">
        <section className="login-visual">
          <div className="login-orbit" />
          <div className="login-brand">
            <img src={logo} className="login-logo" alt="سازمان دامپزشکی" />
            <div>
              <h2>سامانه مدیریت یکپارچه دامپزشکی</h2>
              <p>اداره کل دامپزشکی استان زنجان</p>
            </div>
          </div>

          <div className="login-hero">
            <div className="eyebrow">GIS • VET • INTELLIGENCE</div>
            <h1>تصمیم‌گیری دامپزشکی،<br /><span>داده‌محور و هوشمند</span></h1>
            <p>پایش عملیات، واکسیناسیون، بیماری‌ها، مراقبت و نقشه‌های GIS در یک محیط مدیریتی یکپارچه؛ با دسترسی متناسب با نقش سازمانی شما.</p>
          </div>

          <div className="login-features">
            <div className="login-feature"><b>داشبورد مدیریتی</b>نمای شمای کلی استان و شهرستان</div>
            <div className="login-feature"><b>GIS عملیاتی</b>رصد مکانی واحدها و رخدادها</div>
            <div className="login-feature"><b>AI Analytics</b>پاسخ تحلیلی از داده‌های سامانه</div>
            <div className="login-feature"><b>هشدار هوشمند</b>اعلام موارد بحرانی و نیازمند اقدام</div>
          </div>
        </section>

        <section className="login-form-panel">
          <h1 className="login-form-title">ورود به سامانه</h1>
          <p className="login-form-subtitle">برای ادامه، اطلاعات کاربری سازمانی خود را وارد کنید.</p>

          <form className="login-form" onSubmit={submit}>
            <label className="login-label">
              نام کاربری
              <input className="login-input" autoComplete="username" placeholder="مثلاً admin" value={username} onChange={(e) => setUsername(e.target.value)} required />
            </label>
            <label className="login-label">
              رمز عبور
              <input className="login-input" type="password" autoComplete="current-password" placeholder="رمز عبور" value={password} onChange={(e) => setPassword(e.target.value)} required />
            </label>
            {error && <div className="login-error">{error}</div>}
            <button className="login-button" type="submit" disabled={loading}>
              {loading ? "در حال ورود..." : "ورود امن به سامانه"}
            </button>
          </form>

          <div className="login-footnote">دسترسی‌ها بر اساس نقش و حوزه سازمانی کاربر اعمال می‌شوند. اطلاعات داشبورد مستقیماً از داده‌های سامانه خوانده می‌شود.</div>
        </section>
      </div>
    </div>
  );
}
