@echo off
REM launcher.bat - Inicia o MENINO DA TI com seletor de modo

setlocal enabledelayedexpansion

REM Mudar para o diretório do script
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

REM Exibir mensagem de inicialização
echo.
echo ========================================
echo MENINO DA TI - SELETOR DE MODO
echo ========================================
echo.
echo Iniciando aplicacao...
echo.

REM Executar o launcher
python launcher.py

REM Verificar se houve erro
if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao executar a aplicacao.
    echo.
    pause
    exit /b 1
)

echo.
echo Aplicacao finalizada.
echo.
pause

exit /b 0
