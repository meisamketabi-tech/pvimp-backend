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

Write-Host "TOKEN OK"

$headers = @{
    Authorization = "Bearer $token"
    "Content-Type" = "application/json"
}


Write-Host ""
Write-Host "=== CREATE UNIT TEST ==="

$body = @{
    name = "واحد تست سامانه"
    code = "TEST_SYSTEM_UNIT"
    parent_id = 11
} | ConvertTo-Json


$create = curl.exe -s `
-X POST `
"$baseUrl/organization" `
-Headers $headers `
-d $body


Write-Host $create


Write-Host ""
Write-Host "=== ORGANIZATION TREE ==="

curl.exe -s `
"$baseUrl/organization/tree" `
-Headers $headers


Write-Host ""
Write-Host "=== GET UNIT 51 ==="

curl.exe -s `
"$baseUrl/organization/51" `
-Headers $headers


Write-Host ""
Write-Host "=== UPDATE UNIT 51 ==="

$updateBody = @{
    name = "واحد تست بروزرسانی شده"
} | ConvertTo-Json


curl.exe -s `
-X PUT `
"$baseUrl/organization/51" `
-Headers $headers `
-d $updateBody


Write-Host ""
Write-Host "=== DELETE UNIT 51 ==="

curl.exe -s `
-X DELETE `
"$baseUrl/organization/51" `
-Headers $headers


Write-Host ""
Write-Host "=== CRUD TEST FINISHED ==="
