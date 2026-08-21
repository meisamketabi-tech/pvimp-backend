import React, {useRef, useState} from "react";


interface Props{
onTextGenerated:(text:string)=>void;
}


export default function VoiceRecorder({onTextGenerated}:Props){

const [recording,setRecording]=useState(false);
const [seconds,setSeconds]=useState(0);

const mediaRecorder=useRef<MediaRecorder|null>(null);
const chunks=useRef<Blob[]>([]);
const timer=useRef<any>(null);


const startRecording=async()=>{

const stream=await navigator.mediaDevices.getUserMedia({
audio:true
});


mediaRecorder.current=new MediaRecorder(stream);

chunks.current=[];


mediaRecorder.current.ondataavailable=(e)=>{

if(e.data.size>0){

chunks.current.push(e.data);

}

};


mediaRecorder.current.onstop=()=>{


const audioBlob=new Blob(
chunks.current,
{
type:"audio/webm"
}
);


// فعلا تبدیل آزمایشی
// مرحله بعد اتصال به AI Speech To Text Backend

const text=
"متن استخراج شده از فایل صوتی پس از اتصال هوش مصنوعی";


onTextGenerated(text);


stream.getTracks().forEach(
track=>track.stop()
);


};


mediaRecorder.current.start();


setRecording(true);

setSeconds(0);


timer.current=setInterval(()=>{

setSeconds(x=>x+1);

},1000);


};



const stopRecording=()=>{


mediaRecorder.current?.stop();


setRecording(false);


clearInterval(timer.current);


};



return(

<div
style={{
display:"flex",
alignItems:"center",
gap:"10px",
marginTop:"8px"
}}
>


<button

type="button"

className="upload-btn"

onClick={
recording
?
stopRecording
:
startRecording
}

>

{
recording
?
`⏹ توقف ضبط (${seconds} ثانیه)`
:
"🎙 ضبط توضیحات"
}


</button>


</div>

);


}
