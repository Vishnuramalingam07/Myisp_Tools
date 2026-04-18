#!/usr/bin/env pwsh
# Quick setup script for GitHub Actions configuration

Write-Host "================================" -ForegroundColor Cyan
Write-Host "GitHub Actions Setup Wizard" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if .github/workflows directory exists
if (!(Test-Path ".\.github\workflows")) {
    Write-Host "✅ Creating .github/workflows directory..." -ForegroundColor Green
    New-Item -ItemType Directory -Path ".\.github\workflows" -Force | Out-Null
}

# Check if workflow file exists
if (Test-Path ".\.github\workflows\fetch-ado-data.yml") {
    Write-Host "✅ Workflow file exists: .github/workflows/fetch-ado-data.yml" -ForegroundColor Green
} else {
    Write-Host "❌ Workflow file NOT found!" -ForegroundColor Red
    Write-Host "   Expected: .github/workflows/fetch-ado-data.yml" -ForegroundColor Yellow
}

# Check if upload script exists
if (Test-Path ".\upload_to_firebase.py") {
    Write-Host "✅ Upload script exists: upload_to_firebase.py" -ForegroundColor Green
} else {
    Write-Host "❌ Upload script NOT found!" -ForegroundColor Red
    Write-Host "   Expected: upload_to_firebase.py" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣  Get Azure DevOps PAT Token" -ForegroundColor Yellow
Write-Host "    https://dev.azure.com/accenturecio08/_usersSettings/tokens" -ForegroundColor Gray
Write-Host ""
Write-Host "2️⃣  Add GitHub Secrets (4 required)" -ForegroundColor Yellow
Write-Host "    Go to: Settings → Secrets and variables → Actions" -ForegroundColor Gray
Write-Host ""
Write-Host "    ├── ADO_PAT = <your ADO token>" -ForegroundColor Gray
Write-Host "    ├── ADO_ORG = accenturecio08" -ForegroundColor Gray
Write-Host "    ├── ADO_PROJECT = AutomationProcess_29697" -ForegroundColor Gray
Write-Host "    └── FIREBASE_DATABASE_URL = https://myisptools-default-rtdb.firebaseio.com" -ForegroundColor Gray
Write-Host ""
Write-Host "3️⃣  Push to GitHub" -ForegroundColor Yellow
Write-Host "    git add ." -ForegroundColor Gray
Write-Host "    git commit -m `"Add GitHub Actions workflow`"" -ForegroundColor Gray
Write-Host "    git push origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "4️⃣  Test the workflow" -ForegroundColor Yellow
Write-Host "    GitHub → Actions → Run workflow" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 Full guide: GITHUB_ACTIONS_SETUP.md" -ForegroundColor Cyan
Write-Host ""

# Offer to commit files
Write-Host "Would you like to commit and push the workflow files now? (y/n): " -ForegroundColor Green -NoNewline
$response = Read-Host

if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host ""
    Write-Host "Committing files..." -ForegroundColor Cyan
    
    git add .github/workflows/fetch-ado-data.yml
    git add upload_to_firebase.py
    git add GITHUB_ACTIONS_SETUP.md
    git add .env.example
    
    git commit -m "Add GitHub Actions workflow for automatic ADO sync to Firebase"
    
    Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
    git push origin main
    
    Write-Host ""
    Write-Host "✅ Files pushed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Don't forget to add GitHub Secrets!" -ForegroundColor Yellow
    Write-Host "   Go to: https://github.com/Vishnuramalingam07/Myisp_Tools/settings/secrets/actions" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "Skipped. You can push manually later." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setup complete! 🚀" -ForegroundColor Green
