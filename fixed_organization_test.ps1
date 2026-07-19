$baseUrl = "http://127.0.0.1:8000"

$login = curl.exe -s -X POST `
"$baseUrl/api/v1/auth/login?username=general_director&password=test" `
| ConvertFrom-Json

$token = $login.access_token

Write-Host "TOKEN OK"


Write-Host ""
Write-Host "=== ORGANIZATION TREE ==="

curl.exe -s `
"$baseUrl/organization/tree" `
-H "Authorization: Bearer $token"



Write-Host ""
Write-Host "=== DASHBOARD ==="

curl.exe -s `
"$baseUrl/organization/dashboard" `
-H "Authorization: Bearer $token"



Write-Host ""
Write-Host "=== CRUD TEST FINISHED ==="
