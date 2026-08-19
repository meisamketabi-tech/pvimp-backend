import React, { useEffect, useMemo, useState } from "react";
import "./LiveKpiDashboard.css";

const API_BASE = "/api/v1/gis/dashboard/kpi";

type AnyObj = Record<string, any>;

const nf = new Intl.NumberFormat("fa-IR", { maximumFractionDigits: 1 });
const pct = (v:number) => `${nf.format(Number(v||0))}%`;
const num = (v:number) => nf.format(Number(v||0));

function api(path:string){
  return fetch(`${API_BASE}${path}`, { credentials:"include" }).then(async r => {
    if(!r.ok) throw new Error(`${r.status} ${await r.text()}`);
    return r.json();
  });
}

function LineChart({data, color="#19d9ff", height=220}:{data:any[],color?:string,height?:number}){
  const w=760,h=height,p=34;
  if(!data?.length) return <div style={{padding:30,color:"#789"}}>Ø¯Ø§Ø¯Ù‡â€ŒØ§ÛŒ Ø¨Ø±Ø§ÛŒ Ù†Ù…ÙˆØ¯Ø§Ø± ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯</div>;
  const vals=data.map(x=>Number(x.value||0)); const max=Math.max(...vals,1);
  const pts=data.map((x,i)=>{
    const xx=p+(i*Math.max(1,(w-2*p)/(Math.max(1,data.length-1))));
    const yy=h-p-(Number(x.value||0)/max)*(h-2*p);
    return `${xx},${yy}`;
  }).join(" ");
  return <svg viewBox={`0 0 ${w} ${h}`} width="100%" height={height}>
    <line x1={p} x2={w-p} y1={h-p} y2={h-p} stroke="#173b50"/>
    <polyline points={pts} fill="none" stroke={color} strokeWidth="4"/>
    {data.map((x,i)=>{const [xx,yy]=pts.split(" ")[i].split(",");return <circle key={i} cx={xx} cy={yy} r="4" fill={color}/>})}
    {data.map((x,i)=><text key={`t${i}`} x={p+i*Math.max(1,(w-2*p)/(Math.max(1,data.length-1)))} y={h-10} fill="#7195a8" fontSize="11" textAnchor="middle">{String(x.period).slice(5)}</text>)}
  </svg>;
}

function BarChart({data, valueKey="value", color="#19d9ff"}:{data:any[],valueKey?:string,color?:string}){
  if(!data?.length) return <div style={{padding:30,color:"#789"}}>Ø¯Ø§Ø¯Ù‡â€ŒØ§ÛŒ Ø¨Ø±Ø§ÛŒ Ù†Ù…ÙˆØ¯Ø§Ø± ÙˆØ¬ÙˆØ¯ Ù†Ø¯Ø§Ø±Ø¯</div>;
  const max=Math.max(...data.map(x=>Number(x[valueKey]||0)),1);
  return <div style={{display:"flex",alignItems:"end",gap:10,height:220,padding:"10px 5px 20px"}}>
    {data.slice(0,12).map((x,i)=>{
      const v=Number(x[valueKey]||0); const h=Math.max(5,v/max*165);
      return <div key={i} style={{flex:1,textAlign:"center",minWidth:35}}>
        <div title={num(v)} style={{height:h,background:`linear-gradient(180deg,${color},#07506b)`,borderRadius:"5px 5px 0 0"}}/>
        <div style={{fontSize:10,color:"#8caebe",marginTop:5,overflow:"hidden"}}>{String(x.name||x.period||"").slice(0,12)}</div>
      </div>
    })}
  </div>;
}

function Donut({value,max,color="#19d9ff"}:{value:number,max:number,color?:string}){
  const p=Math.min(100,max?value/max*100:0);
  return <div style={{display:"flex",justifyContent:"center",alignItems:"center",height:220}}>
    <div style={{width:140,height:140,borderRadius:"50%",background:`conic-gradient(${color} ${p}%,#183748 0)` ,display:"grid",placeItems:"center"}}>
      <div style={{width:96,height:96,borderRadius:"50%",background:"#071b2c",display:"grid",placeItems:"center",textAlign:"center"}}>
        <strong style={{fontSize:22}}>{pct(p)}</strong><small style={{color:"#779"}}>Ù¾ÛŒØ´Ø±ÙØª</small>
      </div>
    </div>
  </div>;
}

