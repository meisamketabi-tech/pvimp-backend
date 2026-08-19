$path="src\pages"

Get-ChildItem "$path\Supervision*.tsx" |
ForEach-Object {

    Write-Host $_.Name

}