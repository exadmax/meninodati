@echo off
REM run_launcher_admin.bat - Executa o launcher com seletor de modo como administrador

echo ========================================
echo  MENINO DA TI - SELETOR DE MODO
echo ========================================
echo.
echo Solicitando privilegios de administrador...
echo.

REM Check for administrative privileges
net session >nul 2>&1
if %errorlevel% == 0 (
    echo Executando como Administrador!
    echo.
    setlocal enabledelayedexpansion
    cd /d "%~dp0"
    
    REM Verificar se Python está instalado
    python --version >nul 2>&1
    if errorlevel 1 (
        echo.
        echo [ERRO] Python nao foi encontrado no PATH!
        echo.
        echo Por favor, instale Python 3.8+ ou adicione-o ao PATH do sistema.
        echo.
        pause
        exit /b 1
    )
    
    REM Executar o auto_launcher em modo automático console
    echo Iniciando MENINO DA TI...
    echo.
    python auto_launcher.py console
    
) else (
    echo Privilegios de administrador necessarios!
    echo.
    echo Por favor, execute este script como Administrador:
    echo 1. Clique com botao direito em run_launcher_admin.bat
    echo 2. Selecione "Executar como administrador"
    echo 3. Clique em "Sim" na janela de confirmacao
    echo.
    pause
    exit /b 1
)

echo.
echo Aplicacao finalizada.
echo.
pause
exit /b 0