function Card({label,value,sub,onClick}:{label:string,value:any,sub?:string,onClick?:()=>void}){
  return <div className="kpi-card" onClick={onClick} style={onClick?{cursor:"pointer"}:undefined}>
    <div className="label">{label}</div><div className="value">{value}</div>{sub&&<div className="sub">{sub}</div>}
  </div>
}

export default function LiveKpiDashboard(){
  const [data,setData]=useState<AnyObj|null>(null);
  const [tab,setTab]=useState("overview");
  const [unitId,setUnitId]=useState<number|null>(null);
  const [unit,setUnit]=useState<AnyObj|null>(null);
  const [unitMetric,setUnitMetric]=useState("all");
  const [loading,setLoading]=useState(true);
  const [error,setError]=useState("");
  const [refresh,setRefresh]=useState(0);

  useEffect(()=>{
    setLoading(true); setError("");
    api("/overview").then(setData).catch(e=>setError(String(e))).finally(()=>setLoading(false));
  },[refresh]);

  useEffect(()=>{
    if(unitId==null){setUnit(null);return}
    setLoading(true); api(`/units/${unitId}`).then(setUnit).catch(e=>setError(String(e))).finally(()=>setLoading(false));
  },[unitId]);

  const c=data?.cards||{};
  const series=data?.series||{};
  const diseases=data?.breakdowns?.disease_by_name||[];
  const counties=data?.breakdowns?.vaccination_by_county||[];

  const openMetric=(metric:string)=>{setUnitMetric(metric);setTab("units")};

  const tabs=[
    ["overview","Ù†Ù…Ø§ÛŒ Ú©Ù„ÛŒ"],
    ["disease","Ø¨ÛŒÙ…Ø§Ø±ÛŒ Ùˆ Ø§Ù¾ÛŒØ¯Ù…ÛŒÙˆÙ„ÙˆÚ˜ÛŒ"],
    ["care","Ù…Ø±Ø§Ù‚Ø¨Øª ÙØ¹Ø§Ù„"],
    ["lab","Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡ Ùˆ Ù†Ù…ÙˆÙ†Ù‡"],
    ["vaccination","ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†"],
    ["inventory","Ø²Ù†Ø¬ÛŒØ±Ù‡ ÙˆØ§Ú©Ø³Ù†"],
    ["units","ÙˆØ§Ø­Ø¯Ù‡Ø§ Ùˆ Drill-down"],
  ];

  if(loading && !data && !unit) return <div className="live-kpi-page">Ø¯Ø± Ø­Ø§Ù„ Ø¯Ø±ÛŒØ§ÙØª KPIÙ‡Ø§ÛŒ Ø²Ù†Ø¯Ù‡ Ø§Ø² PostgreSQL...</div>;
  if(error && !data) return <div className="live-kpi-page"><div className="kpi-panel"><b>Ø®Ø·Ø§:</b> {error}</div></div>;

  if(unitId!=null && unit){
    const v=unit.vaccination||{};
    const ops=unit.operation_counts||[];
    return <div className="live-kpi-page">
      <span className="back" onClick={()=>setUnitId(null)}>â† Ø¨Ø§Ø²Ú¯Ø´Øª Ø¨Ù‡ Ø¯Ø§Ø´Ø¨ÙˆØ±Ø¯</span>
      <div className="live-kpi-head">
        <div><h1>Ø¯Ø§Ø´Ø¨ÙˆØ±Ø¯ ÙˆØ§Ø­Ø¯: {unit.unit?.unit_name||`ÙˆØ§Ø­Ø¯ ${unitId}`}</h1><p>ØªÙ…Ø§Ù… Ø¹Ù…Ù„ÛŒØ§Øª Ø«Ø¨Øªâ€ŒØ´Ø¯Ù‡ Ø¨Ø±Ø§ÛŒ Ø§ÛŒÙ† ÙˆØ§Ø­Ø¯ + ÙˆØ¶Ø¹ÛŒØª Ù¾ÛŒØ´Ø±ÙØª ÙˆØ§Ù‚Ø¹ÛŒ</p></div>
        <span className="live-kpi-live">â— LIVE</span>
      </div>
      <div className="kpi-grid">
        <Card label="Ø¯Ø§Ù… ÙˆØ§Ø¬Ø¯ Ø´Ø±Ø§ÛŒØ· ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†" value={num(v.eligible)}/>
        <Card label="Ø¯Ø§Ù… ÙˆØ§Ú©Ø³ÛŒÙ†Ù‡â€ŒØ´Ø¯Ù‡" value={num(v.vaccinated)}/>
        <Card label="Ø¨Ø§Ù‚ÛŒâ€ŒÙ…Ø§Ù†Ø¯Ù‡" value={num(v.remaining)}/>
        <Card label="Ù¾ÛŒØ´Ø±ÙØª ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†" value={pct(v.coverage_percent)} sub="Ø§Ø² Ø¯Ø§Ø¯Ù‡ ÙˆØ§Ù‚Ø¹ÛŒ ÙˆØ§Ø­Ø¯"/>
        <Card label="ØªØ¹Ø¯Ø§Ø¯ Ø¹Ù…Ù„ÛŒØ§Øª Ø«Ø¨Øªâ€ŒØ´Ø¯Ù‡" value={num(unit.operation_history?.length||0)}/>
        <Card label="Ù¾ÛŒØ´â€ŒØ¨ÛŒÙ†ÛŒ Ø´Ù‡Ø±Ø³ØªØ§Ù†" value={num((unit.county_predictions||[])[0]?.value||0)} sub="scope: Ø´Ù‡Ø±Ø³ØªØ§Ù†"/>
      </div>
      <div className="kpi-two">
        <div className="kpi-panel"><h2>Ù¾ÛŒØ´Ø±ÙØª ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ† ÙˆØ§Ø­Ø¯</h2><Donut value={v.vaccinated||0} max={v.eligible||0}/></div>
        <div className="kpi-panel"><h2>ØªØ¹Ø¯Ø§Ø¯ Ø¹Ù…Ù„ÛŒØ§Øª Ø¨Ù‡ ØªÙÚ©ÛŒÚ© Ù†ÙˆØ¹</h2><BarChart data={ops} color="#35e28b"/></div>
      </div>
      <div className="kpi-panel"><h2>ØªØ§Ø±ÛŒØ®Ú†Ù‡ Ø¹Ù…Ù„ÛŒØ§Øª ÙˆØ§Ø­Ø¯</h2>
        <table className="kpi-table"><thead><tr><th>ØªØ§Ø±ÛŒØ®</th><th>Ø¹Ù…Ù„ÛŒØ§Øª</th></tr></thead>
        <tbody>{(unit.operation_history||[]).map((x:any,i:number)=><tr key={i}><td>{String(x.event_date||"").slice(0,19)}</td><td>{x.operation_type}</td></tr>)}</tbody></table>
      </div>
    </div>
  }

  return <div className="live-kpi-page">
    <div className="live-kpi-head">
      <div><h1>Ø¯Ø§Ø´Ø¨ÙˆØ±Ø¯ Ø²Ù†Ø¯Ù‡ Ú©Ù†ØªØ±Ù„ Ø¨ÛŒÙ…Ø§Ø±ÛŒ Ùˆ Ø¹Ù…Ù„ÛŒØ§Øª Ø¯Ø§Ù…Ù¾Ø²Ø´Ú©ÛŒ</h1><p>ØªÙ…Ø§Ù… Ø§Ø¹Ø¯Ø§Ø¯ Ø¯Ø± Ù‡Ø± Ø¯Ø±Ø®ÙˆØ§Ø³Øª Ù…Ø³ØªÙ‚ÛŒÙ…Ø§Ù‹ Ø§Ø² PostgreSQL Ø®ÙˆØ§Ù†Ø¯Ù‡ Ù…ÛŒâ€ŒØ´ÙˆÙ†Ø¯.</p></div>
      <button className="kpi-tab" onClick={()=>setRefresh(x=>x+1)}>â†» Ø¨Ø±ÙˆØ²Ø±Ø³Ø§Ù†ÛŒ</button>
    </div>

    <div className="kpi-tabs">{tabs.map(t=><button key={t[0]} className={`kpi-tab ${tab===t[0]?"active":""}`} onClick={()=>setTab(t[0])}>{t[1]}</button>)}</div>

    {tab==="overview" && <><div className="kpi-grid">
      <Card label="ÙˆØ§Ø­Ø¯Ù‡Ø§ÛŒ Ø§Ù¾ÛŒØ¯Ù…ÛŒÙˆÙ„ÙˆÚ˜ÛŒÚ©" value={num(c.total_units)} onClick={()=>openMetric("all")}/>
      <Card label="ÙˆØ§Ø­Ø¯Ù‡Ø§ÛŒ ÙØ¹Ø§Ù„" value={num(c.active_units)}/>
      <Card label="Ø¬Ù…Ø¹ÛŒØª Ø¯Ø§Ù… ØªØ­Øª Ù¾ÙˆØ´Ø´" value={num(c.total_livestock)}/>
      <Card label="Ú¯Ø²Ø§Ø±Ø´ Ø¨ÛŒÙ…Ø§Ø±ÛŒ" value={num(c.disease_reports)} onClick={()=>openMetric("disease_reports")}/>
      <Card label="Ù…Ø±Ø§Ù‚Ø¨Øª ÙØ¹Ø§Ù„" value={num(c.care_records)} onClick={()=>openMetric("care")}/>
      <Card label="ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ† Ø§Ù†Ø¬Ø§Ù…â€ŒØ´Ø¯Ù‡" value={num(c.vaccinated_animals)} onClick={()=>openMetric("vaccination")}/>
      <Card label="Ù¾ÙˆØ´Ø´ ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†" value={pct(c.vaccination_coverage)}/>
      <Card label="Ø¨Ø§Ù‚ÛŒâ€ŒÙ…Ø§Ù†Ø¯Ù‡ ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†" value={num(c.vaccination_remaining)} onClick={()=>openMetric("vaccination")}/>
      <Card label="Ù†ØªØ§ÛŒØ¬ Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡ÛŒ" value={num(c.lab_results)} onClick={()=>openMetric("lab")}/>
      <Card label="Ù†Ø±Ø® Ù…Ø«Ø¨Øª Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡" value={pct(c.lab_positive_rate)}/>
      <Card label="Ù…ÙˆØ¬ÙˆØ¯ÛŒ ÙˆØ§Ú©Ø³Ù†" value={num(c.inventory_packages)}/>
      <Card label="ÙˆØ§Ú©Ø³Ù† Ù†Ø²Ø¯ÛŒÚ© Ø§Ù†Ù‚Ø¶Ø§" value={num(c.expiring_30_days)}/>
    </div>
    <div className="kpi-layout">
      <div><div className="kpi-panel"><h2>Ø±ÙˆÙ†Ø¯ ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†</h2><div className="chart-box"><LineChart data={series.vaccination}/></div></div>
      <div className="kpi-two"><div className="kpi-panel"><h2>Ø±ÙˆÙ†Ø¯ Ú¯Ø²Ø§Ø±Ø´ Ø¨ÛŒÙ…Ø§Ø±ÛŒ</h2><LineChart data={series.disease_reports} color="#ff476b"/></div><div className="kpi-panel"><h2>Ù…ÙˆØ§Ø±Ø¯ Ù…Ø«Ø¨Øª Ù…Ø±Ø§Ù‚Ø¨Øª</h2><LineChart data={series.care_positive} color="#35e28b"/></div></div></div>
      <div><div className="kpi-panel"><h2>Ù¾ÙˆØ´Ø´ ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†</h2><Donut value={c.vaccinated_animals||0} max={c.eligible_animals||0}/></div>
      <div className="kpi-panel"><h2>Ø¨ÛŒÙ…Ø§Ø±ÛŒâ€ŒÙ‡Ø§ÛŒ Ù¾Ø±ØªÚ©Ø±Ø§Ø±</h2><BarChart data={diseases} color="#ff476b"/></div></div>
    </div>
    <div className="kpi-panel"><h2>Ù…Ù‚Ø§ÛŒØ³Ù‡ Ø¹Ù…Ù„Ú©Ø±Ø¯ ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ† Ø´Ù‡Ø±Ø³ØªØ§Ù†â€ŒÙ‡Ø§</h2><BarChart data={counties.map((x:any)=>({...x,value:x.coverage}))} color="#f4c542"/></div>
    </>}

    {tab==="disease" && <div className="kpi-layout"><div><div className="kpi-grid"><Card label="Ú¯Ø²Ø§Ø±Ø´ Ø¨ÛŒÙ…Ø§Ø±ÛŒ" value={num(c.disease_reports)} onClick={()=>openMetric("disease_reports")}/><Card label="ÙˆÙ‚ÙˆØ¹ Ø¨ÛŒÙ…Ø§Ø±ÛŒ" value={num(c.disease_occurrences)}/><Card label="Ø¨ÛŒÙ…Ø§Ø±ÛŒâ€ŒÙ‡Ø§ÛŒ Ø«Ø¨Øªâ€ŒØ´Ø¯Ù‡" value={num(c.diseases)}/><Card label="Ú©Ø§Ù†ÙˆÙ† ÙØ¹Ø§Ù„" value={num(c.active_outbreaks)}/></div><div className="kpi-panel"><h2>Ø±ÙˆÙ†Ø¯ Ú¯Ø²Ø§Ø±Ø´â€ŒÙ‡Ø§ÛŒ Ø¨ÛŒÙ…Ø§Ø±ÛŒ</h2><LineChart data={series.disease_reports} color="#ff476b" height={300}/></div></div><div className="kpi-panel"><h2>ØªÙˆØ²ÛŒØ¹ Ø¨ÛŒÙ…Ø§Ø±ÛŒâ€ŒÙ‡Ø§</h2><BarChart data={diseases} color="#ff476b"/></div></div>}

    {tab==="care" && <><div className="kpi-grid"><Card label="Ø±Ú©ÙˆØ±Ø¯ Ù…Ø±Ø§Ù‚Ø¨Øª" value={num(c.care_records)}/><Card label="Ø¯Ø§Ù… Ø¨Ø±Ø±Ø³ÛŒâ€ŒØ´Ø¯Ù‡" value={num(c.care_animals)}/><Card label="Ù…Ø«Ø¨Øª" value={num(c.care_positive)}/><Card label="Ù…Ù†ÙÛŒ" value={num(c.care_negative)}/><Card label="Ù…Ø´Ú©ÙˆÚ©" value={num(c.care_suspicious)}/><Card label="Ù†Ø±Ø® Ù…Ø«Ø¨Øª" value={pct(c.care_positive_rate)}/></div><div className="kpi-panel"><h2>Ø±ÙˆÙ†Ø¯ Ù…ÙˆØ§Ø±Ø¯ Ù…Ø«Ø¨Øª Ù…Ø±Ø§Ù‚Ø¨Øª</h2><LineChart data={series.care_positive} color="#35e28b" height={300}/></div></>}

    {tab==="lab" && <><div className="kpi-grid"><Card label="Ù†ØªØ§ÛŒØ¬ Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡ÛŒ" value={num(c.lab_results)} onClick={()=>openMetric("lab")}/><Card label="Ù†Ù…ÙˆÙ†Ù‡ Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡" value={num(c.lab_samples)}/><Card label="Ù†Ù…ÙˆÙ†Ù‡ Ø§Ø±Ø³Ø§Ù„â€ŒØ´Ø¯Ù‡" value={num(c.sent_samples)}/><Card label="Ù…Ø«Ø¨Øª" value={num(c.lab_positive)}/><Card label="Ù†Ø±Ø® Ù…Ø«Ø¨Øª" value={pct(c.lab_positive_rate)}/></div><div className="kpi-two"><div className="kpi-panel"><h2>ÙˆØ¶Ø¹ÛŒØª Ù†Ù…ÙˆÙ†Ù‡ Ùˆ Ù†ØªÛŒØ¬Ù‡</h2><BarChart data={[{name:"Ù†ØªÛŒØ¬Ù‡",value:c.lab_results},{name:"Ø§Ø±Ø³Ø§Ù„",value:c.sent_samples},{name:"Ù…Ø«Ø¨Øª",value:c.lab_positive}]} color="#19d9ff"/></div><div className="kpi-panel"><h2>ØªÙˆØ¶ÛŒØ­ Drill-down</h2><p style={{lineHeight:2,color:"#9eb9c5"}}>Ø§Ø² ØµÙØ­Ù‡ ÙˆØ§Ø­Ø¯Ù‡Ø§ Ù…ÛŒâ€ŒØªÙˆØ§Ù† ØªØ§ ÙˆØ§Ø­Ø¯ Ø§Ù¾ÛŒØ¯Ù…ÛŒÙˆÙ„ÙˆÚ˜ÛŒÚ© Ø±ÙØª Ùˆ ØªØ§Ø±ÛŒØ®Ú†Ù‡ Ø¹Ù…Ù„ÛŒØ§Øª Ù‡Ù…Ø§Ù† ÙˆØ§Ø­Ø¯ Ø±Ø§ Ø¯ÛŒØ¯. Ø¬Ø¯ÙˆÙ„ ÙÙ‚Ø· Ø¯Ø± Ø§Ù†ØªÙ‡Ø§ÛŒ Drill-down Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø´Ø¯Ù‡ Ø§Ø³Øª.</p></div></div></>}

    {tab==="vaccination" && <><div className="kpi-grid"><Card label="Ø¯Ø§Ù… ÙˆØ§Ø¬Ø¯ Ø´Ø±Ø§ÛŒØ·" value={num(c.eligible_animals)}/><Card label="ÙˆØ§Ú©Ø³ÛŒÙ†Ù‡â€ŒØ´Ø¯Ù‡" value={num(c.vaccinated_animals)}/><Card label="Ø¨Ø§Ù‚ÛŒâ€ŒÙ…Ø§Ù†Ø¯Ù‡" value={num(c.vaccination_remaining)}/><Card label="Ù¾ÙˆØ´Ø´" value={pct(c.vaccination_coverage)}/><Card label="ØªÙˆØ²ÛŒØ¹ Ø¨Ø³ØªÙ‡" value={num(c.distributed_packages)}/><Card label="Ø¯ÙØ¹ Ø¨Ø³ØªÙ‡" value={num(c.disposed_packages)}/></div><div className="kpi-two"><div className="kpi-panel"><h2>Ø±ÙˆÙ†Ø¯ ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†</h2><LineChart data={series.vaccination} height={300}/></div><div className="kpi-panel"><h2>Ù¾ÛŒØ´Ø±ÙØª</h2><Donut value={c.vaccinated_animals||0} max={c.eligible_animals||0} color="#35e28b"/></div></div><div className="kpi-panel"><h2>Ù…Ù‚Ø§ÛŒØ³Ù‡ Ø´Ù‡Ø±Ø³ØªØ§Ù†â€ŒÙ‡Ø§</h2><BarChart data={counties.map((x:any)=>({...x,value:x.coverage}))} color="#f4c542"/></div></>}

    {tab==="inventory" && <><div className="kpi-grid"><Card label="Ù…ÙˆØ¬ÙˆØ¯ÛŒ Ø¨Ø³ØªÙ‡" value={num(c.inventory_packages)}/><Card label="ØªÙˆØ²ÛŒØ¹â€ŒØ´Ø¯Ù‡" value={num(c.distributed_packages)}/><Card label="Ø¯ÙØ¹â€ŒØ´Ø¯Ù‡" value={num(c.disposed_packages)}/><Card label="Ù†Ø²Ø¯ÛŒÚ© Ø§Ù†Ù‚Ø¶Ø§ (Û³Û° Ø±ÙˆØ²)" value={num(c.expiring_30_days)}/></div><div className="kpi-panel"><h2>Ø¬Ø±ÛŒØ§Ù† Ø²Ù†Ø¬ÛŒØ±Ù‡ ÙˆØ§Ú©Ø³Ù†</h2><BarChart data={[{name:"Ù…ÙˆØ¬ÙˆØ¯ÛŒ",value:c.inventory_packages},{name:"ØªÙˆØ²ÛŒØ¹",value:c.distributed_packages},{name:"Ø¯ÙØ¹",value:c.disposed_packages},{name:"Ø§Ù†Ù‚Ø¶Ø§ÛŒ Ù†Ø²Ø¯ÛŒÚ©",value:c.expiring_30_days}]} color="#19d9ff"/></div></>}

    {tab==="units" && <UnitExplorer onOpen={setUnitId} metric={unitMetric}/>}
  </div>
}

