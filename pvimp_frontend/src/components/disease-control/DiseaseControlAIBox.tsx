import React, { useState } from "react";
import { getToken } from "../../utils/token";
import "./DiseaseControlAIBox.css";

const API = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";

const examples = [
  "وضعیت واکسیناسیون بروسلوز گاوی در 3 ماهه اول سال 1405 نسبت به مدت مشابه سال 1404 چطور بوده؟",
  "عملکرد واکسیناسیون تب برفکی در بخش خصوصی چند درصد است؟",
  "کدام شهرستان‌ها در پوشش واکسیناسیون عقب هستند؟",
];

export default function DiseaseControlAIBox() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function ask(text = question) {
    if (!text.trim()) return;
    setBusy(true); setError(""); setAnswer("");
    try {
      const response = await fetch(`${API}/gis/disease-control-ai/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json", Authorization: `Bearer ${getToken()}` },
        body: JSON.stringify({ question: text }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data?.detail || "خطا در تحلیل سؤال");
      setAnswer(data?.answer || "پاسخی برای این سؤال پیدا نشد.");
    } catch (e: any) {
      setError(e?.message || "ارتباط با تحلیل‌گر برقرار نشد.");
    } finally { setBusy(false); }
  }

  return (
    <section className="dc-ai-box" dir="rtl">
      <div className="dc-ai-head">
        <div className="dc-ai-mark">AI</div>
        <div><div className="dc-ai-eyebrow">DATA-DRIVEN MANAGEMENT</div><h2>تحلیل‌گر هوشمند مبارزه با بیماری‌های دامی</h2><p>سؤال مدیریتی را به زبان طبیعی بنویسید؛ پاسخ از داده‌های واقعی سامانه و با ذکر مبنای محاسبه تولید می‌شود.</p></div>
      </div>
      <div className="dc-ai-input-row">
        <textarea value={question} onChange={(e) => setQuestion(e.target.value)} onKeyDown={(e) => { if ((e.ctrlKey || e.metaKey) && e.key === "Enter") ask(); }} placeholder="مثلاً: وضعیت واکسیناسیون بروسلوز گاوی در 3 ماهه اول 1405 نسبت به 1404 چطور بوده؟" rows={2} />
        <button onClick={() => ask()} disabled={busy || !question.trim()}>{busy ? "در حال تحلیل..." : "تحلیل سؤال"}</button>
      </div>
      <div className="dc-ai-examples">{examples.map((x) => <button key={x} onClick={() => { setQuestion(x); ask(x); }}>{x}</button>)}</div>
      {error && <div className="dc-ai-error">{error}</div>}
      {answer && <div className="dc-ai-answer"><div className="dc-ai-answer-title">پاسخ تحلیلی</div><div>{answer}</div></div>}
    </section>
  );
}
