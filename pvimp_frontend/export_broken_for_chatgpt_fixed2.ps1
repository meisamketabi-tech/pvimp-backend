$root = ".\src"
$out = ".\broken_for_chatgpt.txt"

Remove-Item $out -ErrorAction SilentlyContinue

$count = 0

Get-ChildItem $root -Recurse -Include *.tsx,*.ts | ForEach-Object {

    $content = Get-Content $_.FullName -Raw -Encoding UTF8

    if ($null -ne $content -and $content -match '\?{2,}') {

        $count++

        Add-Content $out ""
        Add-Content $out "================================================"
        Add-Content $out "FILE:"
        Add-Content $out $_.FullName.Replace((Get-Location).Path,"\")
        Add-Content $out "================================================"
        Add-Content $out ""

        Add-Content $out $content
    }
}

Write-Host ""
Write-Host "Finished"
Write-Host "Broken files exported: $count"
Write-Host "Output:"
Write-Host $out