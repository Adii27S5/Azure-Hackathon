# Packaging script for Azure App Service Zip Deploy
$sourceFiles = @("service.js", "src", "public", "package.json", "package-lock.json", "node_modules")
$zipPath = "deploy\app-package.zip"

if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}

Write-Host "Creating deployment archive $zipPath..."
Compress-Archive -Path $sourceFiles -DestinationPath $zipPath -Force
Write-Host "Package created successfully: $((Get-Item $zipPath).Length / 1MB) MB"
