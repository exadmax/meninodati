@echo off
REM build_launcher.bat - Inicia o seletor de modo de build (GUI ou CLI)

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

REM Verificar e instalar PyInstaller silenciosamente
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Instalando PyInstaller... (isso pode levar um tempo)
    python -m pip install -q pyinstaller
)

echo.
echo ========================================
echo MENINO DA TI - SELETOR DE BUILD
echo ========================================
echo.

REM Executar o launcher de build
python build_launcher.py

if errorlevel 1 (
    echo.
    echo [ERRO] Erro ao executar construtor.
    echo.
    pause
    exit /b 1
)

exit /b 0
