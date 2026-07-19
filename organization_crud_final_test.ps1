$baseUrl="http://127.0.0.1:8000"

$login = curl.exe -s -X POST `
"$baseUrl/api/v1/auth/login?username=general_director&password=test" `
| ConvertFrom-Json

$token=$login.access_token

$auth="Authorization: Bearer $token"


Write-Host "TOKEN OK"


Write-Host ""
Write-Host "=== CREATE UNIT ==="

$body=@{
    name="واحد تست سامانه"
    code="TEST_SYSTEM_UNIT"
    parent_id=11
} | ConvertTo-Json


curl.exe -s `
-X POST `
"$baseUrl/organization/" `
-H $auth `
-H "Content-Type: application/json" `
-d $body


Write-Host ""
Write-Host "=== TREE CHECK ==="

curl.exe -s `
"$baseUrl/organization/tree" `
-H $auth


Write-Host ""
Write-Host "=== GET UNIT 51 ==="

curl.exe -s `
"$baseUrl/organization/51" `
-H $auth


Write-Host ""
Write-Host "=== UPDATE UNIT 51 ==="


$update=@{
    name="واحد تست بروزرسانی شده"
} | ConvertTo-Json


curl.exe -s `
-X PUT `
"$baseUrl/organization/51" `
-H $auth `
-H "Content-Type: application/json" `
-d $update



Write-Host ""
Write-Host "=== DELETE UNIT 51 ==="


curl.exe -s `
-X DELETE `
"$baseUrl/organization/51" `
-H $auth



Write-Host ""
Write-Host "=== FINISHED ==="

