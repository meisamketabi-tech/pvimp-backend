$baseUrl = "http://127.0.0.1:8000"

Write-Host "=== LOGIN ==="

$login = curl.exe -s -X POST `
"$baseUrl/api/v1/auth/login?username=general_director&password=test" `
| ConvertFrom-Json

$token = $login.access_token

if (!$token) {
    Write-Host "LOGIN FAILED"
    exit
}

$headers = @{
    Authorization = "Bearer $token"
    "Content-Type" = "application/json"
}


Write-Host "TOKEN OK"


Write-Host ""
Write-Host "=== CREATE POSITION TEST ==="


$positionBody = @{
    title = "کارشناس تست سازمان"
} | ConvertTo-Json


curl.exe -s `
-X POST `
"$baseUrl/organization/positions" `
-Headers $headers `
-d $positionBody



Write-Host ""
Write-Host "=== LIST POSITIONS ==="


curl.exe -s `
"$baseUrl/organization/positions" `
-Headers $headers



Write-Host ""
Write-Host "=== ASSIGN POSITION TO UNIT ==="


$assignBody = @{
    unit_id = 11
    position_id = 1
} | ConvertTo-Json


curl.exe -s `
-X POST `
"$baseUrl/organization/assign-position" `
-Headers $headers `
-d $assignBody



Write-Host ""
Write-Host "=== ORGANIZATION DASHBOARD ==="


curl.exe -s `
"$baseUrl/organization/dashboard" `
-Headers $headers


Write-Host ""
Write-Host "=== TEST FINISHED ==="
