# Menino de TI Helper - PowerShell Launcher
# This script launches the Menino de TI Helper application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Menino de TI Helper - Iniciando" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if ($isAdmin) {
    Write-Host "✓ Executando como Administrador" -ForegroundColor Green
} else {
    Write-Host "⚠ AVISO: Não está executando como Administrador" -ForegroundColor Yellow
    Write-Host "Algumas funcionalidades podem não funcionar corretamente." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Para melhor funcionamento, execute este script com:" -ForegroundColor Yellow
    Write-Host "  powershell -ExecutionPolicy Bypass -File run.ps1" -ForegroundColor Cyan
    Write-Host "  como Administrador" -ForegroundColor Yellow
    Write-Host ""
}

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERRO: Python não está instalado ou não está no PATH" -ForegroundColor Red
    Write-Host "Por favor, instale o Python 3.7 ou superior" -ForegroundColor Red
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""
Write-Host "Verificando dependências..." -ForegroundColor Cyan

# Check if requirements are installed
$tkinterCheck = python -c "import tkinter" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠ Instalando dependências..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Erro ao instalar dependências" -ForegroundColor Red
        Read-Host "Pressione Enter para sair"
        exit 1
    }
} else {
    Write-Host "✓ Dependências OK" -ForegroundColor Green
}

Write-Host ""
Write-Host "Iniciando Menino de TI Helper..." -ForegroundColor Cyan
Write-Host ""

# Run the application
python main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "✗ O aplicativo encontrou um problema." -ForegroundColor Red
    Write-Host "Verifique os logs para mais detalhes." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Pressione Enter para sair"
}
