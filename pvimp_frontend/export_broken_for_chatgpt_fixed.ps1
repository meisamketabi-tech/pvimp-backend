$source = ".\broken_texts_report"
$output = ".\broken_for_chatgpt.txt"

Remove-Item $output -ErrorAction SilentlyContinue

$files = Get-ChildItem $source -File

$count = 0

foreach ($file in $files) {

    $content = Get-Content $file.FullName -Raw -Encoding UTF8

    if ($null -eq $content) {
        continue
    }

    if ($content.Contains("????")) {

        Add-Content $output ""
        Add-Content $output "=============================="
        Add-Content $output "FILE: $($file.Name)"
        Add-Content $output "=============================="

        Add-Content $output $content

        $count++
    }
}

Write-Host ""
Write-Host "Finished"
Write-Host "Broken files exported: $count"
Write-Host "Output:"
Write-Host $output