$path = "src\pages\Supervision"


$texts = @{
    "SupervisionInspectionList.tsx" = "لیست بازرسی‌ها"
    "SupervisionSamples.tsx" = "نمونه‌برداری"
    "SupervisionLegal.tsx" = "پرونده‌های قضایی"
    "SupervisionGISDashboard.tsx" = "داشبورد GIS نظارت"
    "SupervisionGISImport.tsx" = "ورود اطلاعات GIS"
    "SupervisionLaboratoryResults.tsx" = "نتایج آزمایشگاه"
    "SupervisionViolations.tsx" = "تخلفات"
    "SupervisionAlerts.tsx" = "هشدارها"
    "SupervisionReports.tsx" = "گزارش‌ها"
    "SupervisionDashboard.tsx" = "داشبورد نظارت"
}


foreach($file in $texts.Keys){

    $full = Join-Path $path $file

    if(Test-Path $full){

        $content = Get-Content $full -Raw -Encoding UTF8


        # جایگزینی متن‌های خراب رایج
        $content = $content -replace "????+", $texts[$file]


        # اگر Title/label خالی شده باشد
        $content = $content -replace "title\s*:\s*['""]['""]",
            ("title: '" + $texts[$file] + "'")


        Set-Content `
            -Path $full `
            -Value $content `
            -Encoding UTF8


        Write-Host "Restored:" $file
    }
}


Write-Host "DONE"