function UnitExplorer({onOpen,metric}:{onOpen:(id:number)=>void,metric:string}){
  const [q,setQ]=useState("");
  const [rows,setRows]=useState<any[]>([]);
  const [loading,setLoading]=useState(false);

  useEffect(()=>{
    setLoading(true);
    api(`/drilldown/${metric}`).then(x=>setRows(x.units||[])).finally(()=>setLoading(false))
  },[metric]);

  const list=useMemo(()=>rows.filter(x=>!q||String(x.unit_name||"").includes(q)).slice(0,1000),[rows,q]);
  const title={
    all:"Ù‡Ù…Ù‡ Ø¹Ù…Ù„ÛŒØ§Øª",
    vaccination:"ÙˆØ§Ú©Ø³ÛŒÙ†Ø§Ø³ÛŒÙˆÙ†",
    disease_reports:"Ú¯Ø²Ø§Ø±Ø´ Ø¨ÛŒÙ…Ø§Ø±ÛŒ",
    care:"Ù…Ø±Ø§Ù‚Ø¨Øª",
    lab:"Ø¢Ø²Ù…Ø§ÛŒØ´Ú¯Ø§Ù‡",
    samples:"Ø§Ø±Ø³Ø§Ù„ Ù†Ù…ÙˆÙ†Ù‡",
    spraying:"Ø³Ù…Ù¾Ø§Ø´ÛŒ",
    operations:"ØªØ§Ø±ÛŒØ®Ú†Ù‡ Ø¹Ù…Ù„ÛŒØ§Øª",
  }[metric]||"ÙˆØ§Ø­Ø¯Ù‡Ø§";

  return <div>
    <div className="kpi-panel">
      <h2>Drill-down ÙˆØ§Ø­Ø¯Ù‡Ø§ â€” {title}</h2>
      <p style={{color:"#789",fontSize:12}}>Ú©Ù„ÛŒÚ© Ø±ÙˆÛŒ Ù‡Ø± KPIØŒ ÙˆØ§Ø­Ø¯Ù‡Ø§ÛŒ ØªØ´Ú©ÛŒÙ„â€ŒØ¯Ù‡Ù†Ø¯Ù‡ Ù‡Ù…Ø§Ù† KPI Ø±Ø§ Ù†Ø´Ø§Ù† Ù…ÛŒâ€ŒØ¯Ù‡Ø¯. Ø¨Ø§ Ú©Ù„ÛŒÚ© Ø±ÙˆÛŒ ÙˆØ§Ø­Ø¯ØŒ ØªØ§Ø±ÛŒØ®Ú†Ù‡ Ø¹Ù…Ù„ÛŒØ§Øª Ùˆ Ù¾ÛŒØ´Ø±ÙØª ÙÛŒØ²ÛŒÚ©ÛŒ Ù†Ù…Ø§ÛŒØ´ Ø¯Ø§Ø¯Ù‡ Ù…ÛŒâ€ŒØ´ÙˆØ¯.</p>
      <div className="unit-search"><input value={q} onChange={e=>setQ(e.target.value)} placeholder="Ø¬Ø³ØªØ¬ÙˆÛŒ Ù†Ø§Ù… ÙˆØ§Ø­Ø¯..."/></div>
      {loading?<div>Ø¯Ø± Ø­Ø§Ù„ Ø¯Ø±ÛŒØ§ÙØª Ø¯Ø§Ø¯Ù‡ Ø²Ù†Ø¯Ù‡...</div>:
       <div className="unit-list">{list.map(x=>
         <div className="unit-row" key={x.unit_id} onClick={()=>onOpen(Number(x.unit_id))}>
           <span>{x.unit_name||`ÙˆØ§Ø­Ø¯ ${x.unit_id}`}</span>
           <span>{num(x.value)} {metric==="vaccination"&&<span className={`badge ${Number(x.progress_percent||0)>=80?"good":Number(x.progress_percent||0)>=50?"warn":"bad"}`}>{pct(x.progress_percent||0)}</span>}</span>
         </div>)}
       </div>}
    </div>
  </div>
}
