@echo off
REM Run as Administrator - Menino de TI Helper
REM This script requests administrator privileges before running

echo ========================================
echo  Menino de TI Helper - Admin Mode
echo ========================================
echo.
echo Solicitando privilegios de administrador...
echo.

REM Check for administrative privileges
net session >nul 2>&1
if %errorlevel% == 0 (
    echo Executando como Administrador!
    echo.
    call run.bat
) else (
    echo Privilegios de administrador necessarios!
    echo.
    echo Por favor, execute este arquivo com "Executar como administrador"
    echo Clique com botao direito no arquivo e selecione "Executar como administrador"
    echo.
    pause
)
