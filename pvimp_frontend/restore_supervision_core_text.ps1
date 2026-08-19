$files = @{
"SupervisionDashboard.tsx"="Dashboard";
"SupervisionDashboardAdvanced.tsx"="Advanced Dashboard";
"SupervisionDashboardMenu.tsx"="Menu";
"SupervisionInspectionList.tsx"="Inspection List";
"SupervisionReports.tsx"="Reports";
"SupervisionViolations.tsx"="Violations";
"SupervisionSamples.tsx"="Samples";
"SupervisionLegal.tsx"="Legal Cases";
"SupervisionGISDashboard.tsx"="GIS Dashboard";
"SupervisionGISImport.tsx"="GIS Import"
}


$path="src\pages"


foreach($file in $files.Keys){

    $full="$path\$file"

    if(Test-Path $full){

        $content=Get-Content $full -Raw -Encoding UTF8

        $title=$files[$file]

        $content=$content -replace "<h1>.*?</h1>","<h1>$title</h1>"

        Set-Content `
        -Path $full `
        -Value $content `
        -Encoding UTF8

        Write-Host "Restored:" $file
    }
}


Write-Host "DONE"