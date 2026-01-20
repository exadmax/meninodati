@echo off
REM Atalho para executar o instalador do MENINO DA TI
REM Executa o script PowerShell em modo gráfico

setlocal enabledelayedexpansion

REM Obter o diretório do script
cd /d "%~dp0"

REM Verificar se o PowerShell está instalado
where powershell >nul 2>&1
if errorlevel 1 (
    echo Erro: PowerShell não está instalado no sistema
    pause
    exit /b 1
)

REM Verificar se installer.ps1 existe
if not exist installer.ps1 (
    echo Erro: installer.ps1 não encontrado
    echo O arquivo deve estar no mesmo diretório que este script
    pause
    exit /b 1
)

REM Executar o instalador PowerShell
echo Iniciando instalador...
echo.

REM Usar Set-ExecutionPolicy temporário para este processo
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0installer.ps1"

if errorlevel 1 (
    echo.
    echo Erro ao executar instalador
    pause
    exit /b 1
)

exit /b 0
