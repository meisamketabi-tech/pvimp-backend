$root = ".\src"
$out = ".\broken_texts_report"

New-Item -ItemType Directory -Force -Path $out | Out-Null

Get-ChildItem $root -Recurse -File |
Where-Object {
    $_.Extension -in ".tsx",".ts",".css",".json"
} |
ForEach-Object {

    $file = $_.FullName

    $matches = Select-String `
        -Path $file `
        -Pattern '\?{3,}' `
        -AllMatches

    if ($matches) {

        $relative = $file.Replace((Get-Location).Path,"")

        $report = @"

==============================
FILE:
$relative

LINES:
$($matches.LineNumber -join ",")

TEXT:
$($matches.Line)

==============================

"@

        $name = $_.Name + ".txt"

        $report | Out-File `
            "$out\$name" `
            -Encoding UTF8
    }
}

Write-Host ""
Write-Host "Finished."
Write-Host "Reports saved in:"
Write-Host $out