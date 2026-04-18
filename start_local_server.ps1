#!/usr/bin/env pwsh
# Simple local server to view report with working refresh button

Write-Host "🌐 Starting Local Report Server..." -ForegroundColor Cyan
Write-Host ""
Write-Host "This server serves your report WITH the GitHub token," -ForegroundColor Yellow
Write-Host "so the 'Refresh from Azure DevOps' button will work." -ForegroundColor Yellow
Write-Host ""

# Check if Python is available
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
}

if ($pythonCmd) {
    Write-Host "✓ Using Python HTTP Server" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Open your browser to:" -ForegroundColor Cyan
    Write-Host "   http://localhost:8000/live_report.html" -ForegroundColor White
    Write-Host ""
    Write-Host "   (The refresh button will work here!)" -ForegroundColor Green
    Write-Host ""
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
    Write-Host ""
    
    & $pythonCmd -m http.server 8000
} else {
    Write-Host "❌ Python not found. Installing alternative..." -ForegroundColor Red
    Write-Host ""
    Write-Host "Opening in default browser with file:// protocol..." -ForegroundColor Yellow
    Write-Host "(Note: Refresh button may not work due to CORS restrictions)" -ForegroundColor Yellow
    
    Start-Process "file:///$PWD/live_report.html"
}
