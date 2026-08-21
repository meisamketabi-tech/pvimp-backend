$path="src\pages"

Get-ChildItem "$path\Supervision*.tsx" | ForEach-Object {

    $file=$_.FullName

    $content=Get-Content $file -Raw -Encoding UTF8

    $content=$content -replace '\?\?\?\?\?\?\s*',''

    Set-Content `
        -Path $file `
        -Value $content `
        -Encoding UTF8

    Write-Host "Fixed:" $_.Name
}

Write-Host "DONE"