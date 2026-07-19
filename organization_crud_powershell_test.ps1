$baseUrl="http://127.0.0.1:8000"


$login = Invoke-RestMethod `
-Method POST `
-Uri "$baseUrl/api/v1/auth/login?username=general_director&password=test"


$token=$login.access_token


$headers=@{
    Authorization="Bearer $token"
}


Write-Host "TOKEN OK"



Write-Host ""
Write-Host "=== CREATE UNIT ==="


$body=@{
    name="واحد تست سامانه"
    code="TEST_SYSTEM_UNIT"
    parent_id=11
} | ConvertTo-Json -Depth 10


$created = Invoke-RestMethod `
-Method POST `
-Uri "$baseUrl/organization/" `
-Headers $headers `
-ContentType "application/json" `
-Body $body


$created



Write-Host ""
Write-Host "=== TREE ==="


Invoke-RestMethod `
-Method GET `
-Uri "$baseUrl/organization/tree" `
-Headers $headers



Write-Host ""
Write-Host "=== GET CREATED UNIT ==="


Invoke-RestMethod `
-Method GET `
-Uri "$baseUrl/organization/$($created.id)" `
-Headers $headers



Write-Host ""
Write-Host "=== UPDATE UNIT ==="


$update=@{
    name="واحد تست بروزرسانی شده"
} | ConvertTo-Json


Invoke-RestMethod `
-Method PUT `
-Uri "$baseUrl/organization/$($created.id)" `
-Headers $headers `
-ContentType "application/json" `
-Body $update



Write-Host ""
Write-Host "=== DELETE UNIT ==="


Invoke-RestMethod `
-Method DELETE `
-Uri "$baseUrl/organization/$($created.id)" `
-Headers $headers



Write-Host ""
Write-Host "=== FINISHED ==="

