$baseUrl="http://127.0.0.1:8000"

$login = curl.exe -s -X POST `
"$baseUrl/api/v1/auth/login?username=general_director&password=test" `
| ConvertFrom-Json

$token=$login.access_token

Write-Host "TOKEN:"
Write-Host $token


Write-Host ""
Write-Host "=== OPENAPI ORGANIZATION ROUTES ==="

curl.exe -s `
"$baseUrl/openapi.json" `
| Select-String "organization"

