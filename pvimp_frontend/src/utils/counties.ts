export const countyNames = [

"ابهر",
"ایجرود",
"طارم",
"زنجان",
"خرمدره",
"خدابنده",
"سلطانیه",
"ماهنشان"

];


export function getCountyName(id:string|undefined){

return countyNames[Number(id)] || "نامشخص";

}