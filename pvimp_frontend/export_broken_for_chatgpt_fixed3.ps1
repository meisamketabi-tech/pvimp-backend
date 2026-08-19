$root = ".\src"
$out = ".\broken_for_chatgpt.txt"

Remove-Item $out -Force -ErrorAction SilentlyContinue

$files = Get-ChildItem $root -Recurse -File -Include *.tsx,*.ts |
Where-Object {
    $_.Length -gt 0
}

$count = 0

foreach ($file in $files) {

    $content = Get-Content $file.FullName -Raw -Encoding UTF8

    if ($null -ne $content -and $content.Contains("????")) {

        Add-Content $out "================================================"
        Add-Content $out "FILE:"
        Add-Content $out ($file.FullName.Replace((Get-Location).Path,""))
        Add-Content $out "================================================"
        Add-Content $out ""

        Add-Content $out $content

        Add-Content $out ""
        Add-Content $out ""

        $count++
    }
}

Write-Host ""
Write-Host "Finished"
Write-Host "Broken files exported: $count"
Write-Host "Output:"
Write-Host $out