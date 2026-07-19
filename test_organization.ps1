$baseUrl = "http://127.0.0.1:8000"


Write-Host "=== LOGIN TEST ==="

$login = curl.exe -s -X POST `
"$baseUrl/api/v1/auth/login?username=general_director&password=test" `
| ConvertFrom-Json


$token = $login.access_token


if ($token) {
    Write-Host "TOKEN OK"
}
else {
    Write-Host "LOGIN FAILED"
    exit
}


$authHeader = "Authorization: Bearer $token"



Write-Host ""
Write-Host "=== ORGANIZATION DASHBOARD ==="

curl.exe -s `
"$baseUrl/organization/dashboard" `
-H $authHeader


Write-Host ""
Write-Host ""
Write-Host "=== ORGANIZATION TREE ==="

curl.exe -s `
"$baseUrl/organization/tree" `
-H $authHeader


Write-Host ""
Write-Host ""
Write-Host "=== UNIT USERS ==="

curl.exe -s `
"$baseUrl/organization/1/users" `
-H $authHeader


Write-Host ""
Write-Host ""
Write-Host "=== UNIT POSITIONS ==="

curl.exe -s `
"$baseUrl/organization/1/positions" `
-H $authHeader


Write-Host ""